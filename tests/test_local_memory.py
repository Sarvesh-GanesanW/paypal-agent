from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from paypal_agent.local_memory import LocalMemoryStore


def test_local_memory_appends_and_greps_jsonl(tmp_path: Path) -> None:
    memory: LocalMemoryStore = LocalMemoryStore(tmp_path / "memory")

    path: Path = memory.append(
        "chat",
        {
            "conversation_id": "thread",
            "conversation_id_length": 6,
            "user_input": "send an invoice",
            "user_input_length": 15,
            "intent": "invoice_clarify",
            "authorization": "Bearer should-not-leak",
        },
    )

    matches: list[dict[str, Any]] = memory.grep("invoice")

    assert path.exists()
    assert len(matches) == 1
    assert matches[0]["event"] == {
        "timestamp": matches[0]["event"]["timestamp"],
        "event_type": "chat",
        "conversation_id_length": 6,
        "user_input_length": 15,
        "intent": "invoice_clarify",
    }


def test_local_memory_finds_all_terms(tmp_path: Path) -> None:
    memory: LocalMemoryStore = LocalMemoryStore(tmp_path / "memory")
    memory.append(
        "chat",
        {
            "user_input": "show PayPal invoice tools",
            "intent": "system_search",
            "selected_tool_names": ["paypal_invoices_list"],
        },
    )
    memory.append(
        "chat",
        {
            "user_input": "show PayPal refund tools",
            "intent": "clarify",
            "selected_tool_names": ["paypal_refunds_list"],
        },
    )

    matches: list[dict[str, Any]] = memory.find("paypal invoice")

    assert len(matches) == 1
    assert matches[0]["event"]["intent"] == "system_search"
    assert "user_input" not in matches[0]["event"]


def test_local_memory_grep_treats_invalid_regex_as_literal(
    tmp_path: Path,
) -> None:
    memory: LocalMemoryStore = LocalMemoryStore(tmp_path / "memory")
    memory.append(
        "chat",
        {
            "user_input": "look for [invoice",
            "intent": "look_[invoice",
            "event_type": "chat",
        },
    )

    matches: list[dict[str, Any]] = memory.grep("[invoice")

    assert len(matches) == 1
    assert matches[0]["event"]["event_type"] == "chat"
    assert "user_input" not in matches[0]["event"]


def test_local_memory_filters_legacy_and_malformed_records(
    tmp_path: Path,
) -> None:
    memoryDir: Path = tmp_path / "memory"
    memoryDir.mkdir()
    memoryPath: Path = memoryDir / "memory-legacy.jsonl"
    oldEvent: dict[str, Any] = {
        "timestamp": "2025-01-01T00:00:00+00:00",
        "event_type": "chat",
        "conversation_id": "private-conversation",
        "user_input": ("private ORDER-5O190127TN364715T for buyer@example.com"),
        "answer": "private buyer@example.com",
        "intent": "paypal_orders_show_order_details",
        "selected_tool_names": ["paypal_orders_show_order_details"],
        "unknown": {"order_id": "5O190127TN364715T"},
        "tool_results": [
            {
                "tool_name": "paypal_orders_show_order_details",
                "status": "success",
                "status_code": 200,
                "paypal_debug_id": "debug-correlation-id",
                "order_id": "5O190127TN364715T",
                "response": {"email": "buyer@example.com"},
            }
        ],
    }
    malformedLine: str = "private malformed ORDER-9AA12345 and seller@example.com"
    with memoryPath.open("w", encoding="utf-8") as file:
        file.write(json.dumps(oldEvent) + "\n")
        file.write(malformedLine + "\n")

    memory: LocalMemoryStore = LocalMemoryStore(memoryDir)
    grepMatches: list[dict[str, Any]] = memory.grep("private")
    findMatches: list[dict[str, Any]] = memory.find("seller@example.com")

    assert len(grepMatches) == 2
    assert grepMatches[0]["event"] == {
        "timestamp": "2025-01-01T00:00:00+00:00",
        "event_type": "chat",
        "intent": "paypal_orders_show_order_details",
        "selected_tool_names": ["paypal_orders_show_order_details"],
        "tool_results": [
            {
                "tool_name": "paypal_orders_show_order_details",
                "status": "success",
                "status_code": 200,
                "paypal_debug_id": "debug-correlation-id",
            }
        ],
    }
    assert grepMatches[1]["event"] == {}
    assert len(findMatches) == 1
    assert findMatches[0]["event"] == {}
    serializedGrepMatches: str = json.dumps(grepMatches)
    serializedFindMatches: str = json.dumps(findMatches)
    assert "private-conversation" not in serializedGrepMatches
    assert "buyer@example.com" not in serializedGrepMatches
    assert "5O190127TN364715T" not in serializedGrepMatches
    assert malformedLine not in serializedGrepMatches
    assert "seller@example.com" not in serializedFindMatches
