from __future__ import annotations

import re
from pathlib import Path
from typing import Any


class RagPipeline:
    def __init__(self, knowledge_dir: Path) -> None:
        self.knowledge_dir = knowledge_dir

    def search(self, query: str, *, limit: int = 5) -> dict[str, Any]:
        terms = _terms(query)
        matches: list[tuple[int, Path, str]] = []
        for path in sorted(self.knowledge_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            score = sum(text.lower().count(term) for term in terms)
            if score:
                matches.append((score, path, _snippet(text, terms)))

        matches.sort(key=lambda item: (-item[0], item[1].name))
        return {
            "status": "success",
            "query": query,
            "matches": [
                {"source": path.name, "score": score, "snippet": snippet}
                for score, path, snippet in matches[:limit]
            ],
        }


def _terms(query: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]+", query.lower())
        if len(token) > 2
    }


def _snippet(text: str, terms: set[str], *, size: int = 500) -> str:
    lower_text = text.lower()
    positions = [lower_text.find(term) for term in terms if term in lower_text]
    start = max(min(positions) - 120, 0) if positions else 0
    return text[start : start + size].replace("\n", " ").strip()
