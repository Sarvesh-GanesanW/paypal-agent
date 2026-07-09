from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from paypal_agent.paypal_client import ClientInputError, PayPalClient, ToolCallInput
from paypal_agent.postman import load_postman_tools


@pytest.mark.asyncio
async def test_execute_get_sends_real_request_shape(
    collection_path: Path,
    test_settings,
) -> None:
    tools = load_postman_tools(collection_path)
    tool = next(
        item
        for item in tools
        if item.tool_name == "paypal_orders_show_order_details"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url).endswith("/v2/checkout/orders/ORDER-123")
        assert request.headers["authorization"] == "Bearer token"
        return httpx.Response(200, json={"id": "ORDER-123"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypal_client = PayPalClient(test_settings, http_client=client)
        result = await paypal_client.execute(
            tool,
            ToolCallInput(pathParams={"order_id": "ORDER-123"}),
        )

    assert result["status"] == "success"
    assert result["response"]["id"] == "ORDER-123"
    assert result["request"]["headers"]["Authorization"] == "***"


@pytest.mark.asyncio
async def test_missing_path_param_fails_before_http(
    collection_path: Path,
    test_settings,
) -> None:
    tool = next(
        item
        for item in load_postman_tools(collection_path)
        if item.tool_name == "paypal_orders_show_order_details"
    )
    paypal_client = PayPalClient(test_settings)

    with pytest.raises(ClientInputError, match="order_id"):
        await paypal_client.execute(tool, ToolCallInput())


@pytest.mark.asyncio
async def test_mutation_requires_confirmation(
    collection_path: Path,
    test_settings,
) -> None:
    tool = next(
        item
        for item in load_postman_tools(collection_path)
        if item.tool_name == "paypal_orders_create_order"
    )
    paypal_client = PayPalClient(test_settings)

    result = await paypal_client.execute(tool, ToolCallInput(confirm=True))

    assert result["status"] == "requires_confirmation"
