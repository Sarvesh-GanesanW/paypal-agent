from __future__ import annotations

import re
from pathlib import Path
from typing import Any

RAG_STOP_WORDS: frozenset[str] = frozenset(
    {
        "and",
        "can",
        "does",
        "how",
        "paypal",
        "safe",
        "safely",
        "the",
        "what",
        "with",
    }
)
RAG_TERM_ALIASES: dict[str, set[str]] = {
    "invoice": {"invoices", "invoicing"},
    "invoices": {"invoice", "invoicing"},
    "invoicing": {"invoice", "invoices"},
}


class RagPipeline:
    def __init__(self, knowledge_dir: Path) -> None:
        self.knowledge_dir = knowledge_dir

    def search(self, query: str, *, limit: int = 5) -> dict[str, Any]:
        terms = _terms(query)
        matches: list[tuple[int, int, Path, str]] = []
        for path in sorted(self.knowledge_dir.glob("*.md")):
            text: str = path.read_text(encoding="utf-8")
            snippet, coverage, frequency = _bestSnippet(text, terms)
            if coverage == 0:
                continue
            firstLine: str = text.splitlines()[0] if text.splitlines() else ""
            titleText: str = (path.stem + " " + firstLine).lower()
            titleCoverage: int = sum(term in titleText for term in terms)
            score: int = (
                titleCoverage * 1_000
                + coverage * 100
                + min(frequency, 99)
            )
            matches.append((score, titleCoverage, path, snippet))

        matches.sort(key=lambda item: (-item[0], item[2].name))
        if matches:
            bestTitleCoverage: int = max(match[1] for match in matches)
            if bestTitleCoverage:
                matches = [
                    match
                    for match in matches
                    if match[1] == bestTitleCoverage
                ]
        return {
            "status": "success",
            "query": query,
            "matches": [
                {"source": path.name, "score": score, "snippet": snippet}
                for score, _titleCoverage, path, snippet in matches[:limit]
            ],
        }


def _terms(query: str) -> set[str]:
    terms: set[str] = {
        token
        for token in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]+", query.lower())
        if len(token) > 2 and token not in RAG_STOP_WORDS
    }
    for term in list(terms):
        terms.update(RAG_TERM_ALIASES.get(term, set()))
    return terms


def _bestSnippet(
    text: str,
    terms: set[str],
    *,
    size: int = 500,
) -> tuple[str, int, int]:
    normalizedText: str = re.sub(r"\s+", " ", text).strip()
    lowerText: str = normalizedText.lower()
    bestStart: int = 0
    bestScore: tuple[int, int] = (0, 0)
    bestFrequency: int = 0
    step: int = max(size // 2, 1)
    for start in range(0, len(normalizedText), step):
        window: str = lowerText[start : start + size]
        coverage: int = sum(term in window for term in terms)
        frequency: int = sum(window.count(term) for term in terms)
        boilerplatePenalty: int = (
            6 if len(normalizedText) > size * 6 and start < size * 4 else 0
        )
        score: tuple[int, int] = (
            coverage,
            max(frequency - boilerplatePenalty, 0),
        )
        if score > bestScore:
            bestStart = start
            bestScore = score
            bestFrequency = frequency
    snippet: str = normalizedText[bestStart : bestStart + size].strip()
    return snippet, bestScore[0], bestFrequency
