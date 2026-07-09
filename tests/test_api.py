from __future__ import annotations

from fastapi.testclient import TestClient

from paypal_agent.api import app, service


def test_health_and_catalog_endpoints() -> None:
    client = TestClient(app)
    langsmithEnabled = (
        service.settings.langsmith_tracing
        and service.settings.langsmith_api_key is not None
    )

    assert client.get("/health").json() == {"status": "healthy"}
    root = client.get("/").json()
    assert root["paypal_tool_count"] == 116
    assert root["router"] == "small_model_strict_schema"
    assert root["orchestrator"] == "langgraph_state_graph"
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


def test_missing_tool_call_returns_404() -> None:
    client = TestClient(app)

    response = client.post("/tools/paypal_missing/call", json={})

    assert response.status_code == 404
