from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from paypal_agent.config import Settings
from paypal_agent.model_router import (
    RouterDecision,
    SmallModelRouter,
    _openaiRouterResponseFormat,
    _previousMonthDates,
    _router_payload,
)
from paypal_agent.postman import ApiTool, load_postman_tools


class FakeBedrockClient:
    def __init__(
        self,
        selected_tool_name: str,
        *,
        tool_input: dict[str, Any] | None,
        user_message: str = "selected",
        missing_inputs: list[str] | None = None,
    ) -> None:
        self.selected_tool_name = selected_tool_name
        self.tool_input = tool_input
        self.user_message = user_message
        self.missing_inputs = missing_inputs or []
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
                                    "missing_inputs": self.missing_inputs,
                                    "user_message": self.user_message,
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


class FakeSupportBedrockClient:
    def __init__(self, intent: str) -> None:
        self.intent: str = intent

    def converse(self, **_kwargs: Any) -> dict[str, Any]:
        return {
            "output": {
                "message": {
                    "content": [
                        {
                            "toolUse": {
                                "name": "route_request",
                                "input": {
                                    "intent": self.intent,
                                    "selected_tool_names": [self.intent],
                                    "tool_input": {
                                        "pathParams": {"ignored": "value"},
                                        "query": {"ignored": "value"},
                                        "body": {"ignored": "value"},
                                        "headers": {"ignored": "value"},
                                    },
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


def _toolByName(tools: list[ApiTool], toolName: str) -> ApiTool:
    return next(tool for tool in tools if tool.tool_name == toolName)


@pytest.mark.asyncio
async def test_small_model_router_uses_bedrock_tool_choice(
    collection_path: Path,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    selectedTool: ApiTool = _toolByName(
        tools,
        "paypal_authorization_user_info",
    )
    fakeClient: FakeBedrockClient = FakeBedrockClient(
        selectedTool.tool_name,
        tool_input={"pathParams": {}, "query": {}, "headers": {}},
    )
    router: SmallModelRouter = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
        ),
        bedrock_client=fakeClient,
    )

    result = await router.route("Show user info", tools)

    assert result.mode == "bedrock"
    assert result.decision.selected_tool_names == [selectedTool.tool_name]
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.query == {"schema": "paypalv1.1"}
    assert fakeClient.last_request is not None
    assert fakeClient.last_request["inferenceConfig"]["temperature"] == 0.0
    assert fakeClient.last_request["inferenceConfig"]["maxTokens"] == 2048
    assert fakeClient.last_request["toolConfig"]["toolChoice"] == {
        "tool": {"name": "route_request"}
    }
    payload: dict[str, Any] = json.loads(
        fakeClient.last_request["messages"][0]["content"][0]["text"]
    )
    assert payload["paypal_tool_count"] == 116
    assert len(payload["paypal_tools"]) == 116


@pytest.mark.parametrize(
    ("userInput", "toolName", "missingInputs", "expectedMessage"),
    [
        (
            "Show order details",
            "paypal_orders_show_order_details",
            ["order_id"],
            "I need order_id before calling PayPal.",
        ),
        (
            "List PayPal transactions",
            "paypal_transaction_search_list_transactions",
            ["start_date", "end_date"],
            "I need start_date and end_date before calling PayPal.",
        ),
    ],
)
@pytest.mark.asyncio
async def test_provider_missing_inputs_replace_echoed_message(
    collection_path: Path,
    userInput: str,
    toolName: str,
    missingInputs: list[str],
    expectedMessage: str,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, toolName)
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={"pathParams": {}, "query": {}, "headers": {}},
            user_message=userInput,
        ),
    )

    result = await router.route(userInput, [selectedTool])

    assert result.error is None
    assert result.decision.missing_inputs == missingInputs
    assert result.decision.user_message == expectedMessage


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
async def test_provider_missing_tool_input_fails_closed(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)[:3]
    fake_client = FakeBedrockClient(tools[2].tool_name, tool_input=None)
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
        ),
        bedrock_client=fake_client,
    )

    result = await router.route("Show user info", tools)

    assert result.error == "Model router unavailable."
    assert result.mode == "bedrock_validation_error"
    assert result.decision.intent == "clarify"
    assert result.decision.selected_tool_names == []


@pytest.mark.asyncio
async def test_provider_protected_header_fails_closed(
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
        ),
        bedrock_client=fake_client,
    )

    result = await router.route("Show user info", tools)

    assert result.error == "Model router unavailable."
    assert result.mode == "bedrock_validation_error"
    assert result.decision.selected_tool_names == []


@pytest.mark.asyncio
async def test_provider_unknown_header_fails_closed(
    collection_path: Path,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    selectedTool: ApiTool = _toolByName(
        tools,
        "paypal_authorization_user_info",
    )
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {},
                "query": {},
                "headers": {"X-Invented": "audit-value"},
            },
        ),
    )

    result = await router.route(
        "Show user info with X-Invented audit-value",
        [selectedTool],
    )

    assert result.error == "Model router unavailable."
    assert result.mode == "bedrock_validation_error"
    assert result.decision.selected_tool_names == []


