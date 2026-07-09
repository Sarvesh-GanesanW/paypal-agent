from __future__ import annotations

import httpx
import pytest

from paypal_agent.agent_service import AgentService
from paypal_agent.config import Settings


@pytest.mark.asyncio
async def test_chat_routes_with_structured_decision(test_settings: Settings) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(404, json={"name": "RESOURCE_NOT_FOUND"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = AgentService(test_settings, paypal_http_client=client)
        result = await service.chat("send an invoice for 50 dollars", "test-thread")


    assert result["metadata"]["router_mode"] == "deterministic"
    assert result["metadata"]["orchestration"] == "langgraph"
    assert result["metadata"]["graph"] == "paypal_agent_chat_graph"
    assert result["router_decision"]["intent"] == "paypal_tool"
    assert "paypal_invoices_invoices_send_invoice" in result["selected_tool_names"]
    assert requests
    assert result["tool_results"][0]["status_code"] == 404


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


    matches = service.memory.find("memory-thread invoice")
    assert matches
    assert matches[0]["event"]["conversation_id"] == "memory-thread"


@pytest.mark.asyncio
async def test_chat_routes_memory_find(test_settings: Settings) -> None:
    service = AgentService(test_settings)
    service.memory.append("chat", {"user_input": "previous invoice request"})

    result = await service.chat("remember invoice", "thread")

    assert result["router_decision"]["intent"] == "memory_find"
    assert result["selected_tool_names"] == ["memory_find"]
    assert "previous invoice request" in result["answer"]


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
