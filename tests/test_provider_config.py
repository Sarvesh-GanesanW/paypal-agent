from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from paypal_agent import user_config
from paypal_agent.codex_provider import (
    CodexProviderError,
    _codexCommand,
    completeWithCodex,
)
from paypal_agent.config import Settings
from paypal_agent.package_assets import (
    DEFAULT_POSTMAN_RELATIVE_PATH,
    defaultPostmanCollectionPath,
    resolvePostmanCollectionPath,
)


def test_user_config_persists_provider(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    configPath = tmp_path / "config.json"
    monkeypatch.setattr(user_config, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(user_config, "CONFIG_PATH", configPath)

    user_config.setProvider("codex")

    config = user_config.loadUserConfig()
    assert config.model_provider == "codex"
    assert user_config.settingsOverrides() == {"model_provider": "codex"}


def test_codex_command_uses_ephemeral_read_only_exec(tmp_path: Path) -> None:
    settings: Settings = Settings(
        codex_model_id="gpt-5.3-codex",
        codex_sandbox="danger-full-access",
    )
    outputPath = tmp_path / "output.txt"
    schemaPath = tmp_path / "schema.json"

    command = _codexCommand(settings, outputPath, schemaPath)

    assert command[:2] == ["codex", "exec"]
    assert "--ephemeral" in command
    assert "--ignore-user-config" in command
    assert "--ignore-rules" in command
    assert "--skip-git-repo-check" in command
    assert command[command.index("--sandbox") + 1] == "read-only"
    assert command[command.index("--model") + 1] == "gpt-5.3-codex"
    assert command[command.index("--output-schema") + 1] == str(schemaPath)
    assert command[-1] == "-"


def test_codex_exec_uses_temporary_cwd_and_scrubbed_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    homePath: str = "/home/tester"
    codexHomePath: str = "/home/tester/.codex-test"
    secretNames: set[str] = {
        "ANTHROPIC_API_KEY",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        "CODEX_API_KEY",
        "HTTPS_PROXY",
        "LANGSMITH_API_KEY",
        "OPENAI_API_KEY",
        "PAYPAL_ACCESS_TOKEN",
        "PAYPAL_CLIENT_SECRET",
        "UNRELATED_SECRET",
    }
    monkeypatch.setenv("HOME", homePath)
    monkeypatch.setenv("CODEX_HOME", codexHomePath)
    secretName: str
    for secretName in secretNames:
        monkeypatch.setenv(secretName, "must-not-leak")

    capturedCwd: Path | None = None
    capturedEnv: dict[str, str] = {}

    def fakeRun(
        command: list[str],
        *,
        input: str,
        text: bool,
        capture_output: bool,
        check: bool,
        timeout: float,
        cwd: Path,
        env: dict[str, str],
    ) -> subprocess.CompletedProcess[str]:
        nonlocal capturedCwd, capturedEnv
        capturedCwd = cwd
        capturedEnv = env
        assert cwd.is_dir()
        outputPath: Path = Path(command[command.index("--output-last-message") + 1])
        assert outputPath.parent == cwd
        outputPath.write_text("safe response", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fakeRun)

    response: str = completeWithCodex(
        Settings(codex_timeout_seconds=5.0),
        "route this request",
    )

    assert response == "safe response"
    assert capturedCwd is not None
    assert not capturedCwd.exists()
    assert capturedEnv["HOME"] == homePath
    assert capturedEnv["CODEX_HOME"] == codexHomePath
    assert secretNames.isdisjoint(capturedEnv)


def test_codex_failure_does_not_expose_subprocess_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fakeRun(
        command: list[str],
        **_: Any,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            command,
            1,
            stdout="sensitive PayPal response",
            stderr="secret provider token",
        )

    monkeypatch.setattr(subprocess, "run", fakeRun)

    with pytest.raises(CodexProviderError) as error:
        completeWithCodex(Settings(), "route this request")

    message: str = str(error.value)
    assert message == (
        "Codex provider failed. Run `codex login` or `/login codex` and retry."
    )
    assert "sensitive" not in message
    assert "secret" not in message


def test_default_postman_collection_is_packaged() -> None:
    assert defaultPostmanCollectionPath().exists()


def test_paypal_environment_defaults_to_sandbox() -> None:
    defaultEnvironment: object = Settings.model_fields["paypal_environment"].default

    assert defaultEnvironment == "sandbox"


def test_empty_optional_environment_values_are_ignored(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PAYPAL_ACCESS_TOKEN", "")
    monkeypatch.setenv("PAYPAL_UPLOAD_ROOT", "")
    monkeypatch.setenv("MODEL_ROUTER_ENABLED", "")

    appSettings: Settings = Settings(
        _env_file=None  # pyright: ignore[reportCallIssue]
    )

    assert appSettings.paypal_access_token is None
    assert appSettings.paypal_upload_root is None
    assert appSettings.model_router_enabled is None


def test_default_relative_postman_path_falls_back_to_package(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    resolvedPath = resolvePostmanCollectionPath(DEFAULT_POSTMAN_RELATIVE_PATH)

    assert resolvedPath == defaultPostmanCollectionPath()
    assert resolvedPath.exists()
