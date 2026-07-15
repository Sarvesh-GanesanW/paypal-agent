from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest

from paypal_agent.agent_service import AgentService
from paypal_agent.config import Settings
from paypal_agent.model_router import (
    RoutedToolInput,
    RouterDecision,
    RouteResult,
    SmallModelRouter,
)
from paypal_agent.paypal_client import ToolCallInput
from paypal_agent.postman import ApiTool
from paypal_agent.system_search import RequestLog, _isFullCatalogRequest


def _paypalDecision(toolName: str) -> RouterDecision:
    return RouterDecision(
        intent="paypal_tool",
        selected_tool_names=[toolName],
        tool_input=RoutedToolInput(),
        missing_inputs=[],
        user_message="selected",
        confidence=0.95,
    )


def _fakeModelDecision(
    _router: SmallModelRouter,
    userInput: str,
    _availableTools: list[ApiTool],
) -> RouterDecision:
    latestInput: str = userInput.rsplit("Latest user message:\n", 1)[-1]
    latestText: str = latestInput.lower()
    fullText: str = userInput.lower()

    if "what all tools" in latestText or "tools are available" in latestText:
        return RouterDecision(
            intent="system_search",
            selected_tool_names=["system_search"],
            tool_input=None,
            missing_inputs=[],
            user_message="selected",
            confidence=0.95,
        )
    if "remember" in latestText:
        return RouterDecision(
            intent="memory_find",
            selected_tool_names=["memory_find"],
            tool_input=None,
            missing_inputs=[],
            user_message="selected",
            confidence=0.95,
        )
    if "list paypal products" in latestText:
        return _paypalDecision(
            "paypal_subscriptions_catalog_products_list_products"
        )
    if "show product details" in latestText:
        return _paypalDecision(
            "paypal_subscriptions_catalog_products_show_product_details"
        )
    if "sales volume" in latestText:
        return _paypalDecision(
            "paypal_transaction_search_list_transactions"
        )
    if "list transactions" in latestText:
        return _paypalDecision(
            "paypal_transaction_search_list_transactions"
        )
    if "account balances" in latestText or "balanc check" in latestText:
        return _paypalDecision(
            "paypal_transaction_search_list_all_balances"
        )
    if "create order" in latestText:
        return _paypalDecision("paypal_orders_create_order")
    if "show invoice details" in latestText:
        return _paypalDecision(
            "paypal_invoices_invoices_show_invoice_details"
        )
    if "send invoice" in latestText or "send an invoice" in latestText:
        return _paypalDecision(
            "paypal_invoices_invoices_send_invoice"
        )
    if "show order" in latestText or "what order id" in latestText:
        return _paypalDecision("paypal_orders_show_order_details")
    if (
        "previous unresolved paypal request" in fullText
        and "order id" in latestText
    ):
        return _paypalDecision("paypal_orders_show_order_details")
    return RouterDecision(
        intent="clarify",
        selected_tool_names=[],
        tool_input=None,
        missing_inputs=[],
        user_message="clarify",
        confidence=0.3,
    )


@pytest.fixture(autouse=True)
def fakeModelRouter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        SmallModelRouter,
        "_route_with_provider",
        _fakeModelDecision,
    )


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

    assert result["metadata"]["router_mode"] == "bedrock"
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


