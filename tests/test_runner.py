from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def test_runner_summary_counts_statuses() -> None:
    module = _load_runner()
    results = [
        {"status": "success"},
        {"status": "error"},
        {"status": "client_error"},
        {"status": "requires_confirmation"},
        {"status": "skipped"},
    ]

    summary = module._summary(results)

    assert summary == {
        "total": 5,
        "sent": 4,
        "skipped": 1,
        "success": 1,
        "paypal_errors": 1,
        "client_errors": 1,
        "requires_confirmation": 1,
    }


def _load_runner() -> ModuleType:
    path = Path(__file__).parents[1] / "scripts" / "run_paypal_collection.py"
    spec = importlib.util.spec_from_file_location("run_paypal_collection", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
