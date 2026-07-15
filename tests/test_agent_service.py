from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest

from paypal_agent.agent_service import AgentService
from paypal_agent.config import Settings
from paypal_agent.model_router import RoutedToolInput, RouterDecision, RouteResult
from paypal_agent.paypal_client import ToolCallInput
from paypal_agent.system_search import RequestLog


@pytest.mark.asyncio
async def test_chat_calls_exact_order_endpoint_and_returns_details(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            headers={"PayPal-Debug-Id": "debug-order-123"},
            json={
                "id": "ORDER-123",
                "status": "COMPLETED",
                "purchase_units": [{"reference_id": "PU-1"}],
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat("Show order ORDER-123", "test-thread")

    assert result["metadata"]["router_mode"] == "deterministic"
    assert result["metadata"]["orchestration"] == "langgraph"
    assert result["metadata"]["graph"] == "paypal_agent_chat_graph"
    assert result["router_decision"]["intent"] == "paypal_tool"
    assert result["selected_tool_names"] == ["paypal_orders_show_order_details"]
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/v2/checkout/orders/ORDER-123"
    assert result["tool_results"][0]["status_code"] == 200
    assert "COMPLETED" in result["answer"]
    assert "PU-1" in result["answer"]
    assert "debug-order-123" in result["answer"]


@pytest.mark.asyncio
async def test_chat_uses_user_transaction_dates_without_samples(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"transaction_details": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat(
            "List transactions from 2026-06-01 to 2026-06-15",
            "transaction-thread",
        )

    assert result["selected_tool_names"] == [
        "paypal_transaction_search_list_transactions"
    ]
    assert len(requests) == 1
    query = requests[0].url.params
    assert query["start_date"] == "2026-06-01T00:00:00Z"
    assert query["end_date"] == "2026-06-15T23:59:59Z"
    assert query["page_size"] == "100"
    assert "2025-02-20" not in str(requests[0].url)


@pytest.mark.asyncio
async def test_chat_rejects_long_transaction_range_before_request(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"transaction_details": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat(
            "List transactions from 2026-01-01 to 2026-02-15",
            "long-range-thread",
        )

    assert requests == []
    toolResult: dict[str, Any] = result["tool_results"][0]
    assert toolResult["status"] == "rejected"
    assert toolResult["status_code"] is None
    assert toolResult["request_sent"] is False
    assert toolResult["error"] == ("PayPal transaction searches cannot exceed 31 days.")
    assert "rejected before execution" in result["answer"]
    assert "Executed PayPal tool call" not in result["answer"]


@pytest.mark.asyncio
async def test_chat_surfaces_static_token_recovery_message(
    test_settings: Settings,
) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            401,
            headers={"PayPal-Debug-Id": "debug-static"},
            json={"name": "AUTHENTICATION_FAILURE"},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat("Show order ORDER-123", "static-token-thread")

    assert "Static tokens are never refreshed" in result["answer"]
    assert "remove it and set PAYPAL_CLIENT_ID" in result["answer"]


@pytest.mark.asyncio
async def test_chat_missing_order_id_makes_no_request(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat("Show order details", "missing-id-thread")

    assert requests == []
    assert result["router_decision"]["missing_inputs"] == ["order_id"]
    assert "order_id" in result["answer"]


@pytest.mark.asyncio
async def test_chat_mutation_returns_direct_confirmation_plan_without_request(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    routeResult: RouteResult = RouteResult(
        decision=RouterDecision(
            intent="paypal_tool",
            selected_tool_names=["paypal_invoices_invoices_send_invoice"],
            tool_input=RoutedToolInput(
                pathParams={"invoice_id": "INV2-123"},
                body={"subject": "Reminder"},
            ),
            missing_inputs=[],
            user_message="Prepared the exact invoice send request.",
            confidence=0.99,
        ),
        mode="test",
    )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        monkeypatch.setattr(
            service.router,
            "route",
            AsyncMock(return_value=routeResult),
        )
        result = await service.chat(
            "Send invoice INV2-123 with subject Reminder",
            "mutation-thread",
        )

    assert requests == []
    assert result["tool_results"] == []
    directCall: dict[str, Any] = result["required_direct_call"]
    assert directCall["method"] == "POST"
    assert directCall["path"] == ("/tools/paypal_invoices_invoices_send_invoice/call")
    assert directCall["payload"]["pathParams"] == {"invoice_id": "INV2-123"}
    assert directCall["payload"]["body"] == {"subject": "Reminder"}
    requestId: str = directCall["payload"]["headers"]["PayPal-Request-Id"]
    assert str(uuid.UUID(requestId)) == requestId
    assert directCall["requires"] == [
        "explicit user review",
        "separate direct caller sets confirm=true",
        "reuse PayPal-Request-Id for every retry",
        "PAYPAL_ALLOW_MUTATIONS=true",
    ]
    assert "was not executed" in result["answer"]
    assert '"confirm": true' not in result["answer"]


@pytest.mark.asyncio
async def test_mutation_plan_request_id_is_stable_across_retries(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requestIds: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requestIds.append(request.headers["PayPal-Request-Id"])
        return httpx.Response(202, json={})

    routeResult: RouteResult = RouteResult(
        decision=RouterDecision(
            intent="paypal_tool",
            selected_tool_names=["paypal_invoices_invoices_send_invoice"],
            tool_input=RoutedToolInput(
                pathParams={"invoice_id": "INV2-123"},
                body={"subject": "Reminder"},
            ),
            missing_inputs=[],
            user_message="Prepared the invoice send request.",
            confidence=0.99,
        ),
        mode="test",
    )
    mutationSettings: Settings = test_settings.model_copy(
        update={"paypal_allow_mutations": True}
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(mutationSettings, paypal_http_client=client)
        monkeypatch.setattr(
            service.router,
            "route",
            AsyncMock(return_value=routeResult),
        )
        plan: dict[str, Any] = await service.chat(
            "Send invoice INV2-123 with subject Reminder",
            "retry-thread",
        )
        payload: dict[str, Any] = {
            **plan["required_direct_call"]["payload"],
            "confirm": True,
        }
        for _attempt in range(2):
            await service.call_tool(
                "paypal_invoices_invoices_send_invoice",
                ToolCallInput.model_validate(payload),
            )

    assert len(requestIds) == 2
    assert requestIds[0] == requestIds[1]


@pytest.mark.parametrize("body", [{}, "invalid"])
@pytest.mark.asyncio
async def test_chat_rejects_missing_or_invalid_mutation_body(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
    body: Any,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    routeResult: RouteResult = RouteResult(
        decision=RouterDecision(
            intent="paypal_tool",
            selected_tool_names=["paypal_invoices_invoices_send_invoice"],
            tool_input=RoutedToolInput(
                pathParams={"invoice_id": "INV2-123"},
                body=body,
            ),
            missing_inputs=[],
            user_message="Prepared the invoice send request.",
            confidence=0.99,
        ),
        mode="test",
    )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        monkeypatch.setattr(
            service.router,
            "route",
            AsyncMock(return_value=routeResult),
        )
        result = await service.chat(
            "Send invoice INV2-123",
            "mutation-thread",
        )

    assert requests == []
    assert result["router_decision"]["missing_inputs"] == ["body"]
    assert result["required_direct_call"] is None
    assert "exact non-empty request body" in result["answer"]


class FailingBedrockClient:
    def converse(self, **_kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("router unavailable")


@pytest.mark.asyncio
async def test_chat_provider_error_makes_no_paypal_request(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    providerSettings = test_settings.model_copy(update={"model_router_enabled": True})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(
            providerSettings,
            paypal_http_client=client,
            bedrock_client=FailingBedrockClient(),
        )
        result = await service.chat("Show order ORDER-123", "error-thread")

    assert requests == []
    assert result["router_decision"]["intent"] == "clarify"
    assert result["metadata"]["router_error"]


@pytest.mark.asyncio
async def test_answer_models_are_skipped_for_guarded_routes(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    providerSettings: Settings = test_settings.model_copy(
        update={"model_router_enabled": True}
    )
    service = AgentService(providerSettings)

    def failIfCalled(*_args: Any, **_kwargs: Any) -> str:
        raise AssertionError("answer model must not be called")

    monkeypatch.setattr(service.agent_stack, "_complete", failIfCalled)
    cases: list[tuple[RouteResult, dict[str, Any]]] = [
        (
            RouteResult(
                decision=RouterDecision(
                    intent="clarify",
                    selected_tool_names=[],
                    missing_inputs=[],
                    user_message="Please clarify.",
                    confidence=0.9,
                ),
                mode="test",
            ),
            {},
        ),
        (
            RouteResult(
                decision=RouterDecision(
                    intent="paypal_tool",
                    selected_tool_names=["paypal_orders_show_order_details"],
                    tool_input=RoutedToolInput(pathParams={"order_id": "ORDER-123"}),
                    missing_inputs=[],
                    user_message="Low confidence.",
                    confidence=0.4,
                ),
                mode="test",
            ),
            {},
        ),
        (
            RouteResult(
                decision=RouterDecision(
                    intent="paypal_tool",
                    selected_tool_names=["paypal_orders_show_order_details"],
                    tool_input=RoutedToolInput(pathParams={"order_id": "ORDER-123"}),
                    missing_inputs=[],
                    user_message="Selected.",
                    confidence=0.9,
                ),
                mode="test",
            ),
            {"tool_call_results": [{"status": "success"}]},
        ),
        (
            RouteResult(
                decision=RouterDecision(
                    intent="paypal_tool",
                    selected_tool_names=["paypal_invoices_invoices_send_invoice"],
                    tool_input=RoutedToolInput(
                        pathParams={"invoice_id": "INV2-123"},
                        body={"subject": "Reminder"},
                    ),
                    missing_inputs=[],
                    user_message="Prepared.",
                    confidence=0.9,
                ),
                mode="test",
            ),
            {"required_direct_call": {"payload": {}}},
        ),
    ]

    for routeResult, routePayload in cases:
        answer: str = await service.agent_stack.answer(
            "untrusted user input",
            routeResult,
            routePayload,
            "safe deterministic fallback",
        )
        assert answer == "safe deterministic fallback"


@pytest.mark.asyncio
async def test_network_failure_is_not_reported_as_executed(
    test_settings: Settings,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection failed", request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat("Show order ORDER-123", "network-thread")

    assert "failed before receiving a response" in result["answer"]
    assert "Executed PayPal tool call" not in result["answer"]


@pytest.mark.asyncio
async def test_successful_mutation_ignores_memory_write_failure(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(201, json={"id": "ORDER-1"})

    def failMemoryWrite(
        _eventType: str,
        _payload: dict[str, Any],
    ) -> Path:
        raise OSError("disk full")

    mutationSettings: Settings = test_settings.model_copy(
        update={"paypal_allow_mutations": True}
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(mutationSettings, paypal_http_client=client)
        monkeypatch.setattr(
            service.memory,
            "append",
            failMemoryWrite,
        )
        result = await service.call_tool(
            "paypal_orders_create_order",
            ToolCallInput(
                body={"intent": "CAPTURE", "purchase_units": [{}]},
                headers={"PayPal-Request-Id": "stable-order-request"},
                confirm=True,
            ),
        )

    assert len(requests) == 1
    assert result["status"] == "success"
    assert result["status_code"] == 201


@pytest.mark.asyncio
async def test_direct_tool_memory_excludes_raw_paypal_response(
    test_settings: Settings,
) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"PayPal-Debug-Id": "debug-private"},
            json={
                "id": "ORDER-PRIVATE",
                "payer": {"email_address": "private@example.com"},
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.call_tool(
            "paypal_orders_show_order_details",
            ToolCallInput(pathParams={"order_id": "ORDER-PRIVATE"}),
        )

    assert result["response"]["payer"]["email_address"] == ("private@example.com")
    memoryText = _memory_text(test_settings.memory_dir)
    assert "private@example.com" not in memoryText
    assert "ORDER-PRIVATE" not in memoryText
    assert "debug-private" in memoryText


@pytest.mark.asyncio
async def test_chat_logs_and_system_search_exclude_request_content(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prompt: str = "Show order ORDER-PRIVATE for payer private@example.com"
    conversationId: str = "private-conversation-id"
    routeResult: RouteResult = RouteResult(
        decision=RouterDecision(
            intent="paypal_tool",
            selected_tool_names=["paypal_orders_show_order_details"],
            tool_input=RoutedToolInput(
                pathParams={"order_id": "ORDER-PRIVATE"},
            ),
            missing_inputs=[],
            user_message="Looking up the requested order.",
            confidence=0.99,
        ),
        mode="test",
    )

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"status": "COMPLETED"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        monkeypatch.setattr(
            service.router,
            "route",
            AsyncMock(return_value=routeResult),
        )
        await service.chat(prompt, conversationId)

    memoryText: str = _memory_text(test_settings.memory_dir)
    requestLogText: str = json.dumps(list(service.request_log.items))
    systemSearchResult: dict[str, Any] = service.system_search.search(prompt)
    systemSearchText: str = json.dumps(systemSearchResult)
    persistedText: str = memoryText + requestLogText + systemSearchText
    sensitiveValues: tuple[str, ...] = (
        prompt,
        "ORDER-PRIVATE",
        "private@example.com",
        conversationId,
    )

    assert all(value not in persistedText for value in sensitiveValues)
    assert '"user_input_length"' in memoryText
    assert '"conversation_id_length"' in memoryText
    assert systemSearchResult["query_length"] == len(prompt)
    assert "query" not in systemSearchResult


def test_request_log_discards_request_content() -> None:
    requestLog: RequestLog = RequestLog()
    requestLog.append(
        {
            "conversation_id": "private-conversation-id",
            "user_input": "ORDER-PRIVATE private@example.com",
            "status": "rejected",
        }
    )

    assert list(requestLog.items) == [{"status": "rejected"}]


def _memory_text(memoryDir: Path) -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in memoryDir.glob("*.jsonl")
    )


@pytest.mark.asyncio
async def test_chat_routes_system_search(test_settings: Settings) -> None:
    service = AgentService(test_settings)

    result = await service.chat("what tools are available for invoices", "thread")

    assert result["router_decision"]["intent"] == "system_search"
    assert result["selected_tool_names"] == ["system_search"]


@pytest.mark.asyncio
async def test_chat_writes_local_jsonl_memory(test_settings: Settings) -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda _request: httpx.Response(404, json={"name": "NOT_FOUND"})
        )
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        await service.chat("send an invoice for 50 dollars", "memory-thread")

    matches: list[dict[str, Any]] = service.memory.find("invoice")
    assert matches
    event: dict[str, Any] = matches[0]["event"]
    assert event["conversation_id_length"] == len("memory-thread")
    assert "conversation_id" not in event


@pytest.mark.asyncio
async def test_chat_routes_memory_find(test_settings: Settings) -> None:
    service = AgentService(test_settings)
    service.memory.append(
        "chat",
        {"selected_tool_names": ["paypal_invoices_list_invoices"]},
    )

    result = await service.chat("remember invoice", "thread")

    assert result["router_decision"]["intent"] == "memory_find"
    assert result["selected_tool_names"] == ["memory_find"]
    assert "paypal_invoices_list_invoices" in result["answer"]


@pytest.mark.asyncio
async def test_stream_chat_emits_langgraph_nodes(
    test_settings: Settings,
) -> None:
    service = AgentService(test_settings)

    events = [
        event
        async for event in service.stream_chat(
            "what tools are available for invoices",
            "thread",
        )
    ]

    node_names = [
        event["node"]
        for event in events
        if event["event"] == "node" and "node" in event
    ]
    final_events = [event for event in events if event["event"] == "result"]

    assert "shortlist_tools" in node_names
    assert "route_request" in node_names
    assert "run_system_search" in node_names
    assert final_events
    final_result = final_events[-1].get("result")
    assert isinstance(final_result, dict)
    assert final_result["metadata"]["orchestration"] == "langgraph"
