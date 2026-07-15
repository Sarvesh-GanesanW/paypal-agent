from __future__ import annotations

import atexit
import os
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from pydantic import SecretStr

if TYPE_CHECKING:
    from paypal_agent.config import Settings

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
_TEST_MEMORY_DIR: Path = Path(tempfile.gettempdir()) / (
    f"paypal-agent-tests-{os.getpid()}"
)
_TEST_ENVIRONMENT: dict[str, str] = {
    "ANTHROPIC_API_KEY": "test-key",
    "AWS_ACCESS_KEY_ID": "test-access-key",
    "AWS_EC2_METADATA_DISABLED": "true",
    "AWS_SECRET_ACCESS_KEY": "test-secret-key",
    "BEDROCK_ROUTER_ENABLED": "false",
    "LANGSMITH_API_KEY": "test-key",
    "LANGSMITH_TRACING": "false",
    "MEMORY_DIR": str(_TEST_MEMORY_DIR),
    "MODEL_PROVIDER": "bedrock",
    "MODEL_ROUTER_ENABLED": "false",
    "OPENAI_API_KEY": "test-key",
    "PAYPAL_ACCESS_TOKEN": "test-token",
    "PAYPAL_ALLOW_MUTATIONS": "false",
    "PAYPAL_CLIENT_ID": "test-client-id",
    "PAYPAL_CLIENT_SECRET": "test-client-secret",
    "PAYPAL_ENVIRONMENT": "sandbox",
    "PAYPAL_MANAGED_ACCESS_TOKEN": "test-managed-token",
    "PAYPAL_MANAGED_CLIENT_ID": "test-managed-client-id",
    "PAYPAL_MANAGED_CLIENT_SECRET": "test-managed-client-secret",
    "PAYPAL_POSTMAN_COLLECTION_PATH": str(
        _PROJECT_ROOT / "data/postman/paypal_apis.postman_collection.json"
    ),
    "PAYPAL_UPLOAD_ROOT": str(_TEST_MEMORY_DIR / "uploads"),
}
os.environ.update(_TEST_ENVIRONMENT)
atexit.register(shutil.rmtree, _TEST_MEMORY_DIR, ignore_errors=True)


@pytest.fixture
def collection_path() -> Path:
    return Path("data/postman/paypal_apis.postman_collection.json")


@pytest.fixture
def test_settings(collection_path: Path, tmp_path: Path) -> Settings:
    from paypal_agent.config import Settings

    return Settings(
        _env_file=None,  # pyright: ignore[reportCallIssue]
        paypal_environment="sandbox",
        paypal_client_id=None,
        paypal_client_secret=None,
        paypal_access_token=SecretStr("token"),
        paypal_managed_client_id=None,
        paypal_managed_client_secret=None,
        paypal_managed_access_token=None,
        paypal_upload_root=None,
        paypal_allow_mutations=False,
        paypal_postman_collection_path=collection_path,
        model_router_enabled=False,
        bedrock_router_enabled=False,
        memory_dir=tmp_path / "memory",
        langsmith_tracing=False,
        langsmith_api_key=None,
    )
