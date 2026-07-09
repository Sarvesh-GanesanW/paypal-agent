from __future__ import annotations

from pathlib import Path

from paypal_agent.local_memory import LocalMemoryStore


def test_local_memory_appends_and_greps_jsonl(tmp_path: Path) -> None:
    memory = LocalMemoryStore(tmp_path / "memory")

    path = memory.append(
        "chat",
        {
            "conversation_id": "thread",
            "user_input": "send an invoice",
            "authorization": "Bearer should-not-leak",
        },
    )

    matches = memory.grep("invoice")

    assert path.exists()
    assert len(matches) == 1
    assert matches[0]["event"]["user_input"] == "send an invoice"
    assert matches[0]["event"]["authorization"] == "***"


def test_local_memory_finds_all_terms(tmp_path: Path) -> None:
    memory = LocalMemoryStore(tmp_path / "memory")
    memory.append("chat", {"user_input": "show PayPal invoice tools"})
    memory.append("chat", {"user_input": "show PayPal refund tools"})

    matches = memory.find("paypal invoice")

    assert len(matches) == 1
    assert matches[0]["event"]["user_input"] == "show PayPal invoice tools"


def test_local_memory_grep_treats_invalid_regex_as_literal(
    tmp_path: Path,
) -> None:
    memory = LocalMemoryStore(tmp_path / "memory")
    memory.append("chat", {"user_input": "look for [invoice"})

    matches = memory.grep("[invoice")

    assert len(matches) == 1
    assert matches[0]["event"]["user_input"] == "look for [invoice"
