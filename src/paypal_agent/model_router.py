from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Literal, Protocol, cast

import boto3
from pydantic import BaseModel, ConfigDict, Field

from paypal_agent.codex_provider import completeWithCodex
from paypal_agent.config import Settings
from paypal_agent.postman import ApiTool
from paypal_agent.tracing import traceRun

RouterIntent = Literal[
    "paypal_tool",
    "rag_pipeline_search",
    "system_search",
    "memory_grep",
    "memory_find",
    "clarify",
]
SUPPORT_TOOL_NAMES = {
    "rag_pipeline_search",
    "system_search",
    "memory_grep",
    "memory_find",
}
MEMORY_GREP_TERMS = {"grep"}
MEMORY_FIND_TERMS = {"memory", "memories", "remember", "recall"}
SYSTEM_TERMS = {
    "available",
    "capabilities",
    "capability",
    "history",
    "last",
    "log",
    "logs",
    "recent",
    "request",
    "requests",
    "status",
    "tool",
    "tools",
}
RAG_TERMS = {
    "architecture",
    "context",
    "design",
    "docs",
    "documentation",
    "guide",
    "guides",
    "how",
    "knowledge",
    "why",
}


class BedrockRuntimeClient(Protocol):
    def converse(self, **kwargs: Any) -> dict[str, Any]:
        ...


class RouterDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: RouterIntent
    selected_tool_names: list[str] = Field(max_length=12)
    missing_inputs: list[str] = Field(max_length=12)
    user_message: str
    confidence: float = Field(ge=0, le=1)


@dataclass(frozen=True)
class RouteResult:
    decision: RouterDecision
    mode: str
    error: str | None = None


class RouterModelError(RuntimeError):
    pass


