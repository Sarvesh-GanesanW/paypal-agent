from __future__ import annotations

import re
from collections import deque
from typing import Any

from paypal_agent.postman import ApiTool
from paypal_agent.tool_registry import ToolRegistry

REQUEST_LOG_FIELDS: frozenset[str] = frozenset(
    {
        "conversation_id_length",
        "event_type",
        "intent",
        "request_sent",
        "router_mode",
        "selected_tool_names",
        "status",
        "status_code",
        "tool_name",
        "user_input_length",
    }
)
WORD_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
FULL_CATALOG_NOUN_TERMS: frozenset[str] = frozenset(
    (
        "api apis capabilities capability catalog endpoint endpoints "
        "tool tools"
    ).split()
)
FULL_CATALOG_SCOPE_TERMS: frozenset[str] = frozenset(
    "all available catalog every full have list show what which".split()
)
FULL_CATALOG_TERMS: frozenset[str] = frozenset(
    (
        "a all api apis are available can capabilities capability catalog "
        "complete do does endpoint endpoints every full have is list me of "
        "paypal please show the there tool tools what which you your"
    ).split()
)


class RequestLog:
    def __init__(self, max_items: int = 100) -> None:
        self.items: deque[dict[str, Any]] = deque(maxlen=max_items)

    def append(self, event: dict[str, Any]) -> None:
        metadata: dict[str, Any] = {
            key: value for key, value in event.items() if key in REQUEST_LOG_FIELDS
        }
        self.items.append(metadata)

    def search(self, query: str, *, limit: int = 10) -> list[dict[str, Any]]:
        terms: list[str] = query.lower().split()
        matches: list[dict[str, Any]] = []
        for item in reversed(self.items):
            haystack: str = repr(item).lower()
            if all(term in haystack for term in terms):
                matches.append(item)
            if len(matches) >= limit:
                break
        return matches


class SystemSearch:
    def __init__(self, registry: ToolRegistry, request_log: RequestLog) -> None:
        self.registry = registry
        self.request_log = request_log

    def search(self, query: str, *, limit: int = 10) -> dict[str, Any]:
        isFullCatalog: bool = _isFullCatalogRequest(query)
        if isFullCatalog:
            matchingTools: list[ApiTool] = self.registry.tools[:limit]
        else:
            matchingTools = self.registry.search(query, limit=limit)
        return {
            "status": "success",
            "query_length": len(query),
            "query_term_count": len(query.split()),
            "is_full_catalog": isFullCatalog,
            "support_tools": [
                {
                    "tool_name": "rag_pipeline_search",
                    "description": "Search local docs and operating guidance.",
                },
                {
                    "tool_name": "system_search",
                    "description": "Search tool capabilities and recent requests.",
                },
                {
                    "tool_name": "memory_grep",
                    "description": "Grep local JSONL memory with a regex pattern.",
                },
                {
                    "tool_name": "memory_find",
                    "description": "Find local JSONL memory entries by keywords.",
                },
            ],
            "matching_tools": [tool.to_dict() for tool in matchingTools],
            "matching_requests": self.request_log.search(query, limit=limit),
        }


def _isFullCatalogRequest(userInput: str) -> bool:
    terms: set[str] = {
        match.group(0).lower() for match in WORD_PATTERN.finditer(userInput)
    }
    return (
        bool(terms & FULL_CATALOG_NOUN_TERMS)
        and bool(terms & FULL_CATALOG_SCOPE_TERMS)
        and terms <= FULL_CATALOG_TERMS
    )
