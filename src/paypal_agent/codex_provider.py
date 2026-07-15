from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from paypal_agent.config import Settings

_CODEX_ENV_ALLOWLIST: frozenset[str] = frozenset(
    {
        "CODEX_HOME",
        "HOME",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "PATH",
        "SSL_CERT_DIR",
        "SSL_CERT_FILE",
    }
)


class CodexProviderError(RuntimeError):
    pass


def completeWithCodex(
    settings: Settings,
    prompt: str,
    *,
    schema: dict[str, Any] | None = None,
) -> str:
    with tempfile.TemporaryDirectory(prefix="paypal-agent-codex-") as tempDir:
        tempPath = Path(tempDir)
        outputPath = tempPath / "last-message.txt"
        schemaPath: Path | None = None
        if schema is not None:
            schemaPath = tempPath / "schema.json"
            schemaPath.write_text(json.dumps(schema), encoding="utf-8")

        command: list[str] = _codexCommand(settings, outputPath, schemaPath)
        environment: dict[str, str] = {
            name: value
            for name, value in os.environ.items()
            if name in _CODEX_ENV_ALLOWLIST
        }
        try:
            result: subprocess.CompletedProcess[str] = subprocess.run(
                command,
                input=prompt,
                text=True,
                capture_output=True,
                check=False,
                timeout=settings.codex_timeout_seconds,
                cwd=tempPath,
                env=environment,
            )
        except FileNotFoundError as exc:
            raise CodexProviderError("Codex command was not found.") from exc
        except subprocess.TimeoutExpired as exc:
            raise CodexProviderError("Codex provider timed out.") from exc

        if result.returncode != 0:
            raise CodexProviderError(
                "Codex provider failed. Run `codex login` or `/login codex` and retry."
            )
        if not outputPath.exists():
            raise CodexProviderError("Codex provider did not write output.")
        return outputPath.read_text(encoding="utf-8").strip()


def _codexCommand(
    settings: Settings,
    outputPath: Path,
    schemaPath: Path | None,
) -> list[str]:
    command = [
        settings.codex_command,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--color",
        "never",
        "--output-last-message",
        str(outputPath),
    ]
    if settings.codex_model_id:
        command.extend(["--model", settings.codex_model_id])
    if schemaPath is not None:
        command.extend(["--output-schema", str(schemaPath)])
    command.append("-")
    return command
