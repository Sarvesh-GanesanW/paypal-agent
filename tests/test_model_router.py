from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from paypal_agent.config import Settings
from paypal_agent.model_router import (
    RouterDecision,
    SmallModelRouter,
    _fallback_decision,
    _router_payload,
)
from paypal_agent.postman import ApiTool, load_postman_tools


class FakeBedrockClient:
    def __init__(
        self,
        selected_tool_name: str,
        *,
        tool_input: dict[str, Any] | None,
    ) -> None:
        self.selected_tool_name = selected_tool_name
        self.tool_input = tool_input
        self.last_request: dict[str, Any] | None = None

    def converse(self, **kwargs: Any) -> dict[str, Any]:
        self.last_request = kwargs
        return {
            "output": {
                "message": {
                    "content": [
                        {
                            "toolUse": {
                                "name": "route_request",
                                "input": {
                                    "intent": "paypal_tool",
                                    "selected_tool_names": [self.selected_tool_name],
                                    "tool_input": self.tool_input,
                                    "missing_inputs": [],
                                    "user_message": "selected",
                                    "confidence": 0.9,
                                },
                            }
                        }
                    ]
                }
            }
        }


class FailingBedrockClient:
    def converse(self, **_kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("provider failed with secret-token")


def _toolByName(tools: list[ApiTool], toolName: str) -> ApiTool:
    return next(tool for tool in tools if tool.tool_name == toolName)


@pytest.mark.asyncio
async def test_small_model_router_uses_bedrock_tool_choice(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)[:3]
    selectedTool = tools[2]
    fake_client = FakeBedrockClient(
        selectedTool.tool_name,
        tool_input={"pathParams": {}, "query": {}, "headers": {}},
    )
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            bedrock_router_enabled=True,
            model_router_enabled=True,
        ),
        bedrock_client=fake_client,
    )

    result = await router.route("Show user info", tools)

    assert result.mode == "bedrock"
    assert result.decision.selected_tool_names == [selectedTool.tool_name]
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.query == {"schema": "paypalv1.1"}
    assert fake_client.last_request is not None
    assert fake_client.last_request["inferenceConfig"]["temperature"] == 0.0
    assert fake_client.last_request["toolConfig"]["toolChoice"] == {
        "tool": {"name": "route_request"}
    }


def test_router_decision_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        RouterDecision.model_validate(
            {
                "intent": "clarify",
                "selected_tool_names": [],
                "missing_inputs": ["action"],
                "user_message": "clarify",
                "confidence": 0.2,
                "extra": "nope",
            }
        )


def test_router_decision_rejects_multiple_tools() -> None:
    with pytest.raises(ValidationError):
        RouterDecision.model_validate(
            {
                "intent": "paypal_tool",
                "selected_tool_names": ["first", "second"],
                "tool_input": {"pathParams": {}},
                "missing_inputs": [],
                "user_message": "ambiguous",
                "confidence": 0.8,
            }
        )


@pytest.mark.asyncio
async def test_provider_missing_tool_input_returns_safe_clarification(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)[:3]
    fake_client = FakeBedrockClient(tools[2].tool_name, tool_input=None)
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=fake_client,
    )

    result = await router.route("Show user info", tools)

    assert result.error is not None
    assert result.decision.intent == "clarify"
    assert result.decision.selected_tool_names == []


@pytest.mark.asyncio
async def test_provider_protected_header_returns_safe_clarification(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)[:3]
    fake_client = FakeBedrockClient(
        tools[2].tool_name,
        tool_input={
            "pathParams": {},
            "headers": {"Authorization": "Bearer invented"},
        },
    )
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=fake_client,
    )

    result = await router.route("Show user info", tools)

    assert result.error is not None
    assert result.decision.intent == "clarify"


@pytest.mark.asyncio
async def test_provider_error_does_not_expose_internal_details(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)[:3]
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=FailingBedrockClient(),
    )

    result = await router.route("Show user info", tools)

    assert result.error == "Model router unavailable."
    assert "secret-token" not in result.error


@pytest.mark.asyncio
async def test_provider_binds_required_customer_id_from_user_input(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(
        tools,
        "paypal_payment_method_tokens_vault_payment_source_"
        "payment_token_list_all_payment_tokens_for_customer",
    )
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={"pathParams": {}, "query": {}, "headers": {}},
        ),
    )

    result = await router.route(
        "List all payment tokens for customer id customer-blue",
        [selectedTool],
    )

    assert result.error is None
    assert result.decision.missing_inputs == []
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.query == {"customer_id": "customer-blue"}


