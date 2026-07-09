from __future__ import annotations

import argparse
import asyncio
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import import_module
from pathlib import Path
from typing import Any, cast

from ragas.dataset_schema import SingleTurnSample

from paypal_agent.config import Settings
from paypal_agent.hybrid_rag import HybridRagPipeline


def _metricClass(name: str) -> Any:
    metricsModule = import_module("ragas.metrics")
    metricClass = getattr(metricsModule, f"_{name}", None)
    if metricClass is not None:
        return cast(Any, metricClass)
    return cast(Any, getattr(metricsModule, name))


IDBasedContextPrecision = _metricClass("IDBasedContextPrecision")
IDBasedContextRecall = _metricClass("IDBasedContextRecall")


@dataclass(frozen=True)
class EvalCase:
    question: str
    expected_titles: list[str]


DEFAULT_CASES: tuple[EvalCase, ...] = (
    EvalCase(
        "How do I create and send a PayPal invoice?",
        ["Invoices"],
    ),
    EvalCase(
        "How do I capture an authorized PayPal payment?",
        ["Payments"],
    ),
    EvalCase(
        "How do I search PayPal transaction history?",
        ["Transaction Search"],
    ),
    EvalCase(
        "How do I configure and verify PayPal webhooks?",
        ["Webhooks"],
    ),
    EvalCase(
        "How do I review and respond to a PayPal dispute?",
        ["Disputes"],
    ),
    EvalCase(
        "How do I create a PayPal subscription plan?",
        ["Subscriptions"],
    ),
)


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate PayPal RAG retrieval with RAGAS ID metrics."
    )
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--knowledge-dir", type=Path, default=Path("knowledge_base"))
    parser.add_argument("--output-dir", type=Path, default=Path("logs"))
    return parser.parse_args()


def main() -> int:
    args = parseArgs()
    result = asyncio.run(evaluateRag(args))
    outputPath = _writeResult(result, args.output_dir)
    summary = result["summary"]
    print(
        "ragas_eval="
        + json.dumps(
            {
                "cases": summary["cases"],
                "context_precision": summary["context_precision"],
                "context_recall": summary["context_recall"],
                "top1_accuracy": summary["top1_accuracy"],
                "mrr": summary["mrr"],
                "output": str(outputPath),
            },
            sort_keys=True,
        )
    )
    return 0


async def evaluateRag(args: argparse.Namespace) -> dict[str, Any]:
    settings = Settings()
    pipeline = HybridRagPipeline(settings, args.knowledge_dir)
    precisionMetric = IDBasedContextPrecision()
    recallMetric = IDBasedContextRecall()
    rows: list[dict[str, Any]] = []

    for case in DEFAULT_CASES:
        searchResult = pipeline.search(case.question, limit=args.limit)
        retrievedTitles = [
            str(match["title"])
            for match in searchResult.get("matches", [])
            if isinstance(match, dict) and "title" in match
        ]
        retrievedIds = [_contextId(title) for title in retrievedTitles]
        expectedIds = [_contextId(title) for title in case.expected_titles]
        sample = SingleTurnSample(
            user_input=case.question,
            retrieved_context_ids=cast(list[str | int], retrievedIds),
            reference_context_ids=cast(list[str | int], expectedIds),
        )
        precision = await precisionMetric.single_turn_ascore(sample)
        recall = await recallMetric.single_turn_ascore(sample)
        rows.append(
            {
                "question": case.question,
                "expected_titles": case.expected_titles,
                "retrieved_titles": retrievedTitles,
                "retrieved_ids": retrievedIds,
                "mode": searchResult.get("mode"),
                "context_precision": precision,
                "context_recall": recall,
                "reciprocal_rank": _reciprocalRank(expectedIds, retrievedIds),
                "top1_hit": _top1Hit(expectedIds, retrievedIds),
            }
        )

    return {
        "created_at": datetime.now(UTC).isoformat(),
        "metrics": {
            "library": "ragas",
            "context_precision": "IDBasedContextPrecision",
            "context_recall": "IDBasedContextRecall",
        },
        "summary": _summary(rows),
        "cases": rows,
    }


def _summary(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    count = len(rows)
    if count == 0:
        return {
            "cases": 0,
            "context_precision": 0.0,
            "context_recall": 0.0,
            "top1_accuracy": 0.0,
            "mrr": 0.0,
        }
    return {
        "cases": count,
        "context_precision": _mean(row["context_precision"] for row in rows),
        "context_recall": _mean(row["context_recall"] for row in rows),
        "top1_accuracy": _mean(1.0 if row["top1_hit"] else 0.0 for row in rows),
        "mrr": _mean(row["reciprocal_rank"] for row in rows),
    }


def _writeResult(result: dict[str, Any], outputDir: Path) -> Path:
    outputDir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    outputPath = outputDir / f"ragas_eval_{timestamp}.json"
    outputPath.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return outputPath


def _contextId(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")


def _top1Hit(expectedIds: list[str], retrievedIds: list[str]) -> bool:
    return bool(retrievedIds and retrievedIds[0] in set(expectedIds))


def _reciprocalRank(expectedIds: list[str], retrievedIds: list[str]) -> float:
    expected = set(expectedIds)
    for index, retrievedId in enumerate(retrievedIds, start=1):
        if retrievedId in expected:
            return 1.0 / index
    return 0.0


def _mean(values: Iterable[float]) -> float:
    numbers = [float(value) for value in values]
    if not numbers:
        return 0.0
    return round(sum(numbers) / len(numbers), 4)


if __name__ == "__main__":
    raise SystemExit(main())
