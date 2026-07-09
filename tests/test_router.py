from __future__ import annotations

from pathlib import Path

from paypal_agent.postman import load_postman_tools
from paypal_agent.router import ToolRouter


def test_invoice_request_routes_to_invoice_tools(collection_path: Path) -> None:
    router = ToolRouter(load_postman_tools(collection_path))

    tools = router.search("send an invoice for 50 dollars", limit=5)

    assert any(
        tool.tool_name == "paypal_invoices_invoices_send_invoice"
        for tool in tools
    )


def test_dispute_request_routes_to_dispute_tools(collection_path: Path) -> None:
    router = ToolRouter(load_postman_tools(collection_path))

    tools = router.search("is there an open dispute for this customer", limit=5)

    assert tools
    assert all("dispute" in tool.search_text for tool in tools[:3])
