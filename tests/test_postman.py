from __future__ import annotations

from pathlib import Path

from paypal_agent.postman import load_postman_tools


def test_loads_public_paypal_postman_collection(collection_path: Path) -> None:
    tools = load_postman_tools(collection_path)

    assert len(tools) == 116
    assert len({tool.tool_name for tool in tools}) == len(tools)
    assert any(tool.tool_name == "paypal_orders_create_order" for tool in tools)
    assert any(
        tool.tool_name == "paypal_invoices_invoices_send_invoice"
        for tool in tools
    )


def test_extracts_path_variables(collection_path: Path) -> None:
    tools = load_postman_tools(collection_path)
    order_details = next(
        tool
        for tool in tools
        if tool.tool_name == "paypal_orders_show_order_details"
    )

    assert order_details.path == "/v2/checkout/orders/{order_id}"
    assert order_details.path_variables == ("order_id",)
