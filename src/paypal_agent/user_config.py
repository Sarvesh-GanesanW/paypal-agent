from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from paypal_agent.config import ModelProvider

CONFIG_DIR = Path.home() / ".config" / "paypal-agent"
CONFIG_PATH = CONFIG_DIR / "config.json"


class UserConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_provider: ModelProvider | None = None


def loadUserConfig() -> UserConfig:
    if not CONFIG_PATH.exists():
        return UserConfig()
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return UserConfig()
        return UserConfig.model_validate(data)
    except (OSError, json.JSONDecodeError, ValidationError):
        return UserConfig()


def saveUserConfig(config: UserConfig) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config.model_dump(exclude_none=True), indent=2) + "\n",
        encoding="utf-8",
    )


def settingsOverrides() -> dict[str, Any]:
    return loadUserConfig().model_dump(exclude_none=True)


def setProvider(provider: ModelProvider) -> UserConfig:
    config = loadUserConfig()
    updated = config.model_copy(update={"model_provider": provider})
    saveUserConfig(updated)
    return updated
