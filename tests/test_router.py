from __future__ import annotations

from pathlib import Path

from paypal_agent.postman import load_postman_tools
from paypal_agent.router import ToolRouter


def test_invoice_request_routes_to_invoice_tools(collection_path: Path) -> None:
    router = ToolRouter(load_postman_tools(collection_path))

    tools = router.search("send an invoice for 50 dollars", limit=5)

    assert any(
        tool.tool_name == "paypal_invoices_invoices_send_invoice" for tool in tools
    )


def test_invoice_capability_search_excludes_unrelated_tools(
    collection_path: Path,
) -> None:
    router = ToolRouter(load_postman_tools(collection_path))

    tools = router.search(
        "What PayPal tools are available for invoices?",
        limit=8,
    )

    assert tools
    assert all("invoice" in tool.search_text for tool in tools)


def test_show_invoice_request_includes_exact_tool(
    collection_path: Path,
) -> None:
    router = ToolRouter(load_postman_tools(collection_path))

    tools = router.search("Show invoice INV2-ABC123", limit=12)

    assert any(
        tool.tool_name == "paypal_invoices_invoices_show_invoice_details"
        for tool in tools
    )


def test_dispute_request_routes_to_dispute_tools(collection_path: Path) -> None:
    router = ToolRouter(load_postman_tools(collection_path))

    tools = router.search("is there an open dispute for this customer", limit=5)

    assert tools
    assert all("dispute" in tool.search_text for tool in tools[:3])


def test_sales_volume_request_routes_to_transaction_search(
    collection_path: Path,
) -> None:
    router = ToolRouter(load_postman_tools(collection_path))

    tools = router.search(
        "What was my total PayPal sales volume last month?",
        limit=1,
    )

    assert [tool.tool_name for tool in tools] == [
        "paypal_transaction_search_list_transactions"
    ]