@pytest.mark.asyncio
async def test_provider_error_does_not_expose_internal_details(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)[:3]
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
        ),
        bedrock_client=FailingBedrockClient(),
    )

    result = await router.route("Show user info", tools)

    assert result.error == "Model router unavailable."
    assert "secret-token" not in result.error
    assert result.mode == "bedrock_error"
    assert result.decision.intent == "clarify"
    assert result.decision.selected_tool_names == []


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
async def test_provider_cannot_invent_sensitive_missing_inputs(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_orders_show_order_details")
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={"pathParams": {}, "query": {}, "headers": {}},
            user_message="Send me your PayPal password.",
            missing_inputs=["your PayPal password"],
        ),
    )

    result = await router.route("Show order details", [selectedTool])

    assert result.decision.missing_inputs == ["order_id"]
    assert result.decision.user_message == (
        "I need order_id before calling PayPal."
    )
    assert "password" not in result.decision.model_dump_json().lower()


@pytest.mark.asyncio
async def test_provider_unknown_query_parameter_fails_closed(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_authorization_user_info")
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
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
    assert result.mode == "bedrock_validation_error"
    assert result.decision.selected_tool_names == []


@pytest.mark.parametrize(
    ("queryName", "queryValue"),
    [("fields", "all"), ("page", 9), ("page_size", 99)],
)
@pytest.mark.asyncio
async def test_provider_ungrounded_list_query_fails_closed(
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
    assert result.mode == "bedrock_validation_error"
    assert result.decision.selected_tool_names == []


@pytest.mark.asyncio
async def test_provider_identifier_substring_is_rebound_from_user_input(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_orders_show_order_details")
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
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

    assert result.error is None
    assert result.mode == "bedrock"
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.path_params == {"order_id": "1234"}


@pytest.mark.asyncio
async def test_provider_path_value_is_overwritten_by_explicit_identifier(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_orders_show_order_details")
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {"order_id": "50"},
                "query": {},
                "headers": {},
            },
        ),
    )

    result = await router.route(
        "Show order SAFE-ORDER-123 after a 50 USD payment",
        [selectedTool],
    )

    assert result.mode == "bedrock"
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.path_params == {
        "order_id": "SAFE-ORDER-123"
    }


@pytest.mark.asyncio
async def test_provider_prefers_latest_identifier_over_pending_context(
    collection_path: Path,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    selectedTool: ApiTool = _toolByName(
        tools,
        "paypal_invoices_invoices_show_invoice_details",
    )
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {"invoice_id": "INV2-NEW"},
                "query": {},
                "headers": {},
            },
        ),
    )
    routingInput: str = (
        "Previous unresolved PayPal request:\n"
        "Send invoice with invoice ID INV2-OLD\n"
        "Latest user message:\n"
        "Show invoice details for invoice ID INV2-NEW"
    )

    result = await router.route(routingInput, [selectedTool])

    assert result.error is None
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.path_params == {
        "invoice_id": "INV2-NEW"
    }


