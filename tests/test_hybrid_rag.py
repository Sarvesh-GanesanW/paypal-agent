from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from paypal_agent.config import Settings
from paypal_agent.hybrid_rag import HybridRagPipeline
from paypal_agent.package_assets import defaultKnowledgeBasePath
from paypal_agent.rag import RagPipeline


def test_default_knowledge_path_contains_downloaded_paypal_docs() -> None:
    knowledgePath: Path = defaultKnowledgeBasePath()

    result: dict[str, Any] = RagPipeline(knowledgePath).search(
        "create and send invoice",
        limit=3,
    )

    assert result["matches"]
    assert [match["source"] for match in result["matches"]] == [
        "developer_paypal_com_docs_api_invoicing_v2.md"
    ]
    snippet: str = result["matches"][0]["snippet"].lower()
    assert "create" in snippet
    assert "send" in snippet


def test_rest_credentials_query_prefers_dedicated_guide() -> None:
    result: dict[str, Any] = RagPipeline(defaultKnowledgeBasePath()).search(
        "REST API credentials",
        limit=3,
    )

    assert result["matches"]
    assert result["matches"][0]["source"] == (
        "developer_paypal_com_api_rest.md"
    )


def test_long_document_keeps_match_near_start(tmp_path: Path) -> None:
    knowledgeDir: Path = tmp_path / "early-match"
    knowledgeDir.mkdir()
    (knowledgeDir / "guide.md").write_text(
        "needle guidance appears here. " + ("filler " * 1_000),
        encoding="utf-8",
    )

    result: dict[str, Any] = RagPipeline(knowledgeDir).search("needle")

    assert len(result["matches"]) == 1
    assert "needle guidance" in result["matches"][0]["snippet"]


def test_packaged_knowledge_base_supports_installed_cli() -> None:
    packagedPath: Path = Path(
        "src/paypal_agent/assets/knowledge_base"
    )

    result: dict[str, Any] = RagPipeline(packagedPath).search(
        "create and send invoice",
        limit=3,
    )

    assert len(result["matches"]) == 1
    assert result["matches"][0]["source"] == "paypal_api_guidance.md"


def test_empty_hybrid_index_uses_markdown_fallback(
    test_settings: Settings,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    knowledgeDir: Path = tmp_path / "knowledge"
    knowledgeDir.mkdir()
    (knowledgeDir / "invoices.md").write_text(
        "Create a draft invoice, then send it using the returned invoice ID.",
        encoding="utf-8",
    )
    pipeline: HybridRagPipeline = HybridRagPipeline(
        test_settings,
        knowledgeDir,
    )

    def embed(
        _texts: list[str],
        *,
        input_type: str,
    ) -> list[list[float]]:
        assert input_type == "search_query"
        return [[0.0]]

    def hybridSearch(
        _query: str,
        _embedding: list[float],
        *,
        limit: int,
    ) -> list[dict[str, Any]]:
        assert limit == 25
        return []

    monkeypatch.setattr(pipeline.embedder, "embed", embed)
    monkeypatch.setattr(pipeline.store, "hybrid_search", hybridSearch)

    result: dict[str, Any] = pipeline.search(
        "How do I create and send an invoice?",
        limit=3,
    )

    assert result["mode"] == "markdown_fallback"
    assert len(result["matches"]) == 1
    assert result["matches"][0]["source"] == "invoices.md"
    assert "returned invoice ID" in result["matches"][0]["snippet"]
