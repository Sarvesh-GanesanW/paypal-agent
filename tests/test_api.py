from __future__ import annotations

from typing import Any
from uuid import UUID

import httpx
import pytest
from fastapi.testclient import TestClient

from paypal_agent.api import app, service
from paypal_agent.paypal_client import ToolCallInput


def test_health_and_catalog_endpoints() -> None:
    client = TestClient(app)
    langsmithEnabled = (
        service.settings.langsmith_tracing
        and service.settings.langsmith_api_key is not None
    )

    assert client.get("/health").json() == {"status": "healthy"}
    root = client.get("/").json()
    assert root["paypal_tool_count"] == 116
    assert root["router"] == "small_model_validated_routing"
    assert root["orchestrator"] == "langgraph_state_graph"
    assert root["paypal_environment"] == service.settings.paypal_environment
    assert root["paypal_mutations_enabled"] is service.settings.paypal_allow_mutations
    assert root["langsmith_tracing"] is langsmithEnabled

    catalog = client.get("/tools").json()
    assert catalog["tool_count"] == 116
    assert catalog["total_tool_count"] == 120

    observability = client.get("/observability").json()
    assert observability == {
        "langsmith_tracing": langsmithEnabled,
        "langsmith_project": service.settings.langsmith_project,
        "model_provider": service.settings.model_provider,
        "router_model": service.settings.router_model_id,
        "main_model": service.settings.main_model_id,
        "paypal_environment": service.settings.paypal_environment,
        "paypal_mutations_enabled": service.settings.paypal_allow_mutations,
        "orchestrator": "langgraph_state_graph",
    }


def test_tool_search_endpoint() -> None:
    client = TestClient(app)

    response = client.get(
        "/tools/search",
        params={"query": "send invoice", "limit": 5},
    )

    assert response.status_code == 200
    tool_names = [tool["tool_name"] for tool in response.json()["tools"]]
    assert "paypal_invoices_invoices_send_invoice" in tool_names


def test_chat_issues_unique_bearer_conversation_ids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    conversationIds: list[str] = []

    async def fakeChat(
        _userInput: str,
        conversationId: str,
    ) -> dict[str, Any]:
        conversationIds.append(conversationId)
        return {"answer": "safe"}

    monkeypatch.setattr(service, "chat", fakeChat)
    client: TestClient = TestClient(app)

    firstResponse: httpx.Response = client.post(
        "/chat",
        json={"userInput": "Show order details"},
    )
    secondResponse: httpx.Response = client.post(
        "/chat",
        json={"userInput": "Show order details"},
    )

    assert firstResponse.status_code == 200
    assert secondResponse.status_code == 200
    assert len(set(conversationIds)) == 2
    assert all(UUID(value).version == 4 for value in conversationIds)
    assert firstResponse.json()["conversationId"] == conversationIds[0]


def test_chat_accepts_only_uuid4_conversation_tokens(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fakeChat(
        _userInput: str,
        conversationId: str,
    ) -> dict[str, Any]:
        return {"answer": conversationId}

    monkeypatch.setattr(service, "chat", fakeChat)
    client: TestClient = TestClient(app)

    response: httpx.Response = client.post(
        "/chat",
        json={
            "userInput": "Show order details",
            "conversationId": "default",
        },
    )

    assert response.status_code == 422


def test_chat_rejects_oversized_user_input() -> None:
    client: TestClient = TestClient(app)

    response: httpx.Response = client.post(
        "/chat",
        json={"userInput": "x" * 8_193},
    )

    assert response.status_code == 422


def test_missing_tool_call_returns_404() -> None:
    client = TestClient(app)

    response = client.post("/tools/paypal_missing/call", json={})

    assert response.status_code == 404


@pytest.mark.parametrize(
    ("error", "expectedStatus", "expectedDetail"),
    [
        (
            httpx.ConnectError("connection failed"),
            502,
            "PayPal request failed.",
        ),
        (
            httpx.ReadTimeout("request timed out"),
            504,
            "PayPal request timed out.",
        ),
    ],
)
def test_tool_call_maps_network_errors(
    monkeypatch: pytest.MonkeyPatch,
    error: httpx.RequestError,
    expectedStatus: int,
    expectedDetail: str,
) -> None:
    async def raiseRequestError(
        _toolName: str,
        _payload: ToolCallInput,
    ) -> dict[str, Any]:
        raise error

    monkeypatch.setattr(service, "call_tool", raiseRequestError)
    client: TestClient = TestClient(app)

    response: httpx.Response = client.post(
        "/tools/paypal_orders_show_order_details/call",
        json={"pathParams": {"order_id": "ORDER-123"}},
    )

    assert response.status_code == expectedStatus
    assert response.json() == {"detail": expectedDetail}
