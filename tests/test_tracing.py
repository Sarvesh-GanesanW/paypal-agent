from __future__ import annotations

from paypal_agent.config import Settings
from paypal_agent.tracing import sanitizeTracePayload, traceRun


def test_sanitize_trace_payload_redacts_secrets() -> None:
    payload: dict[str, object] = {
        "authorization": "Bearer token",
        "nested": {
            "client_secret": "secret",
            "normal": "value",
        },
        "large": "x" * 2000,
    }

    sanitized = sanitizeTracePayload(payload)

    assert sanitized["authorization"] == "***"
    assert sanitized["nested"]["client_secret"] == "***"
    assert sanitized["nested"]["normal"] == "value"
    assert str(sanitized["large"]).endswith("...[truncated]")


def test_trace_run_is_noop_without_langsmith_key() -> None:
    settings = Settings(langsmith_tracing=True, langsmith_api_key=None)

    with traceRun(settings, "unit_test") as trace:
        trace.end({"status": "ok"})

    assert trace.run is None
