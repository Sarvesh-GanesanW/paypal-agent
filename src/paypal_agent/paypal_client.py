from __future__ import annotations

import asyncio
import base64
import json
import re
import time
import uuid
from collections.abc import Mapping
from contextlib import AbstractAsyncContextManager, ExitStack
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, BinaryIO, Literal
from urllib.parse import quote

import httpx
from pydantic import BaseModel, Field, SecretStr, field_validator

from paypal_agent.config import Settings
from paypal_agent.postman import ApiTool

SECRET_HEADERS = {"authorization", "paypal-auth-assertion"}
VARIABLE_PATTERN = re.compile(r"{{([^{}]+)}}")
TOKEN_EXPIRY_SKEW_SECONDS = 30.0
MAX_TRANSACTION_PAGE = 10_000
MAX_TRANSACTION_PAGE_SIZE = 100
SAFE_FIXED_QUERY_PARAMETERS = {
    ("/v1/identity/oauth2/userinfo", "schema"): "paypalv1.1",
}
RESERVED_USER_HEADERS = {
    "authorization",
    "content-length",
    "content-type",
    "host",
}
RFC3339_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

TokenFamily = Literal["standard", "managed"]


class ClientInputError(ValueError):
    pass


class ToolCallInput(BaseModel):
    path_params: dict[str, Any] = Field(default_factory=dict, alias="pathParams")
    query: dict[str, Any] = Field(default_factory=dict)
    body: Any = None
    headers: dict[str, str] = Field(default_factory=dict)
    variables: dict[str, Any] = Field(default_factory=dict)
    confirm: bool = False

    model_config = {"populate_by_name": True, "extra": "forbid"}

    @field_validator("headers")
    @classmethod
    def reject_reserved_headers(cls, headers: dict[str, str]) -> dict[str, str]:
        invalid_headers = sorted(
            key for key in headers if key.lower() in RESERVED_USER_HEADERS
        )
        if invalid_headers:
            raise ValueError(
                "Reserved request headers cannot be supplied: "
                + ", ".join(invalid_headers)
            )
        return headers


