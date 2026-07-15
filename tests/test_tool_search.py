from __future__ import annotations

from pathlib import Path

import pytest

from paypal_agent.postman import ApiTool, load_postman_tools
from paypal_agent.tool_search import ToolCatalogSearch


def test_invoice_catalog_search_finds_invoice_tools(
    collection_path: Path,
) -> None:
    search: ToolCatalogSearch = ToolCatalogSearch(
        load_postman_tools(collection_path)
    )

    tools: list[ApiTool] = search.search(
        "send an invoice for 50 dollars",
        limit=5,
    )

    assert any(
        tool.tool_name == "paypal_invoices_invoices_send_invoice"
        for tool in tools
    )


def test_invoice_catalog_search_excludes_unrelated_tools(
    collection_path: Path,
) -> None:
    search: ToolCatalogSearch = ToolCatalogSearch(
        load_postman_tools(collection_path)
    )

    tools: list[ApiTool] = search.search(
        "What PayPal tools are available for invoices?",
        limit=8,
    )

    assert tools
    assert all("invoice" in tool.search_text for tool in tools)


def test_catalog_search_finds_exact_invoice_tool(
    collection_path: Path,
) -> None:
    search: ToolCatalogSearch = ToolCatalogSearch(
        load_postman_tools(collection_path)
    )

    tools: list[ApiTool] = search.search(
        "Show invoice INV2-ABC123",
        limit=12,
    )

    assert any(
        tool.tool_name == "paypal_invoices_invoices_show_invoice_details"
        for tool in tools
    )


def test_dispute_catalog_search_finds_dispute_tools(
    collection_path: Path,
) -> None:
    search: ToolCatalogSearch = ToolCatalogSearch(
        load_postman_tools(collection_path)
    )

    tools: list[ApiTool] = search.search(
        "is there an open dispute for this customer",
        limit=5,
    )

    assert tools
    assert all("dispute" in tool.search_text for tool in tools[:3])


@pytest.mark.parametrize(
    "query",
    [
        "Can you check account balances?",
        "Please execute the balance check",
        "Please execute the balanc check",
    ],
)
def test_balance_catalog_search_finds_balance_tool(
    collection_path: Path,
    query: str,
) -> None:
    search: ToolCatalogSearch = ToolCatalogSearch(
        load_postman_tools(collection_path)
    )

    tools: list[ApiTool] = search.search(query, limit=1)

    assert [tool.tool_name for tool in tools] == [
        "paypal_transaction_search_list_all_balances"
    ]
