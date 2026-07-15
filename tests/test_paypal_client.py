from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

import httpx
import pytest
from pydantic import SecretStr, ValidationError

import paypal_agent.paypal_client as paypal_client_module
from paypal_agent.config import Settings
from paypal_agent.paypal_client import ClientInputError, PayPalClient, ToolCallInput
from paypal_agent.postman import ApiTool, BodyMode, load_postman_tools


def _tool(
    *,
    method: str = "GET",
    path: str = "/v1/test",
    bodyMode: BodyMode | None = None,
    bodyTemplate: Any = None,
    headers: dict[str, str] | None = None,
    queryParams: dict[str, str] | None = None,
    pathVariables: tuple[str, ...] = (),
    authType: str | None = "bearer",
    authTokenVariable: str | None = "access_token",
    multipartFileFields: tuple[str, ...] = (),
    multipartContentTypes: dict[str, str] | None = None,
) -> ApiTool:
    return ApiTool(
        tool_name="paypal_test",
        display_name="Test",
        folder_path="Tests",
        method=method,
        raw_url="{{base_url}}" + path,
        path=path,
        description="",
        headers=headers or {},
        query_params=queryParams or {},
        path_variables=pathVariables,
        auth_type=authType,
        auth_token_variable=authTokenVariable,
        body_mode=bodyMode,
        body_template=bodyTemplate,
        multipart_file_fields=multipartFileFields,
        multipart_content_types=multipartContentTypes or {},
    )


def _mutation_settings(testSettings: Settings, **updates: Any) -> Settings:
    return testSettings.model_copy(update={"paypal_allow_mutations": True, **updates})