@pytest.mark.parametrize(
    ("userInput", "modelIdentifier"),
    [
        ("What order id do I need?", "do"),
        ("What order id should-I use?", "should-I"),
        ("What order id 2 use?", "2"),
    ],
)
@pytest.mark.asyncio
async def test_provider_does_not_bind_ordinary_word_as_identifier(
    collection_path: Path,
    userInput: str,
    modelIdentifier: str,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    selectedTool: ApiTool = _toolByName(
        tools,
        "paypal_orders_show_order_details",
    )
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {"order_id": modelIdentifier},
                "query": {},
                "headers": {},
            },
        ),
    )

    result = await router.route(
        userInput,
        [selectedTool],
    )

    assert result.error is None
    assert result.decision.missing_inputs == ["order_id"]
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.path_params == {}


@pytest.mark.asyncio
async def test_provider_rejects_numeric_body_substring_match(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_orders_create_order")
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
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
    assert result.mode == "bedrock_validation_error"
    assert result.decision.intent == "clarify"
    assert result.decision.selected_tool_names == []


@pytest.mark.parametrize(
    "body",
    [
        {"invented": {"value": "audit"}},
        {"intent": "CAPTURE", "purchase_units": [{}]},
        {
            "intent": "CAPTURE",
            "purchase_units": [{"invented": "audit"}],
        },
        {"intent": None},
        {"intent": 1234},
    ],
)
@pytest.mark.asyncio
async def test_provider_rejects_invalid_mutation_body_structure(
    collection_path: Path,
    body: dict[str, Any],
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    selectedTool: ApiTool = _toolByName(
        tools,
        "paypal_orders_create_order",
    )
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {},
                "query": {},
                "body": body,
                "headers": {},
            },
        ),
    )

    result = await router.route(
        "Create order with intent CAPTURE and value audit",
        [selectedTool],
    )

    assert result.error == "Model router unavailable."
    assert result.mode == "bedrock_validation_error"
    assert result.decision.selected_tool_names == []


@pytest.mark.asyncio
async def test_provider_allows_explicit_non_sample_nested_body_field(
    collection_path: Path,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    selectedTool: ApiTool = _toolByName(
        tools,
        "paypal_orders_create_order",
    )
    body: dict[str, Any] = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {"currency_code": "USD", "value": "10.00"},
                "custom_id": "audit",
            }
        ],
    }
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "pathParams": {},
                "query": {},
                "body": body,
                "headers": {},
            },
        ),
    )

    result = await router.route(
        "Create order with intent CAPTURE, currency code USD, value 10.00, "
        "and custom ID audit",
        [selectedTool],
    )

    assert result.error is None
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.body == body


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

    payloadText: str = _router_payload("List my transactions", selectedTools)
    payload: dict[str, Any] = json.loads(payloadText)
    toolMetadata: dict[str, dict[str, Any]] = {
        tool["tool_name"]: tool for tool in payload["paypal_tools"]
    }

    transactionTool: dict[str, Any] = toolMetadata[
        "paypal_transaction_search_list_transactions"
    ]
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
    userInfoTool: dict[str, Any] = toolMetadata[
        "paypal_authorization_user_info"
    ]
    assert userInfoTool["fixed_query_parameters"] == {"schema": "paypalv1.1"}
    customerTool: dict[str, Any] = toolMetadata[
        "paypal_payment_method_tokens_vault_payment_source_"
        "payment_token_list_all_payment_tokens_for_customer"
    ]
    assert customerTool["required_query_parameters"] == ["customer_id"]
    externalIdTool: dict[str, Any] = toolMetadata[
        "paypal_onboarding_limited_release_manage_accounts_"
        "search_managed_account_through_external_id"
    ]
    assert externalIdTool["required_query_parameters"] == ["external_id"]
    invoiceTool: dict[str, Any] = toolMetadata[
        "paypal_invoices_invoices_send_invoice"
    ]
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
            "PayPal-Request-Id": "generated-by-application",
            "Proxy-Authorization": "secret",
            "X-Custom": "visible",
        },
    )

    payload: dict[str, Any] = json.loads(
        _router_payload("Test headers", [tool])
    )

    assert payload["paypal_tools"][0]["header_parameters"] == ["X-Custom"]


