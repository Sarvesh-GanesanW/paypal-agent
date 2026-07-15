from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from paypal_agent.tracing import sanitizeTracePayload

MAX_MEMORY_LINE_LENGTH = 12000
MEMORY_EVENT_METADATA_FIELDS: frozenset[str] = frozenset(
    {
        "conversation_id_length",
        "event_type",
        "intent",
        "paypal_debug_id",
        "router_mode",
        "selected_tool_names",
        "status",
        "status_code",
        "timestamp",
        "tool_name",
        "user_input_length",
    }
)
TOOL_RESULT_METADATA_FIELDS: frozenset[str] = frozenset(
    {
        "paypal_debug_id",
        "status",
        "status_code",
        "tool_name",
    }
)


class LocalMemoryStore:
    def __init__(self, memory_dir: Path) -> None:
        self.memory_dir = memory_dir.expanduser()

    def append(self, event_type: str, payload: dict[str, Any]) -> Path:
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC)
        event: dict[str, Any] = _metadataOnlyEvent(
            {
                **payload,
                "timestamp": timestamp.isoformat(),
                "event_type": event_type,
            }
        )
        path = self._path_for(timestamp)
        line = json.dumps(event, ensure_ascii=True, separators=(",", ":"))
        with path.open("a", encoding="utf-8") as file:
            file.write(line[:MAX_MEMORY_LINE_LENGTH] + "\n")
        return path

    def grep(
        self,
        pattern: str,
        *,
        limit: int = 20,
        ignore_case: bool = True,
    ) -> list[dict[str, Any]]:
        if not pattern.strip():
            return []
        flags = re.IGNORECASE if ignore_case else 0
        try:
            regex = re.compile(pattern, flags)
        except re.error:
            regex = re.compile(re.escape(pattern), flags)
        matches: list[dict[str, Any]] = []
        for path in self._memory_files():
            with path.open(encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    if regex.search(line):
                        matches.append(self._match_payload(path, line_number, line))
                        if len(matches) >= limit:
                            return matches
        return matches

    def find(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        terms = [term.lower() for term in query.split() if term.strip()]
        if not terms:
            return []
        matches: list[dict[str, Any]] = []
        for path in self._memory_files():
            with path.open(encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    haystack = line.lower()
                    if all(term in haystack for term in terms):
                        matches.append(self._match_payload(path, line_number, line))
                        if len(matches) >= limit:
                            return matches
        return matches

    def _path_for(self, timestamp: datetime) -> Path:
        return self.memory_dir / f"memory-{timestamp:%Y-%m-%d}.jsonl"

    def _memory_files(self) -> list[Path]:
        if not self.memory_dir.exists():
            return []
        return sorted(
            self.memory_dir.glob("*.jsonl"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )

    def _match_payload(
        self,
        path: Path,
        line_number: int,
        line: str,
    ) -> dict[str, Any]:
        stripped = line.strip()
        try:
            event = json.loads(stripped)
        except json.JSONDecodeError:
            event = {}
        return {
            "file": str(path),
            "line_number": line_number,
            "event": _metadataOnlyEvent(event),
        }


def _metadataOnlyEvent(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict):
        return {}

    metadata: dict[str, Any] = {
        key: value
        for key, value in event.items()
        if key in MEMORY_EVENT_METADATA_FIELDS
    }
    toolResults: Any = event.get("tool_results")
    if isinstance(toolResults, list):
        metadata["tool_results"] = [
            {
                key: value
                for key, value in toolResult.items()
                if key in TOOL_RESULT_METADATA_FIELDS
            }
            for toolResult in toolResults
            if isinstance(toolResult, dict)
        ]
    return sanitizeTracePayload(metadata)