@pytest.mark.asyncio
async def test_provider_gates_missing_required_customer_id(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(
        tools,
        "paypal_payment_method_tokens_vault_payment_source_"
        "payment_token_list_all_payment_tokens_for_customer",
    )
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={"pathParams": {}, "query": {}, "headers": {}},
        ),
    )

    result = await router.route(
        "List all payment tokens for customer",
        [selectedTool],
    )

    assert result.error is None
    assert result.decision.missing_inputs == ["customer_id"]


@pytest.mark.asyncio
async def test_provider_rejects_unknown_query_parameter(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_authorization_user_info")
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {},
                "query": {"invented": "value"},
                "headers": {},
            },
        ),
    )

    result = await router.route("Show user info", [selectedTool])

    assert result.error == "Model router unavailable."
    assert result.decision.intent == "clarify"


@pytest.mark.parametrize(
    ("queryName", "queryValue"),
    [("fields", "all"), ("page", 9), ("page_size", 99)],
)
@pytest.mark.asyncio
async def test_provider_rejects_ungrounded_list_query_value(
    collection_path: Path,
    queryName: str,
    queryValue: str | int,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(
        tools,
        "paypal_invoices_invoices_list_invoices",
    )
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {},
                "query": {queryName: queryValue},
                "headers": {},
            },
        ),
    )

    result = await router.route("List invoices", [selectedTool])

    assert result.error == "Model router unavailable."
    assert result.decision.intent == "clarify"


@pytest.mark.asyncio
async def test_provider_rejects_identifier_substring_match(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_orders_show_order_details")
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {"order_id": "123"},
                "query": {},
                "headers": {},
            },
        ),
    )

    result = await router.route(
        "Show order details for order id 1234",
        [selectedTool],
    )

    assert result.error == "Model router unavailable."
    assert result.decision.intent == "clarify"


@pytest.mark.asyncio
async def test_provider_rejects_numeric_body_substring_match(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_orders_create_order")
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=True,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {},
                "query": {},
                "body": {"amount": 9},
                "headers": {},
            },
        ),
    )

    result = await router.route("Create order for amount 79.99", [selectedTool])

    assert result.error == "Model router unavailable."
    assert result.decision.intent == "clarify"


