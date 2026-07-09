from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from paypal_agent.bedrock_rag import BedrockEmbedder
from paypal_agent.config import Settings
from paypal_agent.pgvector_store import PgVectorStore

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Embed PayPal docs into pgvector.")
    parser.add_argument("--docs-dir", type=Path, default=Path("data/paypal_docs"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = Settings()
    store = PgVectorStore(settings.postgres_dsn)
    embedder = BedrockEmbedder(settings)
    store.ensure_schema()

    chunks: list[dict[str, Any]] = []
    for path in sorted(args.docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = _title(text, path)
        source_url = _source_url(text, path)
        text_chunks = _chunks(text)
        embeddings = embedder.embed(text_chunks, input_type="search_document")
        for index, (chunk_text, embedding) in enumerate(
            zip(text_chunks, embeddings, strict=True)
        ):
            chunks.append(
                {
                    "source_url": source_url,
                    "title": title,
                    "chunk_index": index,
                    "content": chunk_text,
                    "embedding": embedding,
                }
            )

    store.replace_document_chunks(chunks)
    print(f"ingested_chunks={len(chunks)}")
    return 0


def _chunks(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(start + CHUNK_SIZE, len(normalized))
        chunks.append(normalized[start:end])
        if end == len(normalized):
            break
        start = max(end - CHUNK_OVERLAP, start + 1)
    return chunks


def _title(text: str, path: Path) -> str:
    first_line = text.splitlines()[0] if text.splitlines() else ""
    return first_line.lstrip("# ").strip() or path.stem


def _source_url(text: str, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("Source: "):
            return line.removeprefix("Source: ").strip()
    return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
