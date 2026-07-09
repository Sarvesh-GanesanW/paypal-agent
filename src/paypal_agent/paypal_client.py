from __future__ import annotations

import base64
import json
import re
from contextlib import AbstractAsyncContextManager
from typing import Any
from urllib.parse import quote

import httpx
from pydantic import BaseModel, Field

from paypal_agent.config import Settings
from paypal_agent.postman import ApiTool

SECRET_HEADERS = {"authorization", "paypal-auth-assertion"}
VARIABLE_PATTERN = re.compile(r"{{([^{}]+)}}")


class ClientInputError(ValueError):
    pass


class ToolCallInput(BaseModel):
    path_params: dict[str, Any] = Field(default_factory=dict, alias="pathParams")
    query: dict[str, Any] = Field(default_factory=dict)
    body: Any = None
    headers: dict[str, str] = Field(default_factory=dict)
    variables: dict[str, Any] = Field(default_factory=dict)
    confirm: bool = False

    model_config = {"populate_by_name": True}


class PayPalClient:
    def __init__(
        self,
        settings: Settings,
        *,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings
        self.http_client = http_client
        self.access_token: str | None = None

    async def execute(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
        *,
        force_request: bool = False,
    ) -> dict[str, Any]:
        if tool.tool_name == "paypal_authorization_generate_access_token":
            await self._get_access_token()
            return {
                "status": "success",
                "status_code": 200,
                "tool": tool.to_dict(),
                "response": {"access_token": "***"},
            }

        if tool.is_mutating and not self._mutation_allowed(payload):
            if force_request:
                return await self._execute_request(
                    tool,
                    payload,
                    force_request=True,
                )
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
        *,
        force_request: bool = False,
    ) -> dict[str, Any]:
        url = self._build_url(tool, payload)
        query = self._build_query(tool, payload)
        headers = await self._build_headers(
            tool,
            payload,
            force_request=force_request,
        )
        body = self._body(tool, payload, force_request=force_request)

        async with self._client() as client:
            response = await client.request(
                tool.method,
                url,
                params=query or None,
                json=body,
                headers=headers,
            )

        response_payload = _response_payload(response)
        return {
            "status": "success" if response.is_success else "error",
            "status_code": response.status_code,
            "tool": tool.to_dict(),
            "request": {
                "method": tool.method,
                "url": url,
                "query": query,
                "headers": _redact_headers(headers),
                "has_body": body is not None,
                "force_request": force_request,
            },
            "response": response_payload,
        }

    def _mutation_allowed(self, payload: ToolCallInput) -> bool:
        return payload.confirm and self.settings.paypal_allow_mutations

    def _build_url(self, tool: ApiTool, payload: ToolCallInput) -> str:
        path = tool.path
        for name in tool.path_variables:
            if name not in payload.path_params:
                raise ClientInputError(f"Missing path parameter: {name}")
            value = quote(str(payload.path_params[name]), safe="")
            path = path.replace("{" + name + "}", value)
        if "{" in path or "}" in path:
            raise ClientInputError(f"Unresolved URL variable in path: {path}")
        return self.settings.paypal_base_url + path

    def _build_query(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
    ) -> dict[str, Any]:
        variables = self._variables(payload)
        query: dict[str, Any] = {}
        for key, value in tool.query_params.items():
            resolved = _replace_variables(value, variables)
            if "{{" not in resolved:
                query[key] = resolved
        query.update(payload.query)
        return query

    async def _build_headers(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
        *,
        force_request: bool = False,
    ) -> dict[str, str]:
        headers: dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        for key, value in tool.headers.items():
            if key.lower() in {"authorization", "content-length", "host"}:
                continue
            resolved = _replace_variables(value, self._variables(payload))
            if "{{" not in resolved:
                headers[key] = resolved
        headers.update(payload.headers)
        headers["Authorization"] = (
            f"Bearer {await self._get_access_token(force_request=force_request)}"
        )
        return headers

    def _body(
        self,
        tool: ApiTool,
        payload: ToolCallInput,
        *,
        force_request: bool = False,
    ) -> Any:
        if payload.body is not None:
            return payload.body
        if tool.is_mutating and tool.body_template is not None and not force_request:
            raise ClientInputError(
                "This mutating tool has a Postman sample body; pass an exact "
                "production body instead of sending the sample."
            )
        return None

    def _variables(self, payload: ToolCallInput) -> dict[str, str]:
        variables = {
            "base_url": self.settings.paypal_base_url,
            **{key: str(value) for key, value in payload.variables.items()},
            **{key: str(value) for key, value in payload.path_params.items()},
        }
        return variables

    async def _get_access_token(self, *, force_request: bool = False) -> str:
        if self.settings.paypal_access_token:
            return self.settings.paypal_access_token.get_secret_value()
        if self.access_token:
            return self.access_token
        if not self.settings.paypal_client_id or not self.settings.paypal_client_secret:
            if force_request:
                return "missing_access_token"
            raise ClientInputError(
                "Set PAYPAL_ACCESS_TOKEN or PAYPAL_CLIENT_ID and "
                "PAYPAL_CLIENT_SECRET."
            )

        credentials = (
            f"{self.settings.paypal_client_id}:"
            f"{self.settings.paypal_client_secret.get_secret_value()}"
        )
        encoded_credentials = base64.b64encode(
            credentials.encode("utf-8")
        ).decode("ascii")
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
            if force_request:
                return "paypal_oauth_failed"
            raise ClientInputError(f"PayPal OAuth failed: {payload}")
        if not isinstance(payload, dict):
            raise ClientInputError("PayPal OAuth response was not a JSON object.")
        access_token = payload.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            raise ClientInputError("PayPal OAuth response did not include a token.")
        self.access_token = access_token
        return access_token

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
