from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any

import httpx
import pytest

from paypal_agent.paypal_client import ToolCallInput
from paypal_agent.postman import ApiTool


def test_runner_summary_counts_statuses() -> None:
    module = _load_runner()
    results = [
        {"status": "success"},
        {"status": "error"},
        {"status": "client_error"},
        {"status": "requires_confirmation"},
        {"status": "skipped"},
    ]

    summary = module._summary(results)

    assert summary == {
        "total": 5,
        "sent": 4,
        "skipped": 1,
        "success": 1,
        "paypal_errors": 1,
        "client_errors": 1,
        "requires_confirmation": 1,
    }


@pytest.mark.asyncio
async def test_runner_maps_paypal_network_errors() -> None:
    module: ModuleType = _load_runner()

    class FailingService:
        async def call_tool(
            self,
            _toolName: str,
            _payload: ToolCallInput,
        ) -> dict[str, Any]:
            raise httpx.ConnectError("connection failed")

    tool: ApiTool = ApiTool(
        tool_name="paypal_test_read",
        display_name="Test read",
        folder_path="Test",
        method="GET",
        raw_url="{{base_url}}/v1/test",
        path="/v1/test",
        description="",
    )

    result: dict[str, Any] = await module._run_tool(
        FailingService(),
        tool,
        {},
        include_mutations=False,
        confirm_mutations=False,
    )

    assert result["status"] == "client_error"
    assert result["error"] == "PayPal request failed."


def _load_runner() -> ModuleType:
    path = Path(__file__).parents[1] / "scripts" / "run_paypal_collection.py"
    spec = importlib.util.spec_from_file_location("run_paypal_collection", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