@pytest.mark.parametrize(
    "userInput",
    [
        "What order id do I need?",
        "What order id should-I use?",
        "What order id 2 use?",
    ],
)
@pytest.mark.asyncio
async def test_chat_does_not_treat_ordinary_word_as_order_id(
    test_settings: Settings,
    userInput: str,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat(
            userInput,
            "ordinary-word-id-thread",
        )

    assert requests == []
    assert result["router_decision"]["missing_inputs"] == ["order_id"]
    assert result["router_decision"]["tool_input"]["path_params"] == {}


@pytest.mark.asyncio
async def test_chat_missing_input_does_not_echo_provider_message(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    routeResult: RouteResult = RouteResult(
        decision=RouterDecision(
            intent="paypal_tool",
            selected_tool_names=["paypal_orders_show_order_details"],
            tool_input=RoutedToolInput(pathParams={}),
            missing_inputs=["order_id"],
            user_message="Show order details",
            confidence=0.95,
        ),
        mode="bedrock",
    )
    service = AgentService(test_settings)
    monkeypatch.setattr(
        service.router,
        "route",
        AsyncMock(return_value=routeResult),
    )

    result = await service.chat("Show order details", "echo-thread")

    assert result["answer"] == "I need order_id before calling PayPal."


@pytest.mark.asyncio
async def test_chat_uses_pending_request_for_follow_up_id(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"id": "TEST-ORDER-123"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        firstResult = await service.chat(
            "Show order details",
            "follow-up-thread",
        )
        secondResult = await service.chat(
            "The order ID is TEST-ORDER-123",
            "follow-up-thread",
        )

    assert firstResult["router_decision"]["missing_inputs"] == ["order_id"]
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/v2/checkout/orders/TEST-ORDER-123"
    assert secondResult["selected_tool_names"] == ["paypal_orders_show_order_details"]


@pytest.mark.asyncio
async def test_new_request_id_wins_over_pending_request_id(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"id": "INV2-NEW"})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        firstResult = await service.chat(
            "Send invoice with invoice ID INV2-OLD",
            "new-invoice-id-thread",
        )
        secondResult = await service.chat(
            "Show invoice details for invoice ID INV2-NEW",
            "new-invoice-id-thread",
        )

    assert firstResult["router_decision"]["missing_inputs"] == [
        "request body"
    ]
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == (
        "/v2/invoicing/invoices/INV2-NEW"
    )
    assert secondResult["selected_tool_names"] == [
        "paypal_invoices_invoices_show_invoice_details"
    ]


@pytest.mark.parametrize(
    "followUp",
    [
        "I can provide the order ID: TEST-ORDER-123",
        "Confirm the order ID is TEST-ORDER-123",
        "Add order ID TEST-ORDER-123",
    ],
)
@pytest.mark.asyncio
async def test_follow_up_verbs_do_not_clear_pending_request(
    test_settings: Settings,
    followUp: str,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"id": "TEST-ORDER-123"})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        await service.chat("Show order details", "verb-follow-up")
        result = await service.chat(followUp, "verb-follow-up")

    assert len(requests) == 1
    assert requests[0].url.path == "/v2/checkout/orders/TEST-ORDER-123"
    assert result["selected_tool_names"] == ["paypal_orders_show_order_details"]


@pytest.mark.asyncio
async def test_stream_chat_uses_pending_request_for_follow_up_id(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"id": "STREAM-ORDER-123"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        firstEvents = [
            event
            async for event in service.stream_chat(
                "Show order details",
                "stream-follow-up",
            )
        ]
        secondEvents = [
            event
            async for event in service.stream_chat(
                "The order ID is STREAM-ORDER-123",
                "stream-follow-up",
            )
        ]

    firstResult = firstEvents[-1].get("result")
    secondResult = secondEvents[-1].get("result")
    assert isinstance(firstResult, dict)
    assert isinstance(secondResult, dict)
    assert firstResult["router_decision"]["missing_inputs"] == ["order_id"]
    assert len(requests) == 1
    assert requests[0].url.path == "/v2/checkout/orders/STREAM-ORDER-123"
    assert secondResult["tool_results"][0]["status_code"] == 200


@pytest.mark.asyncio
async def test_pending_request_is_isolated_by_conversation(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        await service.chat("Show order details", "conversation-a")
        result = await service.chat(
            "The order ID is TEST-ORDER-123",
            "conversation-b",
        )

    assert requests == []
    assert result["router_decision"]["intent"] == "clarify"


@pytest.mark.asyncio
async def test_explicit_new_action_replaces_pending_request(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"products": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        await service.chat("Show order details", "switch-thread")
        result = await service.chat("List PayPal products", "switch-thread")

    assert len(requests) == 1
    assert requests[0].url.path == "/v1/catalogs/products"
    assert result["selected_tool_names"] == [
        "paypal_subscriptions_catalog_products_list_products"
    ]


@pytest.mark.asyncio
async def test_new_incomplete_action_replaces_pending_request(
    test_settings: Settings,
) -> None:
    service = AgentService(test_settings)

    await service.chat("Show order details", "switch-missing-thread")
    result = await service.chat(
        "Actually show product details",
        "switch-missing-thread",
    )

    assert result["selected_tool_names"] == [
        "paypal_subscriptions_catalog_products_show_product_details"
    ]
    assert result["router_decision"]["missing_inputs"] == ["product_id"]
    assert service.pending_requests["switch-missing-thread"][1] == (
        "paypal_subscriptions_catalog_products_show_product_details"
    )


@pytest.mark.asyncio
async def test_same_conversation_requests_are_serialized(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    firstStarted: asyncio.Event = asyncio.Event()
    releaseFirst: asyncio.Event = asyncio.Event()

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"products": []})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)

        async def routeRequest(
            userInput: str,
            _availableTools: list[ApiTool],
        ) -> RouteResult:
            if userInput == "Show order details":
                firstStarted.set()
                await releaseFirst.wait()
                return RouteResult(
                    decision=RouterDecision(
                        intent="paypal_tool",
                        selected_tool_names=[
                            "paypal_orders_show_order_details"
                        ],
                        tool_input=RoutedToolInput(),
                        missing_inputs=["order_id"],
                        user_message="Missing order ID.",
                        confidence=0.9,
                    ),
                    mode="test",
                )
            return RouteResult(
                decision=RouterDecision(
                    intent="paypal_tool",
                    selected_tool_names=[
                        "paypal_subscriptions_catalog_products_list_products"
                    ],
                    tool_input=RoutedToolInput(),
                    missing_inputs=[],
                    user_message="Listing products.",
                    confidence=0.9,
                ),
                mode="test",
            )

        monkeypatch.setattr(service.router, "route", routeRequest)
        firstTask: asyncio.Task[dict[str, Any]] = asyncio.create_task(
            service.chat("Show order details", "serialized-thread")
        )
        await firstStarted.wait()
        secondTask: asyncio.Task[dict[str, Any]] = asyncio.create_task(
            service.chat("List PayPal products", "serialized-thread")
        )
        await asyncio.sleep(0)
        releaseFirst.set()
        firstResult, secondResult = await asyncio.gather(
            firstTask,
            secondTask,
        )

    assert firstResult["router_decision"]["missing_inputs"] == ["order_id"]
    assert secondResult["selected_tool_names"] == [
        "paypal_subscriptions_catalog_products_list_products"
    ]
    assert "serialized-thread" not in service.pending_requests


@pytest.mark.asyncio
async def test_expired_pending_request_is_not_reused(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    currentTime: float = 100.0
    monkeypatch.setattr(
        "paypal_agent.agent_service.time.monotonic",
        lambda: currentTime,
    )
    service = AgentService(test_settings)

    await service.chat("Show order details", "expiry-thread")
    currentTime = 1_001.0
    result = await service.chat(
        "The order ID is PRIVATE-ORDER-123",
        "expiry-thread",
    )

    assert result["router_decision"]["intent"] == "clarify"
    assert "expiry-thread" not in service.pending_requests


@pytest.mark.asyncio
async def test_expired_pending_requests_are_swept_by_other_conversations(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    currentTime: float = 100.0
    monkeypatch.setattr(
        "paypal_agent.agent_service.time.monotonic",
        lambda: currentTime,
    )
    service = AgentService(test_settings)

    await service.chat("Show order details", "expired-conversation")
    currentTime = 1_001.0
    await service.chat("Show product details", "active-conversation")

    assert "expired-conversation" not in service.pending_requests
    assert "active-conversation" in service.pending_requests


@pytest.mark.asyncio
async def test_chat_rejects_unbounded_input_and_conversation_id(
    test_settings: Settings,
) -> None:
    service = AgentService(test_settings)

    with pytest.raises(ValueError, match="user_input"):
        await service.chat("x" * 8_193, "bounded-thread")
    with pytest.raises(ValueError, match="conversation_id"):
        await service.chat("Show order details", "x" * 129)


@pytest.mark.asyncio
async def test_missing_mutation_body_is_not_duplicated(
    test_settings: Settings,
) -> None:
    service = AgentService(test_settings)

    result = await service.chat("Create order for 50 USD", "body-thread")

    assert result["router_decision"]["missing_inputs"] == ["request body"]
    assert result["answer"].count("exact non-empty request body") == 1


@pytest.mark.asyncio
async def test_sales_volume_paginates_and_aggregates_by_currency(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def transaction(
        eventCode: str,
        status: str,
        currency: str,
        value: str,
    ) -> dict[str, Any]:
        return {
            "transaction_info": {
                "transaction_event_code": eventCode,
                "transaction_status": status,
                "transaction_amount": {
                    "currency_code": currency,
                    "value": value,
                },
            }
        }

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        pageNumber: int = int(request.url.params["page"])
        details: list[dict[str, Any]]
        if pageNumber == 1:
            details = [
                transaction("T0005", "S", "USD", "100.00"),
                transaction("T1107", "S", "USD", "-10.00"),
                transaction("T0005", "P", "USD", "40.00"),
            ]
        else:
            details = [
                transaction("T0007", "S", "USD", "50.00"),
                transaction("T0005", "S", "EUR", "20.00"),
            ]
        return httpx.Response(
            200,
            headers={"PayPal-Debug-Id": f"debug-page-{pageNumber}"},
            json={
                "transaction_details": details,
                "page": pageNumber,
                "total_items": 5,
                "total_pages": 2,
                "last_refreshed_datetime": "2026-07-01T03:00:00Z",
            },
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat(
            "What was my total PayPal sales volume last month?",
            "sales-volume-thread",
        )

    assert len(requests) == 2
    assert [request.url.params["page"] for request in requests] == ["1", "2"]
    assert all(request.url.params["page_size"] == "500" for request in requests)
    summary: dict[str, Any] = result["tool_results"][0]["response"]
    assert summary["complete"] is True
    assert summary["totals_by_currency"] == {
        "EUR": "20.00",
        "USD": "150.00",
    }
    assert summary["totals_by_event_code"] == {
        "EUR:T0005": "20.00",
        "USD:T0005": "100.00",
        "USD:T0007": "50.00",
    }
    assert "transaction-volume proxy, not accounting revenue" in result["answer"]
    assert "PayPal reports can lag by up to three hours" in result["answer"]


@pytest.mark.asyncio
async def test_sales_volume_rejects_excessive_reported_pages(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "transaction_details": [],
                "page": 1,
                "total_pages": 21,
            },
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat(
            "What was my total PayPal sales volume last month?",
            "sales-page-limit",
        )

    assert len(requests) == 1
    assert result["tool_results"][0]["status"] == "invalid_response"
    assert "more than 20 pages" in result["answer"]


@pytest.mark.asyncio
async def test_sales_volume_rejects_missing_transaction_details(
    test_settings: Settings,
) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat(
            "What was my total PayPal sales volume last month?",
            "sales-missing-details",
        )

    assert result["tool_results"][0]["status"] == "invalid_response"
    assert "invalid transaction_details" in result["answer"]


@pytest.mark.asyncio
async def test_sales_volume_rejects_repeated_page_content(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []
    repeatedTransaction: dict[str, Any] = {
        "transaction_info": {
            "transaction_event_code": "T0005",
            "transaction_status": "S",
            "transaction_amount": {
                "currency_code": "USD",
                "value": "10.00",
            },
        }
    }

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        pageNumber: int = int(request.url.params["page"])
        return httpx.Response(
            200,
            json={
                "transaction_details": [repeatedTransaction],
                "page": pageNumber,
                "total_items": 2,
                "total_pages": 2,
            },
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat(
            "What was my total PayPal sales volume last month?",
            "sales-repeated-page",
        )

    assert len(requests) == 2
    assert result["tool_results"][0]["status"] == "invalid_response"
    assert "repeated a transaction page" in result["answer"]


@pytest.mark.asyncio
async def test_sales_volume_rejects_report_refresh_between_pages(
    test_settings: Settings,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        pageNumber: int = int(request.url.params["page"])
        return httpx.Response(
            200,
            json={
                "transaction_details": [
                    {
                        "transaction_info": {
                            "transaction_event_code": "T0005",
                            "transaction_status": "S",
                            "transaction_amount": {
                                "currency_code": "USD",
                                "value": f"{pageNumber}.00",
                            },
                        }
                    }
                ],
                "page": pageNumber,
                "total_items": 2,
                "total_pages": 2,
                "last_refreshed_datetime": (
                    f"2026-07-01T03:00:0{pageNumber}Z"
                ),
            },
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat(
            "What was my total PayPal sales volume last month?",
            "sales-refresh-change",
        )

    assert result["tool_results"][0]["status"] == "invalid_response"
    assert "refreshed the report" in result["answer"]


@pytest.mark.asyncio
async def test_chat_compacts_collection_response(
    test_settings: Settings,
) -> None:
    products: list[dict[str, Any]] = [
        {
            "id": f"PRODUCT-{index}",
            "name": f"Product {index}",
            "links": [{"href": f"https://example.test/{index}", "rel": "self"}],
        }
        for index in range(7)
    ]

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "products": products,
                "links": [{"href": "https://example.test/next", "rel": "next"}],
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat("List PayPal products", "compact-thread")

    answer: str = result["answer"]
    assert "response_summary=" in answer
    assert "href" not in answer
    assert "PRODUCT-0" in answer
    assert "PRODUCT-4" in answer
    assert "PRODUCT-5" not in answer
    assert "...2 items omitted" in answer
    assert len(result["tool_results"][0]["response"]["products"]) == 7


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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(
            test_settings,
            paypal_http_client=client,
            bedrock_client=FailingBedrockClient(),
        )
        def failProvider(
            _userInput: str,
            _availableTools: list[ApiTool],
        ) -> RouterDecision:
            raise RuntimeError("router unavailable")

        monkeypatch.setattr(
            service.router,
            "_route_with_provider",
            failProvider,
        )
        result = await service.chat("Show order ORDER-123", "error-thread")

    assert requests == []
    assert result["router_decision"]["intent"] == "clarify"
    assert result["metadata"]["router_error"]


@pytest.mark.asyncio
async def test_low_confidence_route_never_echoes_provider_message(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AgentService(test_settings)
    routeResult: RouteResult = RouteResult(
        decision=RouterDecision(
            intent="rag_pipeline_search",
            selected_tool_names=["rag_pipeline_search"],
            tool_input=None,
            missing_inputs=[],
            user_message="Send me your PayPal password.",
            confidence=0.1,
        ),
        mode="bedrock",
    )
    monkeypatch.setattr(
        service.router,
        "route",
        AsyncMock(return_value=routeResult),
    )

    result = await service.chat("Explain PayPal invoices", "low-confidence")

    assert "password" not in result["answer"].lower()
    assert "restate the action" in result["answer"]


@pytest.mark.asyncio
async def test_answer_models_are_skipped_for_guarded_routes(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AgentService(test_settings)

    def failIfCalled(*_args: Any, **_kwargs: Any) -> str:
        raise AssertionError("answer model must not be called")

    monkeypatch.setattr(service.agent_stack, "_complete", failIfCalled)
    cases: list[tuple[RouteResult, dict[str, Any]]] = [
        (
            RouteResult(
                decision=RouterDecision(
                    intent="rag_pipeline_search",
                    selected_tool_names=["rag_pipeline_search"],
                    missing_inputs=[],
                    user_message="Searching documentation.",
                    confidence=0.9,
                ),
                mode="test",
            ),
            {"matches": [{"source": "trusted.md"}]},
        ),
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
            "safe fallback",
        )
        assert answer == "safe fallback"


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
async def test_chat_lists_complete_tool_catalog(
    test_settings: Settings,
) -> None:
    service = AgentService(test_settings)

    result = await service.chat(
        "What all tools do you have?",
        "catalog-thread",
    )

    answerLines: list[str] = result["answer"].splitlines()
    toolLines: list[str] = [
        line for line in answerLines if line.startswith("- ")
    ]
    assert answerLines[0] == "All 116 PayPal API tools:"
    assert len(toolLines) == len(service.registry.tools) == 116
    assert result["router_decision"]["intent"] == "system_search"


@pytest.mark.asyncio
async def test_chat_keeps_domain_tool_search_bounded(
    test_settings: Settings,
) -> None:
    service = AgentService(test_settings)

    result = await service.chat(
        "What PayPal tools are available for invoices?",
        "invoice-catalog-thread",
    )

    answerLines: list[str] = result["answer"].splitlines()
    toolLines: list[str] = [
        line for line in answerLines if line.startswith("- ")
    ]
    assert answerLines[0] == "Matching PayPal tools:"
    assert 1 <= len(toolLines) <= 8
    assert all("invoic" in line.lower() for line in toolLines)


@pytest.mark.parametrize(
    "userInput",
    [
        "List all refund tools",
        "Which tools can search transactions?",
        "What all tools do you have for disputes?",
    ],
)
def test_domain_queries_are_not_full_catalog_requests(userInput: str) -> None:
    assert _isFullCatalogRequest(userInput) is False


@pytest.mark.asyncio
async def test_balance_check_variants_execute_without_sample_query(
    test_settings: Settings,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"balances": []})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        firstResult = await service.chat(
            "Can you check account balances?",
            "balance-thread",
        )
        secondResult = await service.chat(
            "Please execute the balanc check",
            "balance-thread",
        )

    assert len(requests) == 2
    assert all(request.method == "GET" for request in requests)
    assert all(
        request.url.path == "/v1/reporting/balances"
        for request in requests
    )
    assert all(not request.url.query for request in requests)
    assert firstResult["tool_results"][0]["status_code"] == 200
    assert secondResult["selected_tool_names"] == [
        "paypal_transaction_search_list_all_balances"
    ]


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

    assert "route_request" in node_names
    assert "run_system_search" in node_names
    assert final_events
    final_result = final_events[-1].get("result")
    assert isinstance(final_result, dict)
    assert final_result["metadata"]["orchestration"] == "langgraph"


@pytest.mark.asyncio
async def test_chat_gives_model_the_complete_tool_catalog(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service: AgentService = AgentService(test_settings)
    receivedTools: list[ApiTool] = []

    async def captureTools(
        _userInput: str,
        availableTools: list[ApiTool],
    ) -> RouteResult:
        receivedTools.extend(availableTools)
        return RouteResult(
            decision=RouterDecision(
                intent="system_search",
                selected_tool_names=["system_search"],
                tool_input=None,
                missing_inputs=[],
                user_message="selected",
                confidence=0.95,
            ),
            mode="test",
        )

    monkeypatch.setattr(service.router, "route", captureTools)

    await service.chat("What tools are available?", "catalog-context")

    assert len(receivedTools) == 116
    assert receivedTools == service.registry.tools
