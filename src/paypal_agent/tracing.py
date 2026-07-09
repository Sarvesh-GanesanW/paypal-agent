from __future__ import annotations

import sys
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Literal

from langsmith import Client, trace

from paypal_agent.config import Settings

MAX_TRACE_STRING_LENGTH = 1500
MAX_TRACE_SEQUENCE_ITEMS = 20
MAX_TRACE_MAPPING_ITEMS = 50
SECRET_KEY_TERMS = {
    "api_key",
    "authorization",
    "client_secret",
    "password",
    "secret",
    "token",
}
RunType = Literal[
    "tool",
    "chain",
    "llm",
    "retriever",
    "embedding",
    "prompt",
    "parser",
]


@dataclass(frozen=True)
class LangSmithTrace:
    run: Any | None

    def end(self, outputs: Mapping[str, Any] | None = None) -> None:
        if self.run is None:
            return
        try:
            self.run.end(outputs=sanitizeTracePayload(outputs or {}))
        except Exception:
            return


@contextmanager
def traceRun(
    settings: Settings,
    name: str,
    run_type: RunType = "chain",
    *,
    inputs: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Iterator[LangSmithTrace]:
    if not _langsmithEnabled(settings):
        yield LangSmithTrace(None)
        return

    try:
        client = Client(
            api_key=settings.langsmith_api_key.get_secret_value()
            if settings.langsmith_api_key
            else None,
            api_url=settings.langsmith_endpoint,
            workspace_id=settings.langsmith_workspace_id,
        )
        manager = trace(
            name,
            run_type,
            inputs=sanitizeTracePayload(inputs or {}),
            metadata=sanitizeTracePayload(metadata or {}),
            tags=tags,
            project_name=settings.langsmith_project,
            client=client,
        )
        run = manager.__enter__()
    except Exception:
        yield LangSmithTrace(None)
        return

    try:
        yield LangSmithTrace(run)
    except BaseException:
        try:
            manager.__exit__(*sys.exc_info())
        except Exception:
            pass
        raise
    else:
        try:
            manager.__exit__(None, None, None)
        except Exception:
            return


def flushLangSmith(settings: Settings) -> None:
    if not _langsmithEnabled(settings):
        return
    client = Client(
        api_key=settings.langsmith_api_key.get_secret_value()
        if settings.langsmith_api_key
        else None,
        api_url=settings.langsmith_endpoint,
        workspace_id=settings.langsmith_workspace_id,
    )
    client.flush()


def sanitizeTracePayload(value: Any) -> Any:
    return _sanitizeTraceValue(value, parent_key="")


def _langsmithEnabled(settings: Settings) -> bool:
    return bool(settings.langsmith_tracing and settings.langsmith_api_key)


def _sanitizeTraceValue(value: Any, *, parent_key: str) -> Any:
    if _isSecretKey(parent_key):
        return "***"
    if isinstance(value, str):
        return _truncateString(value)
    if isinstance(value, int | float | bool) or value is None:
        return value
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for index, (key, child_value) in enumerate(value.items()):
            if index >= MAX_TRACE_MAPPING_ITEMS:
                result["__truncated__"] = (
                    f"mapping limited to {MAX_TRACE_MAPPING_ITEMS} items"
                )
                break
            key_string = str(key)
            result[key_string] = _sanitizeTraceValue(
                child_value,
                parent_key=key_string,
            )
        return result
    if isinstance(value, Sequence) and not isinstance(value, bytes | bytearray):
        items = [
            _sanitizeTraceValue(item, parent_key=parent_key)
            for item in value[:MAX_TRACE_SEQUENCE_ITEMS]
        ]
        if len(value) > MAX_TRACE_SEQUENCE_ITEMS:
            items.append(
                f"__truncated__: sequence limited to "
                f"{MAX_TRACE_SEQUENCE_ITEMS} items"
            )
        return items
    return _truncateString(repr(value))


def _isSecretKey(key: str) -> bool:
    normalized = key.lower()
    return any(term in normalized for term in SECRET_KEY_TERMS)


def _truncateString(value: str) -> str:
    if len(value) <= MAX_TRACE_STRING_LENGTH:
        return value
    return value[:MAX_TRACE_STRING_LENGTH] + "...[truncated]"