class SmallModelRouter:
    def __init__(
        self,
        settings: Settings,
        *,
        bedrock_client: BedrockRuntimeClient | None = None,
    ) -> None:
        self.settings = settings
        self.bedrock_client = bedrock_client

    async def route(
        self,
        user_input: str,
        candidates: list[ApiTool],
    ) -> RouteResult:
        fallback = _fallback_decision(user_input, candidates)
        if not self.settings.router_enabled:
            return RouteResult(decision=fallback, mode="deterministic")

        try:
            decision = await asyncio.wait_for(
                asyncio.to_thread(self._route_with_provider, user_input, candidates),
                timeout=self.settings.router_timeout_seconds,
            )
            _validate_tool_names(decision, candidates)
        except Exception as exc:
            provider = self.settings.model_provider
            return RouteResult(
                decision=fallback,
                mode=f"deterministic_after_{provider}_error",
                error=str(exc),
            )
        return RouteResult(
            decision=decision,
            mode=self.settings.model_provider,
        )

    def _route_with_provider(
        self,
        user_input: str,
        candidates: list[ApiTool],
    ) -> RouterDecision:
        if self.settings.model_provider == "openai":
            return self._route_with_openai(user_input, candidates)
        if self.settings.model_provider == "anthropic":
            return self._route_with_anthropic(user_input, candidates)
        if self.settings.model_provider == "codex":
            return self._route_with_codex(user_input, candidates)
        return self._route_with_bedrock(user_input, candidates)

    def _route_with_bedrock(
        self,
        user_input: str,
        candidates: list[ApiTool],
    ) -> RouterDecision:
        payload = _router_payload(user_input, candidates)
        with traceRun(
            self.settings,
            "bedrock_router_converse",
            "llm",
            inputs={
                "model_id": self.settings.bedrock_router_model_id,
                "user_input": user_input,
                "candidate_tool_names": [
                    tool.tool_name for tool in candidates
                ],
            },
            metadata={
                "model_id": self.settings.bedrock_router_model_id,
                "temperature": 0.0,
                "forced_tool": "route_request",
            },
            tags=["bedrock", "router"],
        ) as trace:
            response = self._client().converse(
                modelId=self.settings.bedrock_router_model_id,
                system=[{"text": ROUTER_SYSTEM_PROMPT}],
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": payload}],
                    }
                ],
                toolConfig={
                    "tools": [_router_tool_spec()],
                    "toolChoice": {"tool": {"name": "route_request"}},
                },
                inferenceConfig={"maxTokens": 512, "temperature": 0.0},
            )
            decision = RouterDecision.model_validate(_tool_use_input(response))
            trace.end({"decision": decision.model_dump()})
            return decision

    def _route_with_openai(
        self,
        user_input: str,
        candidates: list[ApiTool],
    ) -> RouterDecision:
        if not self.settings.openai_api_key:
            raise RouterModelError("OPENAI_API_KEY is required for OpenAI routing.")
        payload = _router_payload(user_input, candidates)
        with traceRun(
            self.settings,
            "openai_router_chat_completion",
            "llm",
            inputs={
                "model_id": self.settings.openai_router_model_id,
                "user_input": user_input,
                "candidate_tool_names": [
                    tool.tool_name for tool in candidates
                ],
            },
            metadata={
                "model_id": self.settings.openai_router_model_id,
                "temperature": 0.0,
                "response_format": "json_schema",
            },
            tags=["openai", "router"],
        ) as trace:
            from openai import OpenAI

            client = OpenAI(
                api_key=self.settings.openai_api_key.get_secret_value()
            )
            response = client.chat.completions.create(
                model=self.settings.openai_router_model_id,
                messages=[
                    {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
                    {"role": "user", "content": payload},
                ],
                response_format=cast(Any, _openaiRouterResponseFormat()),
                temperature=0.0,
            )
            content = response.choices[0].message.content
            if not isinstance(content, str):
                raise RouterModelError("OpenAI router returned empty content.")
            decision = RouterDecision.model_validate_json(content)
            trace.end({"decision": decision.model_dump()})
            return decision

    def _route_with_anthropic(
        self,
        user_input: str,
        candidates: list[ApiTool],
    ) -> RouterDecision:
        if not self.settings.anthropic_api_key:
            raise RouterModelError(
                "ANTHROPIC_API_KEY is required for Anthropic routing."
            )
        payload = _router_payload(user_input, candidates)
        with traceRun(
            self.settings,
            "anthropic_router_messages",
            "llm",
            inputs={
                "model_id": self.settings.anthropic_router_model_id,
                "user_input": user_input,
                "candidate_tool_names": [
                    tool.tool_name for tool in candidates
                ],
            },
            metadata={
                "model_id": self.settings.anthropic_router_model_id,
                "temperature": 0.0,
                "forced_tool": "route_request",
            },
            tags=["anthropic", "router"],
        ) as trace:
            from anthropic import Anthropic

            client = Anthropic(
                api_key=self.settings.anthropic_api_key.get_secret_value()
            )
            response = client.messages.create(
                model=self.settings.anthropic_router_model_id,
                max_tokens=512,
                temperature=0.0,
                system=ROUTER_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": payload}],
                tools=cast(Any, [_anthropicRouterToolSpec()]),
                tool_choice=cast(Any, {"type": "tool", "name": "route_request"}),
            )
            decision = RouterDecision.model_validate(
                _anthropicToolUseInput(response)
            )
            trace.end({"decision": decision.model_dump()})
            return decision

    def _route_with_codex(
        self,
        user_input: str,
        candidates: list[ApiTool],
    ) -> RouterDecision:
        payload = _router_payload(user_input, candidates)
        prompt = (
            ROUTER_SYSTEM_PROMPT
            + "\nUse only the JSON payload below. Do not inspect files or run "
            + "commands. Return the final answer as JSON only.\n\n"
            + payload
        )
        with traceRun(
            self.settings,
            "codex_router_exec",
            "llm",
            inputs={
                "model_id": self.settings.router_model_id,
                "user_input": user_input,
                "candidate_tool_names": [
                    tool.tool_name for tool in candidates
                ],
            },
            metadata={
                "model_id": self.settings.router_model_id,
                "command": self.settings.codex_command,
                "sandbox": self.settings.codex_sandbox,
            },
            tags=["codex", "router"],
        ) as trace:
            text = completeWithCodex(
                self.settings,
                prompt,
                schema=RouterDecision.model_json_schema(),
            )
            decision = RouterDecision.model_validate_json(
                _jsonTextFromCodex(text)
            )
            trace.end({"decision": decision.model_dump()})
            return decision

    def _client(self) -> BedrockRuntimeClient:
        if self.bedrock_client:
            return self.bedrock_client
        return cast(
            BedrockRuntimeClient,
            boto3.client(
                "bedrock-runtime",
                region_name=self.settings.aws_region,
            ),
        )


ROUTER_SYSTEM_PROMPT = """\
You are the routing sub-agent for a PayPal API orchestrator.

You receive a user request and a shortlisted set of PayPal tools. Pick only from
that shortlist or from the support tools. Never invent a tool name. If required
IDs, dates, emails, amounts, or request body values are missing, list them in
missing_inputs. Mutating actions may be selected, but execution is handled by a
separate confirmation gate.

Return only through the route_request tool.
"""


def _router_tool_spec() -> dict[str, Any]:
    return {
        "toolSpec": {
            "name": "route_request",
            "description": "Select the next tool target for the PayPal request.",
            "inputSchema": {"json": RouterDecision.model_json_schema()},
        }
    }


def _anthropicRouterToolSpec() -> dict[str, Any]:
    return {
        "name": "route_request",
        "description": "Select the next tool target for the PayPal request.",
        "input_schema": RouterDecision.model_json_schema(),
    }


def _openaiRouterResponseFormat() -> dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "router_decision",
            "strict": True,
            "schema": RouterDecision.model_json_schema(),
        },
    }