def test_router_payload_contains_all_116_tools_and_metadata(
    collection_path: Path,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)

    payload: dict[str, Any] = json.loads(
        _router_payload("Check my balance", tools)
    )

    toolMetadata: list[dict[str, Any]] = payload["paypal_tools"]
    assert payload["paypal_tool_count"] == 116
    assert len(toolMetadata) == 116
    assert {tool["tool_name"] for tool in toolMetadata} == {
        tool.tool_name for tool in tools
    }
    assert all(tool["description"] is not None for tool in toolMetadata)
    unsupportedTools: list[dict[str, Any]] = [
        tool for tool in toolMetadata if not tool["is_supported"]
    ]
    assert [tool["tool_name"] for tool in unsupportedTools] == [
        "paypal_disputes_appeal_dispute"
    ]
    assert unsupportedTools[0]["unsupported_reason"]


@pytest.mark.asyncio
async def test_selected_balance_tool_binds_explicit_filters(
    collection_path: Path,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    selectedTool: ApiTool = _toolByName(
        tools,
        "paypal_transaction_search_list_all_balances",
    )
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={"pathParams": {}, "query": {}, "headers": {}},
        ),
    )

    result = await router.route(
        "Show my USD balance as of 2026-07-01 including crypto",
        tools,
    )

    assert result.error is None
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.query == {
        "as_of_time": "2026-07-01T23:59:59Z",
        "currency_code": "USD",
        "include_crypto_currencies": True,
    }


def test_previous_month_dates_use_calendar_boundaries() -> None:
    assert _previousMonthDates(date(2026, 7, 15)) == (
        "2026-06-01T00:00:00Z",
        "2026-06-30T23:59:59Z",
    )


def test_openai_router_uses_json_object_for_free_form_inputs() -> None:
    assert _openaiRouterResponseFormat() == {"type": "json_object"}


@pytest.mark.asyncio
async def test_selected_sales_volume_tool_binds_transaction_dates(
    collection_path: Path,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    selectedTool: ApiTool = _toolByName(
        tools,
        "paypal_transaction_search_list_transactions",
    )
    userInput: str = "What was my total PayPal sales volume last month?"
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={"pathParams": {}, "query": {}, "headers": {}},
        ),
    )

    result = await router.route(userInput, tools)

    assert result.error is None
    assert result.decision.tool_input is not None
    assert result.decision.tool_input.query["start_date"].endswith(
        "-01T00:00:00Z"
    )
    assert result.decision.tool_input.query["end_date"].endswith(
        "T23:59:59Z"
    )


@pytest.mark.asyncio
async def test_sales_volume_rejects_ungrounded_model_filters(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(
        tools,
        "paypal_transaction_search_list_transactions",
    )
    userInput: str = "What was my total PayPal sales volume last month?"
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
        ),
        bedrock_client=FakeBedrockClient(
            selectedTool.tool_name,
            tool_input={
                "query": {
                    "start_date": "2025-06-01T00:00:00Z",
                    "end_date": "2025-06-30T23:59:59Z",
                    "fields": "all",
                }
            },
        ),
    )

    result = await router.route(userInput, [selectedTool])

    assert result.error == "Model router unavailable."
    assert result.mode == "bedrock_validation_error"
    assert result.decision.selected_tool_names == []


@pytest.mark.parametrize(
    ("userInput", "intent"),
    [
        ("How do I create an invoice?", "rag_pipeline_search"),
        ("What tools are available?", "system_search"),
        ("Remember my last invoice request", "memory_find"),
        ("Grep memory for invoice", "memory_grep"),
    ],
)
@pytest.mark.asyncio
async def test_model_selects_support_tools(
    collection_path: Path,
    userInput: str,
    intent: str,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeSupportBedrockClient(intent),
    )

    result = await router.route(userInput, tools)

    assert result.error is None
    assert result.mode == "bedrock"
    assert result.decision.intent == intent
    assert result.decision.selected_tool_names == [intent]
    assert result.decision.tool_input is None


