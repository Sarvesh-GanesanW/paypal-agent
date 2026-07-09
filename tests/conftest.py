from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import SecretStr

from paypal_agent.config import Settings


@pytest.fixture
def collection_path() -> Path:
    return Path("data/postman/paypal_apis.postman_collection.json")


@pytest.fixture
def test_settings(collection_path: Path, tmp_path: Path) -> Settings:
    return Settings(
        paypal_access_token=SecretStr("token"),
        paypal_postman_collection_path=collection_path,
        bedrock_router_enabled=False,
        memory_dir=tmp_path / "memory",
    )