def test_router_payload_exposes_parameter_names_without_sample_values(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTools = [
        tool
        for tool in tools
        if tool.tool_name
        in {
            "paypal_authorization_user_info",
            "paypal_invoices_invoices_send_invoice",
            (
                "paypal_onboarding_limited_release_manage_accounts_"
                "search_managed_account_through_external_id"
            ),
            (
                "paypal_payment_method_tokens_vault_payment_source_"
                "payment_token_list_all_payment_tokens_for_customer"
            ),
            "paypal_transaction_search_list_transactions",
        }
    ]

    payloadText = _router_payload("List my transactions", selectedTools)
    payload = json.loads(payloadText)
    candidates = {
        candidate["tool_name"]: candidate
        for candidate in payload["candidate_paypal_tools"]
    }

    transactionTool = candidates["paypal_transaction_search_list_transactions"]
    assert transactionTool["query_parameters"] == [
        "fields",
        "start_date",
        "end_date",
    ]
    assert transactionTool["required_query_parameters"] == [
        "start_date",
        "end_date",
    ]
    assert transactionTool["fixed_query_parameters"] == {}
    assert transactionTool["server_query_parameters"] == ["page", "page_size"]
    userInfoTool = candidates["paypal_authorization_user_info"]
    assert userInfoTool["fixed_query_parameters"] == {"schema": "paypalv1.1"}
    customerTool = candidates[
        "paypal_payment_method_tokens_vault_payment_source_"
        "payment_token_list_all_payment_tokens_for_customer"
    ]
    assert customerTool["required_query_parameters"] == ["customer_id"]
    externalIdTool = candidates[
        "paypal_onboarding_limited_release_manage_accounts_"
        "search_managed_account_through_external_id"
    ]
    assert externalIdTool["required_query_parameters"] == ["external_id"]
    invoiceTool = candidates["paypal_invoices_invoices_send_invoice"]
    assert "subject" in invoiceTool["body_fields"]
    assert "2025-02-20" not in payloadText
    assert "recipient_cc1@example.com" not in payloadText


def test_router_payload_excludes_protected_headers() -> None:
    tool = ApiTool(
        tool_name="header_test",
        display_name="Header test",
        folder_path="Test",
        method="GET",
        raw_url="{{base_url}}/test",
        path="/test",
        description="Test protected header metadata.",
        headers={
            "Authorization": "secret",
            "Content-Length": "1",
            "Content-Type": "application/json",
            "Host": "example.test",
            "PayPal-Auth-Assertion": "secret",
            "Proxy-Authorization": "secret",
            "X-Custom": "visible",
        },
    )

    payload = json.loads(_router_payload("Test headers", [tool]))

    assert payload["candidate_paypal_tools"][0]["header_parameters"] == ["X-Custom"]


@pytest.mark.parametrize(
    ("userInput", "toolName"),
    [
        (
            "show order status for order id 5O190127TN364715T",
            "paypal_orders_show_order_details",
        ),
        (
            "show refund request with refund id RF123456",
            "paypal_payments_show_refund_details",
        ),
        (
            "last transactions from 2026-01-01 to 2026-01-02",
            "paypal_transaction_search_list_transactions",
        ),
    ],
)
def test_business_request_terms_route_to_paypal(
    collection_path: Path,
    userInput: str,
    toolName: str,
) -> None:
    tools = load_postman_tools(collection_path)

    decision = _fallback_decision(userInput, tools)

    assert decision.intent == "paypal_tool"
    assert decision.selected_tool_names == [toolName]
    assert decision.missing_inputs == []


@pytest.mark.parametrize(
    "userInput",
    [
        "show available tools",
        "show last requests",
        "show recent requests",
        "system status",
    ],
)
def test_explicit_system_request_still_routes_to_system(
    collection_path: Path,
    userInput: str,
) -> None:
    tools = load_postman_tools(collection_path)

    decision = _fallback_decision(userInput, tools)

    assert decision.intent == "system_search"
    assert decision.selected_tool_names == ["system_search"]


@pytest.mark.parametrize(
    ("userInput", "toolName", "expectedQuery"),
    [
        (
            "Show user info",
            "paypal_authorization_user_info",
            {"schema": "paypalv1.1"},
        ),
        (
            "List all payment tokens for customer id customer-blue",
            (
                "paypal_payment_method_tokens_vault_payment_source_"
                "payment_token_list_all_payment_tokens_for_customer"
            ),
            {"customer_id": "customer-blue"},
        ),
        (
            "Search managed account through external id external-blue",
            (
                "paypal_onboarding_limited_release_manage_accounts_"
                "search_managed_account_through_external_id"
            ),
            {"external_id": "external-blue"},
        ),
    ],
)
def test_deterministic_router_binds_query_contract(
    collection_path: Path,
    userInput: str,
    toolName: str,
    expectedQuery: dict[str, str],
) -> None:
    tools = load_postman_tools(collection_path)

    decision = _fallback_decision(userInput, tools)

    assert decision.selected_tool_names == [toolName]
    assert decision.missing_inputs == []
    assert decision.tool_input is not None
    assert decision.tool_input.query == expectedQuery


@pytest.mark.parametrize(
    ("userInput", "missingInput"),
    [
        ("List all payment tokens for customer", "customer_id"),
        ("Search managed account through external id", "external_id"),
    ],
)
def test_deterministic_router_gates_missing_required_query_input(
    collection_path: Path,
    userInput: str,
    missingInput: str,
) -> None:
    tools = load_postman_tools(collection_path)

    decision = _fallback_decision(userInput, tools)

    assert decision.intent == "paypal_tool"
    assert decision.missing_inputs == [missingInput]


@pytest.mark.asyncio
async def test_router_excludes_unsupported_paypal_tool(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    unsupportedTool = next(
        tool for tool in tools if tool.display_name == "Appeal dispute"
    )
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_router_enabled=False,
        )
    )

    result = await router.route(
        "Appeal dispute with dispute id PP-D-123",
        [unsupportedTool],
    )

    assert result.decision.intent == "clarify"
    assert result.decision.selected_tool_names == []