@pytest.mark.asyncio
async def test_clarification_discards_a_model_tool_hint(
    collection_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path)
    )

    def modelClarification(
        _userInput: str,
        _availableTools: list[ApiTool],
    ) -> RouterDecision:
        return RouterDecision(
            intent="clarify",
            selected_tool_names=[
                "paypal_invoices_invoices_create_draft_invoice"
            ],
            tool_input=None,
            missing_inputs=["invoice details"],
            user_message="selected",
            confidence=0.85,
        )

    monkeypatch.setattr(
        router,
        "_route_with_provider",
        modelClarification,
    )

    result = await router.route("Create and send an invoice", tools)

    assert result.error is None
    assert result.mode == "bedrock"
    assert result.decision.intent == "clarify"
    assert result.decision.selected_tool_names == []
    assert result.decision.tool_input is None


@pytest.mark.parametrize(
    "userInput",
    [
        "What all tools do you have?",
        "Please execute the balanc check",
        "Create and send an invoice",
        "Use the invoice tool to list invoices",
    ],
)
@pytest.mark.asyncio
async def test_provider_failure_never_uses_a_selection_fallback(
    collection_path: Path,
    userInput: str,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FailingBedrockClient(),
    )

    result = await router.route(userInput, tools)

    assert result.mode == "bedrock_error"
    assert result.error == "Model router unavailable."
    assert result.decision.intent == "clarify"
    assert result.decision.selected_tool_names == []


@pytest.mark.asyncio
async def test_codex_router_uses_direct_json_without_strict_schema(
    collection_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tools = load_postman_tools(collection_path)
    selectedTool = _toolByName(tools, "paypal_orders_show_order_details")
    capturedPrompt: str = ""
    capturedSchema: dict[str, Any] | None = {"unexpected": True}

    def fakeCompleteWithCodex(
        _settings: Settings,
        prompt: str,
        *,
        schema: dict[str, Any] | None = None,
    ) -> str:
        nonlocal capturedPrompt, capturedSchema
        capturedPrompt = prompt
        capturedSchema = schema
        return json.dumps(
            {
                "intent": "paypal_tool",
                "selected_tool_names": [selectedTool.tool_name],
                "tool_input": {
                    "pathParams": {"order_id": "ORDER-123"},
                    "query": {},
                    "body": None,
                    "headers": {},
                },
                "missing_inputs": [],
                "user_message": "Showing the requested order.",
                "confidence": 0.95,
            }
        )

    monkeypatch.setattr(
        "paypal_agent.model_router.completeWithCodex",
        fakeCompleteWithCodex,
    )
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            model_provider="codex",
        )
    )

    result = await router.route("Show order ORDER-123", tools)

    assert result.error is None
    assert result.mode == "codex"
    assert result.decision.selected_tool_names == [selectedTool.tool_name]
    assert capturedSchema is None
    assert "do not call tools" in capturedPrompt
    assert "selected_tool_names" in capturedPrompt
    assert "intent must be exactly one of" in capturedPrompt
    assert "has_body=false" in capturedPrompt
    assert '"paypal_tool_count":116' in capturedPrompt


@pytest.mark.asyncio
async def test_router_excludes_unsupported_paypal_tool(
    collection_path: Path,
) -> None:
    tools: list[ApiTool] = load_postman_tools(collection_path)
    unsupportedTool: ApiTool = next(
        tool for tool in tools if tool.display_name == "Appeal dispute"
    )
    router: SmallModelRouter = SmallModelRouter(
        Settings(paypal_postman_collection_path=collection_path),
        bedrock_client=FakeBedrockClient(
            unsupportedTool.tool_name,
            tool_input={"pathParams": {}, "query": {}, "headers": {}},
        ),
    )

    result = await router.route(
        "Appeal dispute with dispute id PP-D-123",
        tools,
    )

    assert result.error == "Model router unavailable."
    assert result.mode == "bedrock_validation_error"
    assert result.decision.intent == "clarify"
    assert result.decision.selected_tool_names == []
