from __future__ import annotations

import re
from collections import Counter

from paypal_agent.postman import ApiTool

DOMAIN_HINTS: dict[str, set[str]] = {
    "balanc": {"balances", "reporting"},
    "balance": {"balances", "reporting"},
    "balances": {"reporting"},
    "bill": {"billing", "plan", "plans", "subscription", "subscriptions"},
    "button": {"buttons", "links", "payment"},
    "dispute": {"claim", "dispute", "disputes", "evidence"},
    "invoice": {"invoice", "invoices", "invoicing", "template", "templates"},
    "order": {"authorize", "capture", "checkout", "order", "orders"},
    "pay": {"capture", "payment", "payments", "payout", "payouts", "refund"},
    "payout": {"batch", "payout", "payouts"},
    "refund": {"capture", "payments", "refund", "refunds"},
    "report": {"balances", "reporting", "transactions"},
    "sale": {"reporting", "transaction", "transactions"},
    "sales": {"reporting", "transaction", "transactions"},
    "token": {"payment-tokens", "setup-tokens", "token", "tokens", "vault"},
    "tracking": {"shipment", "shipping", "tracker", "trackers", "tracking"},
    "transaction": {"balances", "reporting", "transaction", "transactions"},
    "volume": {"reporting", "transaction", "transactions"},
    "webhook": {"event", "notification", "webhook", "webhooks"},
}
QUERY_STOP_WORDS: frozenset[str] = frozenset(
    {
        "are",
        "available",
        "can",
        "check",
        "execute",
        "for",
        "have",
        "paypal",
        "please",
        "the",
        "tool",
        "tools",
        "what",
        "which",
        "with",
    }
)


class ToolCatalogSearch:
    def __init__(self, tools: list[ApiTool]) -> None:
        self.tools: list[ApiTool] = tools
        self.toolTerms: dict[str, Counter[str]] = {
            tool.tool_name: _tokenCounts(tool.search_text) for tool in tools
        }

    def search(self, query: str, *, limit: int = 12) -> list[ApiTool]:
        queryTerms: set[str] = _expandedTerms(query)
        if not queryTerms:
            return self.tools[:limit]

        scoredTools: list[tuple[int, str, ApiTool]] = []
        for tool in self.tools:
            toolTerms: Counter[str] = self.toolTerms[tool.tool_name]
            score: int = sum(
                (4 if term in tool.tool_name else 1) * toolTerms.get(term, 0)
                for term in queryTerms
            )
            if score:
                scoredTools.append((score, tool.tool_name, tool))

        scoredTools.sort(key=lambda item: (-item[0], item[1]))
        return [tool for _, _, tool in scoredTools[:limit]]


def _expandedTerms(query: str) -> set[str]:
    terms: set[str] = set(_tokenCounts(query)) - QUERY_STOP_WORDS
    for term in list(terms):
        terms.update(DOMAIN_HINTS.get(term, set()))
    return terms


def _tokenCounts(text: str) -> Counter[str]:
    return Counter(
        token
        for token in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]+", text.lower())
        if len(token) > 2
    )
