from __future__ import annotations

from pathlib import Path

import pytest

from paypal_agent import user_config
from paypal_agent.codex_provider import _codexCommand
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
    settings = Settings(codex_model_id="gpt-5.3-codex")
    outputPath = tmp_path / "output.txt"
    schemaPath = tmp_path / "schema.json"

    command = _codexCommand(settings, outputPath, schemaPath)

    assert command[:2] == ["codex", "exec"]
    assert "--ephemeral" in command
    assert "--skip-git-repo-check" in command
    assert command[command.index("--sandbox") + 1] == "read-only"
    assert command[command.index("--model") + 1] == "gpt-5.3-codex"
    assert command[command.index("--output-schema") + 1] == str(schemaPath)
    assert command[-1] == "-"


def test_default_postman_collection_is_packaged() -> None:
    assert defaultPostmanCollectionPath().exists()


def test_default_relative_postman_path_falls_back_to_package(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    resolvedPath = resolvePostmanCollectionPath(DEFAULT_POSTMAN_RELATIVE_PATH)

    assert resolvedPath == defaultPostmanCollectionPath()
    assert resolvedPath.exists()