@pytest.mark.asyncio
async def test_execute_get_sends_real_request_shape(
    collection_path: Path,
    test_settings: Settings,
) -> None:
    tools = load_postman_tools(collection_path)
    tool = next(
        item for item in tools if item.tool_name == "paypal_orders_show_order_details"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url).endswith("/v2/checkout/orders/ORDER-123")
        assert request.headers["authorization"] == "Bearer token"
        return httpx.Response(
            200,
            headers={"PayPal-Debug-Id": "debug-123"},
            json={"id": "ORDER-123", "nested": {"status": "COMPLETED"}},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        result = await paypalClient.execute(
            tool,
            ToolCallInput(pathParams={"order_id": "ORDER-123"}),
        )

    assert result["status"] == "success"
    assert result["paypal_debug_id"] == "debug-123"
    assert result["response"] == {
        "id": "ORDER-123",
        "nested": {"status": "COMPLETED"},
    }
    assert result["request"]["headers"]["Authorization"] == "***"


@pytest.mark.asyncio
async def test_missing_or_blank_path_param_fails_before_http(
    collection_path: Path,
    test_settings: Settings,
) -> None:
    tool = next(
        item
        for item in load_postman_tools(collection_path)
        if item.tool_name == "paypal_orders_show_order_details"
    )
    paypalClient = PayPalClient(test_settings)

    with pytest.raises(ClientInputError, match="Missing.*order_id"):
        await paypalClient.execute(tool, ToolCallInput())
    with pytest.raises(ClientInputError, match="Blank.*order_id"):
        await paypalClient.execute(
            tool,
            ToolCallInput(pathParams={"order_id": "  "}),
        )


@pytest.mark.parametrize(
    ("payload", "location"),
    [
        (ToolCallInput(query={"field": "{{missing}}"}), "query"),
        (ToolCallInput(body={"field": "{{missing}}"}), "body"),
        (ToolCallInput(headers={"X-Test": "{{missing}}"}), "headers"),
    ],
)
@pytest.mark.asyncio
async def test_unresolved_placeholders_fail_before_http(
    test_settings: Settings,
    payload: ToolCallInput,
    location: str,
) -> None:
    requestCount = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal requestCount
        requestCount += 1
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        with pytest.raises(
            ClientInputError,
            match=f"Unresolved variable.*{location}",
        ):
            await paypalClient.execute(_tool(), payload)

    assert requestCount == 0


@pytest.mark.asyncio
async def test_mutation_requires_confirmation_and_exact_body(
    collection_path: Path,
    test_settings: Settings,
) -> None:
    tool = next(
        item
        for item in load_postman_tools(collection_path)
        if item.tool_name == "paypal_orders_create_order"
    )
    paypalClient = PayPalClient(test_settings)

    result = await paypalClient.execute(tool, ToolCallInput(confirm=True))

    assert result["status"] == "requires_confirmation"

    enabledClient = PayPalClient(_mutation_settings(test_settings))
    with pytest.raises(ClientInputError, match="exact production body"):
        await enabledClient.execute(tool, ToolCallInput(confirm=True))


@pytest.mark.asyncio
async def test_raw_multipart_related_tool_is_rejected_before_http(
    collection_path: Path,
    test_settings: Settings,
) -> None:
    tool = next(
        item
        for item in load_postman_tools(collection_path)
        if item.display_name == "Appeal dispute"
    )
    requestCount = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal requestCount
        requestCount += 1
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        with pytest.raises(
            ClientInputError,
            match="multipart/related request encoding is not supported",
        ):
            await paypalClient.execute(
                tool,
                ToolCallInput(
                    pathParams={"dispute_id": "PP-D-1"},
                    body={"evidences": []},
                    confirm=True,
                ),
            )

    assert requestCount == 0


def test_tool_input_rejects_extra_fields_and_reserved_headers() -> None:
    with pytest.raises(ValidationError, match="extra_forbidden"):
        ToolCallInput.model_validate({"unexpected": True})
    for headerName in (
        "Authorization",
        "host",
        "CONTENT-LENGTH",
        "Content-Type",
    ):
        with pytest.raises(ValidationError, match="Reserved request headers"):
            ToolCallInput(headers={headerName: "unsafe"})


@pytest.mark.asyncio
async def test_ignores_postman_sample_query_values(
    test_settings: Settings,
) -> None:
    tool = _tool(queryParams={"sample": "must-not-be-sent"})

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.query == b"requested=value"
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        await paypalClient.execute(
            tool,
            ToolCallInput(query={"requested": "value"}),
        )


@pytest.mark.asyncio
async def test_applies_safe_user_info_schema(
    collection_path: Path,
    test_settings: Settings,
) -> None:
    tool = next(
        item
        for item in load_postman_tools(collection_path)
        if item.tool_name == "paypal_authorization_user_info"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["schema"] == "paypalv1.1"
        assert len(request.url.params) == 1
        return httpx.Response(200, json={"user_id": "USER-1"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        result = await paypalClient.execute(tool, ToolCallInput())

    assert result["request"]["query"] == {"schema": "paypalv1.1"}


@pytest.mark.asyncio
async def test_rejects_unsupported_user_info_schema_before_http(
    collection_path: Path,
    test_settings: Settings,
) -> None:
    tool = next(
        item
        for item in load_postman_tools(collection_path)
        if item.tool_name == "paypal_authorization_user_info"
    )
    requestCount = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal requestCount
        requestCount += 1
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        with pytest.raises(
            ClientInputError,
            match="schema must be paypalv1.1",
        ):
            await paypalClient.execute(
                tool,
                ToolCallInput(query={"schema": "unsupported"}),
            )

    assert requestCount == 0


@pytest.mark.parametrize(
    ("toolName", "parameterName"),
    [
        (
            "paypal_payment_method_tokens_vault_payment_source_"
            "payment_token_list_all_payment_tokens_for_customer",
            "customer_id",
        ),
        (
            "paypal_onboarding_limited_release_manage_accounts_"
            "search_managed_account_through_external_id",
            "external_id",
        ),
    ],
)
@pytest.mark.asyncio
async def test_requires_variable_backed_query_before_http(
    collection_path: Path,
    test_settings: Settings,
    toolName: str,
    parameterName: str,
) -> None:
    tool = next(
        item
        for item in load_postman_tools(collection_path)
        if item.tool_name == toolName
    )
    requestCount = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal requestCount
        requestCount += 1
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        with pytest.raises(
            ClientInputError,
            match=f"Missing required query parameter: {parameterName}",
        ):
            await paypalClient.execute(tool, ToolCallInput())
        with pytest.raises(
            ClientInputError,
            match=f"Missing required query parameter: {parameterName}",
        ):
            await paypalClient.execute(
                tool,
                ToolCallInput(query={parameterName: "  "}),
            )

    assert requestCount == 0


@pytest.mark.asyncio
async def test_transaction_query_normalizes_dates_and_bounds_page(
    test_settings: Settings,
) -> None:
    tool = _tool(path="/v1/reporting/transactions")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["start_date"] == "2026-06-01T00:00:00Z"
        assert request.url.params["end_date"] == "2026-06-30T23:59:59Z"
        assert request.url.params["page"] == "1"
        assert request.url.params["page_size"] == "500"
        return httpx.Response(200, json={"transaction_details": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        result = await paypalClient.execute(
            tool,
            ToolCallInput(
                query={
                    "start_date": "2026-06-01",
                    "end_date": "2026-06-30",
                    "page": 0,
                    "page_size": 1_000,
                }
            ),
        )

    assert result["request"]["query"]["page_size"] == 500


@pytest.mark.asyncio
async def test_transaction_query_requires_valid_31_day_range(
    test_settings: Settings,
) -> None:
    tool = _tool(path="/v1/reporting/transactions")
    paypalClient = PayPalClient(test_settings)

    with pytest.raises(ClientInputError, match="start_date"):
        await paypalClient.execute(tool, ToolCallInput())
    with pytest.raises(ClientInputError, match="31 days"):
        await paypalClient.execute(
            tool,
            ToolCallInput(
                query={
                    "start_date": "2026-01-01T00:00:00Z",
                    "end_date": "2026-02-02T00:00:00Z",
                }
            ),
        )


@pytest.mark.asyncio
async def test_subscription_transactions_require_ordered_rfc3339_range(
    test_settings: Settings,
) -> None:
    tool = _tool(
        path=("/v1/billing/subscriptions/{subscription_id}/transactions"),
        pathVariables=("subscription_id",),
    )
    paypalClient = PayPalClient(test_settings)
    pathParams = {"subscription_id": "I-SUBSCRIPTION"}

    with pytest.raises(ClientInputError, match="start_time"):
        await paypalClient.execute(
            tool,
            ToolCallInput(pathParams=pathParams),
        )
    with pytest.raises(ClientInputError, match="RFC3339"):
        await paypalClient.execute(
            tool,
            ToolCallInput(
                pathParams=pathParams,
                query={
                    "start_time": "2026-01-01",
                    "end_time": "2026-02-01T00:00:00Z",
                },
            ),
        )
    with pytest.raises(ClientInputError, match="before start_time"):
        await paypalClient.execute(
            tool,
            ToolCallInput(
                pathParams=pathParams,
                query={
                    "start_time": "2026-02-01T00:00:00Z",
                    "end_time": "2026-01-01T00:00:00Z",
                },
            ),
        )


@pytest.mark.asyncio
async def test_subscription_transaction_range_can_exceed_31_days(
    test_settings: Settings,
) -> None:
    tool = _tool(
        path=("/v1/billing/subscriptions/{subscription_id}/transactions"),
        pathVariables=("subscription_id",),
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["start_time"] == "2026-01-01T00:00:00Z"
        assert request.url.params["end_time"] == "2026-06-01T00:00:00Z"
        return httpx.Response(200, json={"transactions": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        result = await paypalClient.execute(
            tool,
            ToolCallInput(
                pathParams={"subscription_id": "I-SUBSCRIPTION"},
                query={
                    "start_time": "2026-01-01T00:00:00Z",
                    "end_time": "2026-06-01T00:00:00Z",
                },
            ),
        )

    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_raw_json_and_urlencoded_body_modes(
    test_settings: Settings,
) -> None:
    requestBodies: list[tuple[str, bytes, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requestBodies.append(
            (
                request.url.path,
                request.content,
                request.headers["content-type"],
            )
        )
        return httpx.Response(200, json={})

    settings = _mutation_settings(test_settings)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        await paypalClient.execute(
            _tool(method="POST", path="/json", bodyMode="raw"),
            ToolCallInput(body={"amount": 10}, confirm=True),
        )
        await paypalClient.execute(
            _tool(method="POST", path="/form", bodyMode="urlencoded"),
            ToolCallInput(body={"grant_type": "client_credentials"}, confirm=True),
        )

    assert json.loads(requestBodies[0][1]) == {"amount": 10}
    assert requestBodies[0][2].startswith("application/json")
    assert parse_qs(requestBodies[1][1].decode()) == {
        "grant_type": ["client_credentials"]
    }
    assert requestBodies[1][2].startswith("application/x-www-form-urlencoded")


@pytest.mark.asyncio
async def test_multipart_upload_is_confined_and_closed(
    test_settings: Settings,
    tmp_path: Path,
) -> None:
    uploadRoot = tmp_path / "uploads"
    uploadRoot.mkdir()
    uploadFile = uploadRoot / "evidence.txt"
    uploadFile.write_text("evidence", encoding="utf-8")
    settings = _mutation_settings(
        test_settings,
        paypal_upload_root=uploadRoot,
    )
    tool = _tool(
        method="POST",
        bodyMode="formdata",
        multipartFileFields=("evidence",),
        multipartContentTypes={"metadata": "application/json"},
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["content-type"].startswith("multipart/form-data;")
        assert b"evidence.txt" in request.content
        assert b"evidence" in request.content
        assert b"application/json" in request.content
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        await paypalClient.execute(
            tool,
            ToolCallInput(
                body={
                    "evidence": "evidence.txt",
                    "metadata": {"case": "CASE-1"},
                },
                confirm=True,
            ),
        )

    assert uploadFile.read_text(encoding="utf-8") == "evidence"


@pytest.mark.asyncio
async def test_multipart_rejects_unconfigured_or_outside_paths(
    test_settings: Settings,
    tmp_path: Path,
) -> None:
    outsideFile = tmp_path / "outside.txt"
    outsideFile.write_text("private", encoding="utf-8")
    uploadRoot = tmp_path / "uploads"
    uploadRoot.mkdir()
    tool = _tool(
        method="POST",
        bodyMode="formdata",
        multipartFileFields=("file",),
    )

    with pytest.raises(ClientInputError, match="PAYPAL_UPLOAD_ROOT"):
        await PayPalClient(_mutation_settings(test_settings)).execute(
            tool,
            ToolCallInput(body={"file": outsideFile}, confirm=True),
        )

    settings = _mutation_settings(
        test_settings,
        paypal_upload_root=uploadRoot,
    )
    with pytest.raises(ClientInputError, match="outside"):
        await PayPalClient(settings).execute(
            tool,
            ToolCallInput(body={"file": outsideFile}, confirm=True),
        )


@pytest.mark.asyncio
async def test_missing_multipart_file_fails_before_oauth_http(
    test_settings: Settings,
) -> None:
    settings = _mutation_settings(
        test_settings,
        paypal_access_token=None,
        paypal_client_id="client-id",
        paypal_client_secret=SecretStr("client-secret"),
    )
    requestCount = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal requestCount
        requestCount += 1
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        with pytest.raises(ClientInputError, match="Missing multipart.*evidence"):
            await paypalClient.execute(
                _tool(
                    method="POST",
                    bodyMode="formdata",
                    multipartFileFields=("evidence",),
                ),
                ToolCallInput(
                    body={"metadata": {"case": "CASE-1"}},
                    confirm=True,
                ),
            )

    assert requestCount == 0


@pytest.mark.asyncio
async def test_oauth_401_refreshes_once_and_caches_token() -> None:
    settings = Settings(
        paypal_access_token=None,
        paypal_client_id="client-id",
        paypal_client_secret=SecretStr("client-secret"),
    )
    counts: dict[str, int] = {"oauth": 0, "api": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/oauth2/token":
            counts["oauth"] += 1
            return httpx.Response(
                200,
                json={
                    "access_token": f"token-{counts['oauth']}",
                    "expires_in": 3_600,
                },
            )
        counts["api"] += 1
        if request.headers["authorization"] == "Bearer token-1":
            return httpx.Response(401, json={"name": "AUTHENTICATION_FAILURE"})
        return httpx.Response(
            200,
            headers={"PayPal-Debug-Id": "debug-final"},
            json={"details": {"complete": True}},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        firstResult = await paypalClient.execute(_tool(), ToolCallInput())
        secondResult = await paypalClient.execute(_tool(), ToolCallInput())

    assert counts == {"oauth": 2, "api": 3}
    assert firstResult["paypal_debug_id"] == "debug-final"
    assert firstResult["response"] == {"details": {"complete": True}}
    assert secondResult["status"] == "success"


@pytest.mark.asyncio
async def test_static_access_token_401_is_not_retried() -> None:
    settings = Settings(
        paypal_access_token=SecretStr("static-token"),
        paypal_client_id="client-id",
        paypal_client_secret=SecretStr("client-secret"),
    )
    requestPaths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requestPaths.append(request.url.path)
        return httpx.Response(
            401,
            headers={"PayPal-Debug-Id": "debug-static"},
            json={"name": "AUTHENTICATION_FAILURE"},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        result = await paypalClient.execute(_tool(), ToolCallInput())

    assert requestPaths == ["/v1/test"]
    assert result["status"] == "error"
    assert result["paypal_debug_id"] == "debug-static"
    assert "PAYPAL_ACCESS_TOKEN was rejected" in result["message"]
    assert "Static tokens are never refreshed" in result["message"]


@pytest.mark.asyncio
async def test_noauth_401_never_adds_or_refreshes_bearer_token() -> None:
    settings = Settings(
        paypal_access_token=None,
        paypal_client_id="client-id",
        paypal_client_secret=SecretStr("client-secret"),
    )
    requestPaths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requestPaths.append(request.url.path)
        assert "authorization" not in request.headers
        return httpx.Response(401, json={"name": "AUTHENTICATION_FAILURE"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        result = await paypalClient.execute(
            _tool(authType="noauth", authTokenVariable=None),
            ToolCallInput(),
        )

    assert requestPaths == ["/v1/test"]
    assert result["status"] == "error"


@pytest.mark.asyncio
async def test_mutation_retry_reuses_generated_request_id() -> None:
    settings = Settings(
        paypal_access_token=None,
        paypal_client_id="client-id",
        paypal_client_secret=SecretStr("client-secret"),
        paypal_allow_mutations=True,
    )
    requestIds: list[str] = []
    oauthCount = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal oauthCount
        if request.url.path == "/v1/oauth2/token":
            oauthCount += 1
            return httpx.Response(
                200,
                json={
                    "access_token": f"token-{oauthCount}",
                    "expires_in": 3_600,
                },
            )
        requestIds.append(request.headers["paypal-request-id"])
        if len(requestIds) == 1:
            return httpx.Response(401, json={})
        return httpx.Response(201, json={"id": "ORDER-1"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        result = await paypalClient.execute(
            _tool(
                method="POST",
                bodyMode="raw",
                headers={
                    "PayPal-Request-Id": "postman-value",
                    "X-Request-Source": "postman",
                },
            ),
            ToolCallInput(
                body={"intent": "CAPTURE"},
                headers={
                    "paypal-request-id": "  ",
                    "x-request-source": "caller",
                },
                confirm=True,
            ),
        )

    assert result["status"] == "success"
    assert len(requestIds) == 2
    assert requestIds[0] == requestIds[1]
    assert str(uuid.UUID(requestIds[0])) == requestIds[0]
    resultHeaders = result["request"]["headers"]
    assert resultHeaders["x-request-source"] == "caller"
    assert sum(key.lower() == "paypal-request-id" for key in resultHeaders) == 1


@pytest.mark.asyncio
async def test_read_only_tool_drops_idempotency_header(
    test_settings: Settings,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "paypal-request-id" not in request.headers
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(test_settings, http_client=client)
        await paypalClient.execute(
            _tool(headers={"PayPal-Request-Id": "postman-value"}),
            ToolCallInput(headers={"paypal-request-id": "caller-value"}),
        )


@pytest.mark.asyncio
async def test_oauth_lock_prevents_duplicate_concurrent_tokens() -> None:
    settings = Settings(
        paypal_access_token=None,
        paypal_client_id="client-id",
        paypal_client_secret=SecretStr("client-secret"),
    )
    oauthCount = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal oauthCount
        if request.url.path == "/v1/oauth2/token":
            oauthCount += 1
            return httpx.Response(
                200,
                json={"access_token": "shared-token", "expires_in": 3_600},
            )
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        await asyncio.gather(
            *(paypalClient.execute(_tool(), ToolCallInput()) for _ in range(5))
        )

    assert oauthCount == 1


@pytest.mark.asyncio
async def test_oauth_expires_using_monotonic_clock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock: dict[str, float] = {"now": 100.0}
    monkeypatch.setattr(
        paypal_client_module.time,
        "monotonic",
        lambda: clock["now"],
    )
    settings = Settings(
        paypal_access_token=None,
        paypal_client_id="client-id",
        paypal_client_secret=SecretStr("client-secret"),
    )
    oauthCount = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal oauthCount
        if request.url.path == "/v1/oauth2/token":
            oauthCount += 1
            return httpx.Response(
                200,
                json={
                    "access_token": f"token-{oauthCount}",
                    "expires_in": 100,
                },
            )
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        await paypalClient.execute(_tool(), ToolCallInput())
        clock["now"] = 191.0
        await paypalClient.execute(_tool(), ToolCallInput())

    assert oauthCount == 2


@pytest.mark.asyncio
async def test_managed_tool_never_uses_standard_credentials(
    test_settings: Settings,
) -> None:
    managedTool = _tool(authTokenVariable="managed_path_access_token")

    with pytest.raises(ClientInputError, match="PAYPAL_MANAGED"):
        await PayPalClient(test_settings).execute(managedTool, ToolCallInput())

    settings = test_settings.model_copy(
        update={"paypal_managed_access_token": SecretStr("managed-token")}
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer managed-token"
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paypalClient = PayPalClient(settings, http_client=client)
        await paypalClient.execute(managedTool, ToolCallInput())
