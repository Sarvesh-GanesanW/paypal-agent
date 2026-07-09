from __future__ import annotations

import re
from collections import Counter

from paypal_agent.postman import ApiTool

DOMAIN_HINTS = {
    "bill": {"billing", "plan", "plans", "subscription", "subscriptions"},
    "button": {"buttons", "links", "payment"},
    "dispute": {"claim", "dispute", "disputes", "evidence"},
    "invoice": {"invoice", "invoices", "invoicing", "template", "templates"},
    "order": {"authorize", "capture", "checkout", "order", "orders"},
    "pay": {"capture", "payment", "payments", "payout", "payouts", "refund"},
    "payout": {"batch", "payout", "payouts"},
    "refund": {"capture", "payments", "refund", "refunds"},
    "report": {"balances", "reporting", "transactions"},
    "token": {"payment-tokens", "setup-tokens", "token", "tokens", "vault"},
    "tracking": {"shipment", "shipping", "tracker", "trackers", "tracking"},
    "transaction": {"balances", "reporting", "transaction", "transactions"},
    "webhook": {"event", "notification", "webhook", "webhooks"},
}


class ToolRouter:
    def __init__(self, tools: list[ApiTool]) -> None:
        self.tools = tools
        self.tool_terms = {
            tool.tool_name: _token_counts(tool.search_text) for tool in tools
        }

    def search(self, query: str, *, limit: int = 12) -> list[ApiTool]:
        query_terms = _expanded_terms(query)
        if not query_terms:
            return self.tools[:limit]

        scored_tools: list[tuple[int, str, ApiTool]] = []
        for tool in self.tools:
            tool_terms = self.tool_terms[tool.tool_name]
            score = sum(
                (4 if term in tool.tool_name else 1) * tool_terms.get(term, 0)
                for term in query_terms
            )
            if score:
                scored_tools.append((score, tool.tool_name, tool))

        scored_tools.sort(key=lambda item: (-item[0], item[1]))
        return [tool for _, _, tool in scored_tools[:limit]]


def _expanded_terms(query: str) -> set[str]:
    terms = set(_token_counts(query))
    for term in list(terms):
        terms.update(DOMAIN_HINTS.get(term, set()))
    return terms


def _token_counts(text: str) -> Counter[str]:
    return Counter(
        token
        for token in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]+", text.lower())
        if len(token) > 2
    )
