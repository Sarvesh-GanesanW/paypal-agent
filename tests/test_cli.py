from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest

from paypal_agent.agent_service import AgentService
from paypal_agent.cli import CliState, _handleInput, formatChatResult
from paypal_agent.config import Settings


def test_format_chat_result_includes_route_summary() -> None:
    result: dict[str, Any] = {
        "answer": "Selected PayPal tools.",
        "selected_tool_names": ["paypal_invoices_invoices_send_invoice"],
        "tool_results": [
            {
                "status": "error",
                "status_code": 404,
                "paypal_debug_id": "debug-cli-123",
                "tool": {"tool_name": "paypal_invoices_invoices_send_invoice"},
            }
        ],
        "router_decision": {
            "intent": "paypal_tool",
            "selected_tool_names": ["paypal_invoices_invoices_send_invoice"],
            "missing_inputs": [],
            "user_message": "selected",
            "confidence": 0.9,
        },
        "metadata": {
            "router_mode": "bedrock",
            "router_error": None,
            "router_model": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
            "answer_model_used": True,
            "answer_model": "us.anthropic.claude-opus-4-6-v1",
            "subagent_model": "us.anthropic.claude-opus-4-6-v1",
        },
    }

    output = formatChatResult(result, no_color=True)

    assert "assistant>" in output
    assert "intent=paypal_tool" in output
    assert "mode=bedrock" in output
    assert "router_model=us.anthropic.claude-haiku-4-5-20251001-v1:0" in output
    assert "subagent_model=us.anthropic.claude-opus-4-6-v1" in output
    assert "answer_model=us.anthropic.claude-opus-4-6-v1" in output
    assert "paypal_invoices_invoices_send_invoice" in output
    assert "tool_call=paypal_invoices_invoices_send_invoice" in output
    assert "status_code=404" in output
    assert "paypal_debug_id=debug-cli-123" in output


@pytest.mark.asyncio
async def test_tui_query_commands_use_chat_graph(
    test_settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AgentService(test_settings)
    result: dict[str, Any] = {
        "answer": "model answer",
        "selected_tool_names": [],
        "tool_results": [],
        "router_decision": {
            "intent": "clarify",
            "selected_tool_names": [],
            "missing_inputs": [],
            "user_message": "clarify",
            "confidence": 0.9,
        },
        "metadata": {
            "router_mode": "bedrock",
            "router_error": None,
            "router_model": test_settings.router_model_id,
            "answer_model_used": True,
            "answer_model": test_settings.main_model_id,
            "subagent_model": test_settings.subagent_model_id,
        },
    }
    chatMock: AsyncMock = AsyncMock(return_value=result)
    monkeypatch.setattr(service, "chat", chatMock)
    state = CliState(
        settings=test_settings,
        service=service,
        conversation_id="query-command-thread",
        no_stream=True,
        no_color=True,
    )
    commands: list[str] = [
        "/tools invoice",
        "/rag invoice flow",
        "/grep invoice",
        "/find previous invoice",
    ]

    for command in commands:
        await _handleInput(state, command)

    assert [call.args for call in chatMock.await_args_list] == [
        (command, "query-command-thread") for command in commands
    ]