class PayPalClient:
    def __init__(
        self,
        settings: Settings,
        *,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings
        self.http_client = http_client
        self._access_tokens: dict[TokenFamily, str | None] = {
            "standard": None,
            "managed": None,
        }
        self._access_token_expiries: dict[TokenFamily, float] = {
            "standard": 0.0,
            "managed": 0.0,
        }
        self._token_locks: dict[TokenFamily, asyncio.Lock] = {
            "standard": asyncio.Lock(),
            "managed": asyncio.Lock(),
        }

    async def execute(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
    ) -> dict[str, Any]:
        if tool.unsupported_reason is not None:
            raise ClientInputError(
                f"Unsupported PayPal tool: {tool.unsupported_reason}"
            )

        if tool.tool_name == "paypal_authorization_generate_access_token":
            await self._get_access_token("standard")
            return {
                "status": "success",
                "status_code": 200,
                "tool": tool.to_dict(),
                "response": {"access_token": "***"},
            }

        if tool.is_mutating and not self._mutation_allowed(payload):
            return {
                "status": "requires_confirmation",
                "message": (
                    "Mutating PayPal calls require confirm=true and "
                    "PAYPAL_ALLOW_MUTATIONS=true."
                ),
                "tool": tool.to_dict(),
            }

        return await self._execute_request(tool, payload)

    async def _execute_request(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
    ) -> dict[str, Any]:
        variables = self._variables(tool, payload)
        url = self._build_url(tool, payload)
        query = self._build_query(tool, payload, variables)
        body = self._body(tool, payload, variables)
        _reject_unresolved_placeholders(query, "query")
        _reject_unresolved_placeholders(body, "body")
        self._validate_multipart_body(tool, body)
        headers = await self._build_headers(tool, payload, variables)
        token_family = self._token_family(tool)

        async with self._client() as client:
            response = await self._send_request(
                client,
                tool,
                url,
                query,
                headers,
                body,
            )
            if self._should_retry_unauthorized(
                response,
                tool,
                headers,
                token_family,
            ):
                failed_token = _bearer_token(headers)
                access_token = await self._refresh_access_token(
                    token_family,
                    failed_token,
                )
                _set_header(headers, "Authorization", f"Bearer {access_token}")
                response = await self._send_request(
                    client,
                    tool,
                    url,
                    query,
                    headers,
                    body,
                )

        response_payload = _response_payload(response)
        result: dict[str, Any] = {
            "status": "success" if response.is_success else "error",
            "status_code": response.status_code,
            "paypal_debug_id": response.headers.get("PayPal-Debug-Id"),
            "tool": tool.to_dict(),
            "request": {
                "method": tool.method,
                "url": url,
                "query": query,
                "headers": _redact_headers(headers),
                "has_body": body is not None,
            },
            "response": response_payload,
        }
        if response.status_code == 401 and self._uses_static_token(
            token_family,
            headers,
        ):
            result["message"] = self._static_token_failure_message(token_family)
        return result

    async def _send_request(
        self,
        client: httpx.AsyncClient,
        tool: ApiTool,
        url: str,
        query: dict[str, Any],
        headers: dict[str, str],
        body: Any,
    ) -> httpx.Response:
        if body is None:
            return await client.request(
                tool.method,
                url,
                params=query or None,
                headers=headers,
            )
        if tool.body_mode == "urlencoded":
            return await client.request(
                tool.method,
                url,
                params=query or None,
                data=body,
                headers=headers,
            )
        if tool.body_mode == "formdata":
            with ExitStack() as stack:
                data, files = self._multipart_parts(tool, body, stack)
                return await client.request(
                    tool.method,
                    url,
                    params=query or None,
                    data=data or None,
                    files=files or None,
                    headers=headers,
                )
        return await client.request(
            tool.method,
            url,
            params=query or None,
            json=body,
            headers=headers,
        )

    def _multipart_parts(
        self,
        tool: ApiTool,
        body: Any,
        stack: ExitStack,
    ) -> tuple[dict[str, str], dict[str, Any]]:
        self._validate_multipart_body(tool, body)
        if not isinstance(body, Mapping):
            raise RuntimeError("Validated multipart body was not an object.")

        data: dict[str, str] = {}
        files: dict[str, Any] = {}
        file_fields = set(tool.multipart_file_fields)
        for raw_key, value in body.items():
            key = str(raw_key)
            if key in file_fields:
                path, filename, content_type = _file_specification(
                    key,
                    value,
                    tool.multipart_content_types.get(key),
                    self.settings.paypal_upload_root,
                )
                try:
                    file_handle: BinaryIO = stack.enter_context(path.open("rb"))
                except OSError as error:
                    raise ClientInputError(
                        f"Unable to open multipart file for field: {key}"
                    ) from error
                if content_type:
                    files[key] = (filename, file_handle, content_type)
                else:
                    files[key] = (filename, file_handle)
                continue

            text_value = _form_value(value)
            content_type = tool.multipart_content_types.get(key)
            if content_type:
                files[key] = (None, text_value, content_type)
            else:
                data[key] = text_value
        return data, files

    def _validate_multipart_body(self, tool: ApiTool, body: Any) -> None:
        if tool.body_mode != "formdata":
            return
        if not isinstance(body, Mapping):
            raise ClientInputError("Multipart request body must be an object.")

        normalized_body = {str(key): value for key, value in body.items()}
        missing_fields = sorted(
            set(tool.multipart_file_fields) - normalized_body.keys()
        )
        if missing_fields:
            raise ClientInputError(
                "Missing multipart file field(s): " + ", ".join(missing_fields)
            )
        for field_name in tool.multipart_file_fields:
            _file_specification(
                field_name,
                normalized_body[field_name],
                tool.multipart_content_types.get(field_name),
                self.settings.paypal_upload_root,
            )

    def _mutation_allowed(self, payload: ToolCallInput) -> bool:
        return payload.confirm and self.settings.paypal_allow_mutations

    def _build_url(self, tool: ApiTool, payload: ToolCallInput) -> str:
        path = tool.path
        for name in tool.path_variables:
            if name not in payload.path_params:
                raise ClientInputError(f"Missing path parameter: {name}")
            raw_value = payload.path_params[name]
            if raw_value is None or not str(raw_value).strip():
                raise ClientInputError(f"Blank path parameter: {name}")
            if "{{" in str(raw_value) or "}}" in str(raw_value):
                raise ClientInputError(f"Unresolved path parameter: {name}")
            value = quote(str(raw_value), safe="")
            path = path.replace("{" + name + "}", value)
        if "{" in path or "}" in path:
            raise ClientInputError(f"Unresolved URL variable in path: {path}")
        return self.settings.paypal_base_url + path

    def _build_query(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
        variables: dict[str, str],
    ) -> dict[str, Any]:
        query: dict[str, Any] = {
            key: _resolve_value(value, variables)
            for key, value in payload.query.items()
        }
        for key, value in tool.query_params.items():
            fixed_value = SAFE_FIXED_QUERY_PARAMETERS.get((tool.path, key))
            if fixed_value is not None and value == fixed_value:
                if key in query and query[key] != fixed_value:
                    raise ClientInputError(
                        f"{key} must be {fixed_value} for this PayPal tool."
                    )
                query[key] = fixed_value
                continue
            if key in query:
                query_value = query[key]
                if VARIABLE_PATTERN.fullmatch(value) and (
                    query_value is None or not str(query_value).strip()
                ):
                    raise ClientInputError(f"Missing required query parameter: {key}")
                continue
            if VARIABLE_PATTERN.fullmatch(value):
                resolved = _replace_variables(value, variables)
                if VARIABLE_PATTERN.search(resolved) or not resolved.strip():
                    raise ClientInputError(f"Missing required query parameter: {key}")
                query[key] = resolved
        if tool.path == "/v1/reporting/transactions":
            _validate_transaction_query(query)
        if tool.path == ("/v1/billing/subscriptions/{subscription_id}/transactions"):
            _validate_subscription_transaction_query(query)
        return query

    async def _build_headers(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
        variables: dict[str, str],
    ) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        for key, value in tool.headers.items():
            if key.lower() in {"authorization", "content-length", "host"}:
                continue
            resolved = _replace_variables(value, variables)
            if "{{" not in resolved:
                _set_header(headers, key, resolved)
        for key, value in payload.headers.items():
            _set_header(headers, key, _replace_variables(value, variables))
        if tool.body_mode == "formdata":
            _remove_header(headers, "Content-Type")

        request_id = _header_value(headers, "PayPal-Request-Id")
        if tool.method == "POST":
            if request_id is None or not request_id.strip():
                _set_header(headers, "PayPal-Request-Id", variables["$guid"])
        else:
            _remove_header(headers, "PayPal-Request-Id")

        _reject_unresolved_placeholders(headers, "headers")

        if _header_value(headers, "Authorization") is not None:
            return headers
        if tool.auth_type == "noauth":
            return headers
        if tool.auth_type not in {None, "bearer"}:
            raise ClientInputError(
                f"Unsupported Postman authentication type: {tool.auth_type}"
            )
        token_family = self._token_family(tool)
        access_token = await self._get_access_token(token_family)
        _set_header(headers, "Authorization", f"Bearer {access_token}")
        return headers

    def _body(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
        variables: dict[str, str],
    ) -> Any:
        if payload.body is not None:
            return _resolve_value(payload.body, variables)
        if tool.is_mutating and tool.body_template is not None:
            raise ClientInputError(
                "This mutating tool has a Postman sample body; pass an exact "
                "production body instead of sending the sample."
            )
        return None

    def _variables(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
    ) -> dict[str, str]:
        return {
            **tool.collection_variables,
            **{
                key: str(value)
                for key, value in payload.variables.items()
                if value is not None
            },
            **{key: str(value) for key, value in payload.path_params.items()},
            "$guid": str(uuid.uuid4()),
            "base_url": self.settings.paypal_base_url,
        }

    def _token_family(self, tool: ApiTool) -> TokenFamily:
        token_variable = tool.auth_token_variable
        if token_variable in {None, "access_token"}:
            return "standard"
        if token_variable == "managed_path_access_token":
            return "managed"
        raise ClientInputError(
            f"Unsupported PayPal access token variable: {token_variable}"
        )

    async def _get_access_token(self, family: TokenFamily) -> str:
        if self._cached_token_is_valid(family):
            return self._required_cached_token(family)

        static_token = self._static_access_token(family)
        if static_token is not None:
            return static_token.get_secret_value()
        self._require_client_credentials(family)

        async with self._token_locks[family]:
            if self._cached_token_is_valid(family):
                return self._required_cached_token(family)
            return await self._request_access_token(family)

    async def _refresh_access_token(
        self,
        family: TokenFamily,
        failed_token: str | None,
    ) -> str:
        self._require_client_credentials(family)
        async with self._token_locks[family]:
            cached_token = self._access_tokens[family]
            if (
                cached_token is not None
                and cached_token != failed_token
                and self._cached_token_is_valid(family)
            ):
                return cached_token
            self._access_tokens[family] = None
            self._access_token_expiries[family] = 0.0
            return await self._request_access_token(family)

    async def _request_access_token(self, family: TokenFamily) -> str:
        client_id, client_secret = self._require_client_credentials(family)
        credentials = f"{client_id}:{client_secret.get_secret_value()}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "ascii"
        )
        async with self._client() as client:
            response = await client.post(
                self.settings.paypal_base_url + "/v1/oauth2/token",
                data={"grant_type": "client_credentials"},
                headers={
                    "Authorization": f"Basic {encoded_credentials}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
        payload = _response_payload(response)
        if not response.is_success:
            debug_id = response.headers.get("PayPal-Debug-Id")
            raise ClientInputError(
                f"PayPal OAuth failed (PayPal-Debug-Id={debug_id}): {payload}"
            )
        if not isinstance(payload, dict):
            raise ClientInputError("PayPal OAuth response was not a JSON object.")
        access_token = payload.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            raise ClientInputError("PayPal OAuth response did not include a token.")
        expires_in = payload.get("expires_in")
        if (
            isinstance(expires_in, bool)
            or not isinstance(expires_in, (int, float))
            or expires_in <= 0
        ):
            raise ClientInputError(
                "PayPal OAuth response did not include a valid expires_in."
            )
        expiry_skew = min(TOKEN_EXPIRY_SKEW_SECONDS, float(expires_in) / 10)
        self._access_tokens[family] = access_token
        self._access_token_expiries[family] = (
            time.monotonic() + float(expires_in) - expiry_skew
        )
        return access_token

    def _cached_token_is_valid(self, family: TokenFamily) -> bool:
        return (
            self._access_tokens[family] is not None
            and time.monotonic() < self._access_token_expiries[family]
        )

    def _required_cached_token(self, family: TokenFamily) -> str:
        access_token = self._access_tokens[family]
        if access_token is None:
            raise RuntimeError("Cached access token unexpectedly missing.")
        return access_token

    def _static_access_token(self, family: TokenFamily) -> SecretStr | None:
        if family == "managed":
            return self.settings.paypal_managed_access_token
        return self.settings.paypal_access_token

    def _require_client_credentials(
        self,
        family: TokenFamily,
    ) -> tuple[str, SecretStr]:
        if family == "managed":
            client_id = self.settings.paypal_managed_client_id
            client_secret = self.settings.paypal_managed_client_secret
            setting_names = (
                "PAYPAL_MANAGED_ACCESS_TOKEN or PAYPAL_MANAGED_CLIENT_ID and "
                "PAYPAL_MANAGED_CLIENT_SECRET"
            )
        else:
            client_id = self.settings.paypal_client_id
            client_secret = self.settings.paypal_client_secret
            setting_names = (
                "PAYPAL_ACCESS_TOKEN or PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET"
            )
        if not client_id or client_secret is None:
            raise ClientInputError(f"Set {setting_names}.")
        return client_id, client_secret

    def _can_refresh(self, family: TokenFamily) -> bool:
        if family == "managed":
            return bool(
                self.settings.paypal_managed_client_id
                and self.settings.paypal_managed_client_secret
            )
        return bool(
            self.settings.paypal_client_id and self.settings.paypal_client_secret
        )

    def _should_retry_unauthorized(
        self,
        response: httpx.Response,
        tool: ApiTool,
        headers: dict[str, str],
        family: TokenFamily,
    ) -> bool:
        if (
            response.status_code != 401
            or tool.auth_type == "noauth"
            or not self._can_refresh(family)
        ):
            return False
        if self._uses_static_token(family, headers):
            return False
        if not tool.is_mutating:
            return True
        return _header_value(headers, "PayPal-Request-Id") is not None

    def _uses_static_token(
        self,
        family: TokenFamily,
        headers: Mapping[str, str],
    ) -> bool:
        static_token = self._static_access_token(family)
        return (
            static_token is not None
            and _bearer_token(headers) == static_token.get_secret_value()
        )

    def _static_token_failure_message(self, family: TokenFamily) -> str:
        if family == "managed":
            token_name = "PAYPAL_MANAGED_ACCESS_TOKEN"
            credential_names = (
                "PAYPAL_MANAGED_CLIENT_ID and PAYPAL_MANAGED_CLIENT_SECRET"
            )
        else:
            token_name = "PAYPAL_ACCESS_TOKEN"
            credential_names = "PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET"
        return (
            f"{token_name} was rejected by PayPal. Static tokens are never "
            f"refreshed; replace it, or remove it and set {credential_names}."
        )

    def _client(self) -> AbstractAsyncContextManager[httpx.AsyncClient]:
        if self.http_client:
            return BorrowedAsyncClient(self.http_client)
        return httpx.AsyncClient(timeout=self.settings.request_timeout_seconds)


class BorrowedAsyncClient(AbstractAsyncContextManager[httpx.AsyncClient]):
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def __aenter__(self) -> httpx.AsyncClient:
        return self.client

    async def __aexit__(self, *args: object) -> None:
        return None


def _replace_variables(value: str, variables: dict[str, str]) -> str:
    return VARIABLE_PATTERN.sub(
        lambda match: variables.get(match.group(1), match.group(0)),
        value,
    )


def _resolve_value(value: Any, variables: dict[str, str]) -> Any:
    if isinstance(value, str):
        return _replace_variables(value, variables)
    if isinstance(value, dict):
        return {key: _resolve_value(item, variables) for key, item in value.items()}
    if isinstance(value, list):
        return [_resolve_value(item, variables) for item in value]
    return value


def _reject_unresolved_placeholders(value: Any, location: str) -> None:
    if _has_unresolved_placeholder(value):
        raise ClientInputError(
            f"Unresolved variable placeholder in request {location}."
        )


def _has_unresolved_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return "{{" in value or "}}" in value
    if isinstance(value, Mapping):
        return any(
            _has_unresolved_placeholder(key) or _has_unresolved_placeholder(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple, set)):
        return any(_has_unresolved_placeholder(item) for item in value)
    return False


def _response_payload(response: httpx.Response) -> Any:
    if not response.content:
        return None
    content_type = response.headers.get("content-type", "")
    if "json" not in content_type:
        return response.text
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text


def _redact_headers(headers: dict[str, str]) -> dict[str, str]:
    return {
        key: "***" if key.lower() in SECRET_HEADERS else value
        for key, value in headers.items()
    }


def _header_value(headers: Mapping[str, str], name: str) -> str | None:
    normalized_name = name.lower()
    return next(
        (value for key, value in headers.items() if key.lower() == normalized_name),
        None,
    )


def _set_header(headers: dict[str, str], name: str, value: str) -> None:
    _remove_header(headers, name)
    headers[name] = value


def _remove_header(headers: dict[str, str], name: str) -> None:
    normalized_name = name.lower()
    for key in tuple(headers):
        if key.lower() == normalized_name:
            del headers[key]


def _bearer_token(headers: Mapping[str, str]) -> str | None:
    authorization = _header_value(headers, "Authorization")
    if authorization is None or not authorization.lower().startswith("bearer "):
        return None
    return authorization[7:]


def _file_specification(
    field_name: str,
    value: Any,
    default_content_type: str | None,
    upload_root: Path | None,
) -> tuple[Path, str, str | None]:
    if isinstance(value, Mapping):
        path_value = value.get("path", value.get("src"))
        filename_value = value.get("filename")
        content_type_value = value.get(
            "content_type",
            value.get("contentType", default_content_type),
        )
    else:
        path_value = value
        filename_value = None
        content_type_value = default_content_type
    if not isinstance(path_value, (str, Path)):
        raise ClientInputError(
            f"Multipart file field '{field_name}' requires a file path."
        )
    if upload_root is None:
        raise ClientInputError("Set PAYPAL_UPLOAD_ROOT before sending multipart files.")
    resolved_root = upload_root.expanduser().resolve()
    candidate_path = Path(path_value).expanduser()
    if not candidate_path.is_absolute():
        candidate_path = resolved_root / candidate_path
    try:
        path = candidate_path.resolve(strict=True)
    except OSError as error:
        raise ClientInputError(
            f"Multipart file for field '{field_name}' does not exist."
        ) from error
    if not path.is_relative_to(resolved_root):
        raise ClientInputError(
            f"Multipart file for field '{field_name}' is outside PAYPAL_UPLOAD_ROOT."
        )
    filename = str(filename_value) if filename_value else path.name
    content_type = (
        str(content_type_value) if content_type_value else default_content_type
    )
    return path, filename, content_type


def _form_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def _validate_transaction_query(query: dict[str, Any]) -> None:
    start_date, end_date = _required_time_range(
        query,
        "start_date",
        "end_date",
        normalize_dates=True,
    )
    if end_date - start_date > timedelta(days=31):
        raise ClientInputError("PayPal transaction searches cannot exceed 31 days.")
    query["page"] = _clamped_integer(
        query.get("page", 1),
        "page",
        1,
        MAX_TRANSACTION_PAGE,
    )
    query["page_size"] = _clamped_integer(
        query.get("page_size", MAX_TRANSACTION_PAGE_SIZE),
        "page_size",
        1,
        MAX_TRANSACTION_PAGE_SIZE,
    )


def _validate_subscription_transaction_query(query: dict[str, Any]) -> None:
    _required_time_range(
        query,
        "start_time",
        "end_time",
        normalize_dates=False,
    )


def _required_time_range(
    query: dict[str, Any],
    start_name: str,
    end_name: str,
    *,
    normalize_dates: bool,
) -> tuple[datetime, datetime]:
    start_time = _required_rfc3339(
        query,
        start_name,
        is_end=False,
        normalize_date=normalize_dates,
    )
    end_time = _required_rfc3339(
        query,
        end_name,
        is_end=True,
        normalize_date=normalize_dates,
    )
    if end_time < start_time:
        raise ClientInputError(f"{end_name} must not be before {start_name}.")
    return start_time, end_time


def _required_rfc3339(
    query: dict[str, Any],
    name: str,
    *,
    is_end: bool,
    normalize_date: bool,
) -> datetime:
    value = query.get(name)
    if not isinstance(value, str):
        raise ClientInputError(f"{name} must be an RFC3339 timestamp.")
    if normalize_date and DATE_PATTERN.fullmatch(value):
        value += "T23:59:59Z" if is_end else "T00:00:00Z"
        query[name] = value
    if not RFC3339_PATTERN.fullmatch(value):
        raise ClientInputError(f"{name} must be an RFC3339 timestamp.")
    normalized_value = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(normalized_value)
    except ValueError as error:
        raise ClientInputError(f"{name} must be an RFC3339 timestamp.") from error


def _clamped_integer(
    value: Any,
    name: str,
    minimum: int,
    maximum: int,
) -> int:
    if isinstance(value, bool):
        raise ClientInputError(f"{name} must be an integer.")
    if isinstance(value, float) and not value.is_integer():
        raise ClientInputError(f"{name} must be an integer.")
    try:
        integer_value = int(value)
    except (TypeError, ValueError) as error:
        raise ClientInputError(f"{name} must be an integer.") from error
    return min(max(integer_value, minimum), maximum)
