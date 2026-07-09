from __future__ import annotations

from scripts.evaluate_rag import _contextId, _reciprocalRank, _summary


def test_ragas_eval_helpers_score_retrieval_ids() -> None:
    assert _contextId("Transaction Search") == "transaction_search"
    assert _reciprocalRank(["invoices"], ["orders", "invoices"]) == 0.5

    summary = _summary(
        [
            {
                "context_precision": 1.0,
                "context_recall": 1.0,
                "top1_hit": True,
                "reciprocal_rank": 1.0,
            },
            {
                "context_precision": 0.5,
                "context_recall": 0.0,
                "top1_hit": False,
                "reciprocal_rank": 0.5,
            },
        ]
    )

    assert summary["context_precision"] == 0.75
    assert summary["context_recall"] == 0.5
    assert summary["top1_accuracy"] == 0.5
    assert summary["mrr"] == 0.75
