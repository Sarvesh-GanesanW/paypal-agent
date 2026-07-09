from __future__ import annotations

import json
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError

from paypal_agent.config import Settings

EMBEDDING_DIMENSION = 1536
EMBEDDING_BATCH_SIZE = 12
EMBEDDING_MAX_ATTEMPTS = 8
EMBEDDING_RETRY_BASE_SECONDS = 2.0


class BedrockEmbedder:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def embed(self, texts: list[str], *, input_type: str) -> list[list[float]]:
        if not texts:
            return []
        client = boto3.client(
            "bedrock-runtime",
            region_name=self.settings.aws_region,
        )
        results: list[list[float]] = []
        for index in range(0, len(texts), EMBEDDING_BATCH_SIZE):
            batch = texts[index : index + EMBEDDING_BATCH_SIZE]
            body = json.dumps(
                {
                    "texts": batch,
                    "input_type": input_type,
                    "truncate": "END",
                    "embedding_types": ["float"],
                }
            )
            response = _invoke_with_retry(
                client,
                model_id=self.settings.bedrock_embedding_model_id,
                body=body,
            )
            payload = json.loads(response["body"].read())
            embeddings = payload.get("embeddings", [])
            if isinstance(embeddings, dict):
                embeddings = embeddings.get("float") or next(
                    iter(embeddings.values())
                )
            results.extend(
                [float(value) for value in embedding] for embedding in embeddings
            )
        return results


class BedrockReranker:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def rerank(
        self,
        query: str,
        chunks: list[dict[str, Any]],
        *,
        top_k: int,
    ) -> list[dict[str, Any]]:
        if len(chunks) <= 1:
            return chunks
        client = boto3.client(
            "bedrock-runtime",
            region_name=self.settings.aws_region,
        )
        body = json.dumps(
            {
                "documents": [chunk["content"] for chunk in chunks],
                "query": query,
                "top_n": top_k,
                "api_version": 2,
            }
        )
        response = _invoke_with_retry(
            client,
            model_id=self.settings.bedrock_rerank_model_id,
            body=body,
        )
        payload = json.loads(response["body"].read())
        reranked: list[dict[str, Any]] = []
        for item in payload.get("results", []):
            index = item.get("index")
            if isinstance(index, int) and 0 <= index < len(chunks):
                reranked.append(
                    chunks[index] | {"rerank_score": item.get("relevance_score")}
                )
        return reranked or chunks[:top_k]


def _invoke_with_retry(
    client: Any,
    *,
    model_id: str,
    body: str,
) -> dict[str, Any]:
    for attempt in range(1, EMBEDDING_MAX_ATTEMPTS + 1):
        try:
            return client.invoke_model(
                modelId=model_id,
                body=body,
                contentType="application/json",
                accept="application/json",
            )
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")
            if (
                error_code != "ThrottlingException"
                or attempt == EMBEDDING_MAX_ATTEMPTS
            ):
                raise
            delay_seconds = EMBEDDING_RETRY_BASE_SECONDS * attempt
            time.sleep(delay_seconds)
    raise RuntimeError("Bedrock invoke retry loop exited unexpectedly.")
