from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from paypal_agent.config import Settings


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

        command = _codexCommand(settings, outputPath, schemaPath)
        try:
            result = subprocess.run(
                command,
                input=prompt,
                text=True,
                capture_output=True,
                check=False,
                timeout=settings.codex_timeout_seconds,
            )
        except FileNotFoundError as exc:
            raise CodexProviderError(
                f"Codex command not found: {settings.codex_command}"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise CodexProviderError("Codex provider timed out.") from exc

        if result.returncode != 0:
            stderr = result.stderr.strip() or result.stdout.strip()
            raise CodexProviderError(
                "Codex provider failed. Run `codex login` or `/login codex` "
                f"and retry. Details: {stderr[:500]}"
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
        "--skip-git-repo-check",
        "--sandbox",
        settings.codex_sandbox,
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
