from __future__ import annotations

from pathlib import Path

from paypal_agent.postman import load_postman_tools


def test_loads_public_paypal_postman_collection(collection_path: Path) -> None:
    tools = load_postman_tools(collection_path)

    assert len(tools) == 116
    assert len({tool.tool_name for tool in tools}) == len(tools)
    assert any(tool.tool_name == "paypal_orders_create_order" for tool in tools)
    assert any(
        tool.tool_name == "paypal_invoices_invoices_send_invoice" for tool in tools
    )


def test_extracts_path_variables(collection_path: Path) -> None:
    tools = load_postman_tools(collection_path)
    order_details = next(
        tool for tool in tools if tool.tool_name == "paypal_orders_show_order_details"
    )

    assert order_details.path == "/v2/checkout/orders/{order_id}"
    assert order_details.path_variables == ("order_id",)


def test_extracts_body_modes_and_multipart_metadata(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    create_order = next(
        tool for tool in tools if tool.tool_name == "paypal_orders_create_order"
    )
    generate_token = next(
        tool
        for tool in tools
        if tool.tool_name == "paypal_authorization_generate_access_token"
    )
    provide_evidence = next(
        tool
        for tool in tools
        if tool.display_name == "Provide evidence" and tool.body_mode == "formdata"
    )

    assert create_order.body_mode == "raw"
    assert generate_token.body_mode == "urlencoded"
    assert provide_evidence.multipart_file_fields == ("evidence-file",)
    assert provide_evidence.multipart_content_types["input"] == "application/json"


def test_marks_raw_multipart_related_tool_unsupported(
    collection_path: Path,
) -> None:
    appeal_dispute = next(
        tool
        for tool in load_postman_tools(collection_path)
        if tool.display_name == "Appeal dispute"
    )

    assert appeal_dispute.body_mode == "raw"
    assert appeal_dispute.unsupported_reason == (
        "multipart/related request encoding is not supported."
    )
    assert appeal_dispute.to_dict()["is_supported"] is False


def test_inherits_auth_without_loading_public_credentials(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    order_details = next(
        tool for tool in tools if tool.tool_name == "paypal_orders_show_order_details"
    )
    managed_tools = [tool for tool in tools if "/Manage Accounts" in tool.folder_path]

    assert order_details.auth_type == "bearer"
    assert order_details.auth_token_variable == "access_token"
    assert order_details.collection_variables["order_intent"] == "CAPTURE"
    assert "client_id" not in order_details.collection_variables
    assert "client_secret" not in order_details.collection_variables
    assert "managed_path_client_id" not in order_details.collection_variables
    assert "managed_path_client_secret" not in order_details.collection_variables
    assert managed_tools
    assert all(
        tool.auth_token_variable == "managed_path_access_token"
        for tool in managed_tools
    )
