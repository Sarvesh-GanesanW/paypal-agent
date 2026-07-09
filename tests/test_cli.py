from __future__ import annotations

from typing import Any

from paypal_agent.cli import formatChatResult


def test_format_chat_result_includes_route_summary() -> None:
    result: dict[str, Any] = {
        "answer": "Selected PayPal tools.",
        "selected_tool_names": ["paypal_invoices_invoices_send_invoice"],
        "tool_results": [
            {
                "status": "error",
                "status_code": 404,
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
        },
    }

    output = formatChatResult(result, no_color=True)

    assert "assistant>" in output
    assert "intent=paypal_tool" in output
    assert "mode=bedrock" in output
    assert "paypal_invoices_invoices_send_invoice" in output
    assert "tool_call=paypal_invoices_invoices_send_invoice" in output
    assert "status_code=404" in output
