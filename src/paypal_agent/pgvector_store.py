from __future__ import annotations

from typing import Any

import psycopg
from psycopg import sql
from psycopg.rows import dict_row

from paypal_agent.bedrock_rag import EMBEDDING_DIMENSION


class PgVectorStore:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def ensure_schema(self) -> None:
        with psycopg.connect(self.dsn, autocommit=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cursor.execute(
                    """
                    SELECT format_type(a.atttypid, a.atttypmod)
                    FROM pg_attribute a
                    JOIN pg_class c ON c.oid = a.attrelid
                    WHERE c.relname = 'paypal_doc_chunks'
                    AND a.attname = 'embedding'
                    AND NOT a.attisdropped;
                    """
                )
                row = cursor.fetchone()
                expected_type = f"vector({EMBEDDING_DIMENSION})"
                if row and row[0] != expected_type:
                    cursor.execute("DROP TABLE paypal_doc_chunks;")
                cursor.execute(
                    sql.SQL(
                        """
                    CREATE TABLE IF NOT EXISTS paypal_doc_chunks (
                        id bigserial PRIMARY KEY,
                        source_url text NOT NULL,
                        title text NOT NULL,
                        chunk_index integer NOT NULL,
                        content text NOT NULL,
                        embedding vector({dimension}) NOT NULL,
                        created_at timestamptz NOT NULL DEFAULT now(),
                        content_tsv tsvector GENERATED ALWAYS AS (
                            to_tsvector('english', content)
                        ) STORED
                    );
                    """
                    ).format(dimension=sql.Literal(EMBEDDING_DIMENSION))
                )
                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_paypal_doc_chunks_tsv
                    ON paypal_doc_chunks USING gin(content_tsv);
                    """
                )
                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_paypal_doc_chunks_embedding
                    ON paypal_doc_chunks
                    USING hnsw (embedding vector_cosine_ops);
                    """
                )
                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_paypal_doc_chunks_embedding_ivfflat
                    ON paypal_doc_chunks
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                    """
                )

    def replace_document_chunks(self, chunks: list[dict[str, Any]]) -> None:
        if not chunks:
            return
        source_urls = sorted({str(chunk["source_url"]) for chunk in chunks})
        with psycopg.connect(self.dsn, autocommit=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM paypal_doc_chunks WHERE source_url = ANY(%s);",
                    (source_urls,),
                )
                rows = [
                    (
                        chunk["source_url"],
                        chunk["title"],
                        chunk["chunk_index"],
                        chunk["content"],
                        _vector_literal(chunk["embedding"]),
                    )
                    for chunk in chunks
                ]
                cursor.executemany(
                    """
                    INSERT INTO paypal_doc_chunks (
                        source_url, title, chunk_index, content, embedding
                    )
                    VALUES (%s, %s, %s, %s, %s::vector);
                    """,
                    rows,
                )

    def hybrid_search(
        self,
        query: str,
        embedding: list[float],
        *,
        limit: int = 25,
        vector_weight: float = 0.7,
        text_weight: float = 0.3,
    ) -> list[dict[str, Any]]:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    WITH scored AS (
                        SELECT
                            source_url,
                            title,
                            chunk_index,
                            content,
                            1 - (embedding <=> %s::vector) AS vector_score,
                            ts_rank_cd(
                                content_tsv,
                                plainto_tsquery('english', %s)
                            ) AS text_score
                        FROM paypal_doc_chunks
                    )
                    SELECT
                        source_url,
                        title,
                        chunk_index,
                        content,
                        vector_score,
                        text_score,
                        (%s * vector_score + %s * text_score) AS score
                    FROM scored
                    ORDER BY score DESC
                    LIMIT %s;
                    """,
                    (
                        _vector_literal(embedding),
                        query,
                        vector_weight,
                        text_weight,
                        limit,
                    ),
                )
                return [dict(row) for row in cursor.fetchall()]


def _vector_literal(values: list[float]) -> str:
    return "[" + ",".join(str(float(value)) for value in values) + "]"
