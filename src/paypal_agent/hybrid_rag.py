from __future__ import annotations

from pathlib import Path
from typing import Any

from paypal_agent.bedrock_rag import BedrockEmbedder, BedrockReranker
from paypal_agent.config import Settings
from paypal_agent.pgvector_store import PgVectorStore
from paypal_agent.rag import RagPipeline
from paypal_agent.tracing import traceRun


class HybridRagPipeline:
    def __init__(self, settings: Settings, knowledge_dir: Path) -> None:
        self.settings = settings
        self.markdown_fallback = RagPipeline(knowledge_dir)
        self.embedder = BedrockEmbedder(settings)
        self.reranker = BedrockReranker(settings)
        self.store = PgVectorStore(settings.postgres_dsn)

    def search(self, query: str, *, limit: int = 5) -> dict[str, Any]:
        try:
            with traceRun(
                self.settings,
                "rag_query_embedding",
                "embedding",
                inputs={"query_length": len(query)},
                metadata={"model_id": self.settings.bedrock_embedding_model_id},
                tags=["rag", "embedding"],
            ) as trace:
                embedding = self.embedder.embed(
                    [query],
                    input_type="search_query",
                )[0]
                trace.end({"embedding_dimension": len(embedding)})
            with traceRun(
                self.settings,
                "pgvector_hybrid_search",
                "retriever",
                inputs={"query_length": len(query), "limit": 25},
                tags=["rag", "pgvector"],
            ) as trace:
                chunks = self.store.hybrid_search(query, embedding, limit=25)
                trace.end(
                    {
                        "match_count": len(chunks),
                        "titles": [chunk["title"] for chunk in chunks[:limit]],
                    }
                )
            if not chunks:
                return self._markdownFallback(
                    query,
                    limit=limit,
                    hybridAvailable=True,
                )
            with traceRun(
                self.settings,
                "rag_rerank",
                "retriever",
                inputs={
                    "query_length": len(query),
                    "candidate_count": len(chunks),
                    "top_k": limit,
                },
                metadata={"model_id": self.settings.bedrock_rerank_model_id},
                tags=["rag", "rerank"],
            ) as trace:
                reranked = self.reranker.rerank(query, chunks, top_k=limit)
                trace.end(
                    {
                        "match_count": len(reranked),
                        "titles": [chunk["title"] for chunk in reranked[:limit]],
                    }
                )
        except Exception:
            return self._markdownFallback(
                query,
                limit=limit,
                hybridAvailable=False,
            )

        if not reranked:
            return self._markdownFallback(
                query,
                limit=limit,
                hybridAvailable=True,
            )

        return {
            "status": "success",
            "mode": "pgvector_hybrid",
            "query": query,
            "matches": [
                {
                    "source": chunk["source_url"],
                    "title": chunk["title"],
                    "score": chunk.get("score"),
                    "snippet": chunk["content"][:500],
                }
                for chunk in reranked[:limit]
            ],
        }

    def _markdownFallback(
        self,
        query: str,
        *,
        limit: int,
        hybridAvailable: bool,
    ) -> dict[str, Any]:
        with traceRun(
            self.settings,
            "rag_markdown_fallback",
            "retriever",
            inputs={"query_length": len(query), "limit": limit},
            tags=["rag", "fallback"],
        ) as trace:
            fallback: dict[str, Any] = self.markdown_fallback.search(
                query,
                limit=limit,
            )
            trace.end(
                {
                    "match_count": len(fallback["matches"]),
                    "hybrid_rag_available": hybridAvailable,
                }
            )
        fallback["mode"] = "markdown_fallback"
        if hybridAvailable:
            fallback["error"] = (
                "Hybrid RAG returned no matches; used local markdown fallback."
            )
        else:
            fallback["error"] = (
                "Hybrid RAG was unavailable; used local markdown fallback."
            )
        return fallback
