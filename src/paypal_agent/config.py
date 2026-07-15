from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from paypal_agent.package_assets import defaultPostmanCollectionPath

ModelProvider = Literal["bedrock", "openai", "anthropic", "codex"]
CodexSandboxMode = Literal["read-only", "workspace-write", "danger-full-access"]


class Settings(BaseSettings):
    app_name: str = "Datazoic PayPal Agent"
    paypal_environment: Literal["sandbox", "live"] = "sandbox"
    paypal_client_id: str | None = None
    paypal_client_secret: SecretStr | None = None
    paypal_access_token: SecretStr | None = None
    paypal_managed_client_id: str | None = None
    paypal_managed_client_secret: SecretStr | None = None
    paypal_managed_access_token: SecretStr | None = None
    paypal_upload_root: Path | None = None
    paypal_allow_mutations: bool = False
    paypal_postman_collection_path: Path = Field(
        default_factory=defaultPostmanCollectionPath
    )
    max_selected_tools: int = Field(default=12, ge=1, le=50)
    request_timeout_seconds: float = Field(default=30.0, gt=0)
    model_provider: ModelProvider = "bedrock"
    model_router_enabled: bool | None = None
    aws_region: str = "us-east-1"
    bedrock_router_enabled: bool = True
    bedrock_router_model_id: str = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    bedrock_main_model_id: str = "us.anthropic.claude-opus-4-6-v1"
    bedrock_subagent_model_id: str = "us.anthropic.claude-opus-4-6-v1"
    bedrock_embedding_model_id: str = "cohere.embed-v4:0"
    bedrock_rerank_model_id: str = "cohere.rerank-v3-5:0"
    openai_api_key: SecretStr | None = None
    openai_router_model_id: str = "gpt-5.5"
    openai_main_model_id: str = "gpt-5.5"
    openai_subagent_model_id: str = "gpt-5.5"
    anthropic_api_key: SecretStr | None = None
    anthropic_router_model_id: str = "claude-haiku-4-5-20251001"
    anthropic_main_model_id: str = "claude-opus-4-6"
    anthropic_subagent_model_id: str = "claude-opus-4-6"
    codex_command: str = "codex"
    codex_model_id: str | None = None
    codex_timeout_seconds: float = Field(default=180.0, gt=0)
    codex_sandbox: CodexSandboxMode = "read-only"
    router_timeout_seconds: float = Field(default=20.0, gt=0)
    postgres_dsn: str = "postgresql://postgres:postgres@localhost:5432/paypal_agent"
    memory_dir: Path = Field(
        default_factory=lambda: (
            Path.home() / ".local" / "share" / "paypal-agent" / "memory"
        )
    )
    langsmith_tracing: bool = False
    langsmith_api_key: SecretStr | None = None
    langsmith_project: str = "datazoic-paypal-agent"
    langsmith_endpoint: str | None = None
    langsmith_workspace_id: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    @property
    def paypal_base_url(self) -> str:
        if self.paypal_environment == "live":
            return "https://api-m.paypal.com"
        return "https://api-m.sandbox.paypal.com"

    @property
    def router_enabled(self) -> bool:
        if self.model_router_enabled is not None:
            return self.model_router_enabled
        return self.bedrock_router_enabled

    @property
    def router_model_id(self) -> str:
        if self.model_provider == "openai":
            return self.openai_router_model_id
        if self.model_provider == "anthropic":
            return self.anthropic_router_model_id
        if self.model_provider == "codex":
            return self.codex_model_id or "codex-default"
        return self.bedrock_router_model_id

    @property
    def main_model_id(self) -> str:
        if self.model_provider == "openai":
            return self.openai_main_model_id
        if self.model_provider == "anthropic":
            return self.anthropic_main_model_id
        if self.model_provider == "codex":
            return self.codex_model_id or "codex-default"
        return self.bedrock_main_model_id

    @property
    def subagent_model_id(self) -> str:
        if self.model_provider == "openai":
            return self.openai_subagent_model_id
        if self.model_provider == "anthropic":
            return self.anthropic_subagent_model_id
        if self.model_provider == "codex":
            return self.codex_model_id or "codex-default"
        return self.bedrock_subagent_model_id


settings = Settings()