def _router_payload(user_input: str, candidates: list[ApiTool]) -> str:
    payload: dict[str, Any] = {
        "user_input": user_input,
        "support_tools": [
            {
                "tool_name": "rag_pipeline_search",
                "use_when": "The user asks for docs, guides, or architecture.",
            },
            {
                "tool_name": "system_search",
                "use_when": (
                    "The user asks about available tools, capabilities, logs, "
                    "or recent request status."
                ),
            },
            {
                "tool_name": "memory_grep",
                "use_when": (
                    "The user asks to grep local JSONL memory or search memory "
                    "with a regex-like pattern."
                ),
            },
            {
                "tool_name": "memory_find",
                "use_when": (
                    "The user asks to find, recall, or remember prior local "
                    "memory entries by keywords."
                ),
            },
        ],
        "candidate_paypal_tools": [
            {
                "tool_name": tool.tool_name,
                "display_name": tool.display_name,
                "folder_path": tool.folder_path,
                "method": tool.method,
                "path": tool.path,
                "path_variables": list(tool.path_variables),
                "is_mutating": tool.is_mutating,
            }
            for tool in candidates
        ],
    }
    return json.dumps(payload, separators=(",", ":"))


def _tool_use_input(response: dict[str, Any]) -> dict[str, Any]:
    content_blocks = (
        response.get("output", {}).get("message", {}).get("content") or []
    )
    for block in content_blocks:
        tool_use = block.get("toolUse") if isinstance(block, dict) else None
        if isinstance(tool_use, dict) and tool_use.get("name") == "route_request":
            tool_input = tool_use.get("input")
            if isinstance(tool_input, dict):
                return tool_input
    raise RouterModelError("Bedrock router did not return route_request toolUse.")


def _anthropicToolUseInput(response: Any) -> dict[str, Any]:
    content_blocks = getattr(response, "content", [])
    for block in content_blocks:
        block_type = getattr(block, "type", None)
        block_name = getattr(block, "name", None)
        block_input = getattr(block, "input", None)
        if (
            block_type == "tool_use"
            and block_name == "route_request"
            and isinstance(block_input, dict)
        ):
            return block_input
    raise RouterModelError("Anthropic router did not return route_request tool_use.")


def _jsonTextFromCodex(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        return stripped[start : end + 1]
    raise RouterModelError("Codex router did not return JSON.")


def _validate_tool_names(decision: RouterDecision, candidates: list[ApiTool]) -> None:
    allowed_names = {tool.tool_name for tool in candidates} | SUPPORT_TOOL_NAMES
    invalid_names = [
        tool_name
        for tool_name in decision.selected_tool_names
        if tool_name not in allowed_names
    ]
    if invalid_names:
        raise RouterModelError(
            "Router selected invalid tools: " + ", ".join(invalid_names)
        )


def _fallback_decision(user_input: str, candidates: list[ApiTool]) -> RouterDecision:
    terms = {term.strip(".,:;?!").lower() for term in user_input.split()}
    if terms & MEMORY_GREP_TERMS:
        return RouterDecision(
            intent="memory_grep",
            selected_tool_names=["memory_grep"],
            missing_inputs=[],
            user_message="Grepping local JSONL memory.",
            confidence=0.85,
        )
    if terms & MEMORY_FIND_TERMS:
        return RouterDecision(
            intent="memory_find",
            selected_tool_names=["memory_find"],
            missing_inputs=[],
            user_message="Finding matching local memory entries.",
            confidence=0.85,
        )
    if terms & SYSTEM_TERMS:
        return RouterDecision(
            intent="system_search",
            selected_tool_names=["system_search"],
            missing_inputs=[],
            user_message="Searching system capabilities and recent requests.",
            confidence=0.8,
        )
    if terms & RAG_TERMS:
        return RouterDecision(
            intent="rag_pipeline_search",
            selected_tool_names=["rag_pipeline_search"],
            missing_inputs=[],
            user_message="Searching the local knowledge base.",
            confidence=0.8,
        )
    selected_tool_names = [tool.tool_name for tool in candidates]
    return RouterDecision(
        intent="paypal_tool" if selected_tool_names else "clarify",
        selected_tool_names=selected_tool_names,
        missing_inputs=[] if selected_tool_names else ["more specific request"],
        user_message=(
            "Selected the most relevant PayPal tools."
            if selected_tool_names
            else "Please provide the PayPal action you want to perform."
        ),
        confidence=0.65 if selected_tool_names else 0.3,
    )
