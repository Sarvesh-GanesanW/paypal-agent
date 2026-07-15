from __future__ import annotations

import asyncio
import json
from typing import Any, Protocol, cast

import boto3

from paypal_agent.codex_provider import completeWithCodex
from paypal_agent.config import Settings
from paypal_agent.model_router import SUPPORT_TOOL_NAMES, RouteResult
from paypal_agent.tracing import traceRun


class BedrockRuntimeClient(Protocol):
    def converse(self, **kwargs: Any) -> dict[str, Any]: ...


class BedrockAgentStack:
    def __init__(
        self,
        settings: Settings,
        *,
        bedrock_client: BedrockRuntimeClient | None = None,
    ) -> None:
        self.settings = settings
        self.bedrock_client = bedrock_client

    async def answer(
        self,
        user_input: str,
        route_result: RouteResult,
        route_payload: dict[str, Any],
        fallback_answer: str,
    ) -> str:
        if not self.settings.router_enabled:
            return fallback_answer
        decision = route_result.decision
        if (
            route_result.error
            or decision.intent in SUPPORT_TOOL_NAMES
            or decision.intent == "clarify"
            or decision.missing_inputs
            or decision.confidence < 0.5
            or route_payload.get("tool_call_results")
            or route_payload.get("required_direct_call")
        ):
            return fallback_answer
        try:
            subagent_output = await asyncio.to_thread(
                self._complete,
                self.settings.subagent_model_id,
                SUBAGENT_SYSTEM_PROMPT,
                {
                    "user_input": user_input,
                    "router_decision": route_result.decision.model_dump(),
                    "route_payload": route_payload,
                },
                1200,
            )
            answer = await asyncio.to_thread(
                self._complete,
                self.settings.main_model_id,
                ORCHESTRATOR_SYSTEM_PROMPT,
                {
                    "user_input": user_input,
                    "router_decision": route_result.decision.model_dump(),
                    "route_payload": route_payload,
                    "subagent_output": subagent_output,
                },
                1200,
            )
            return answer
        except Exception:
            return fallback_answer

    def _complete(
        self,
        model_id: str,
        system_prompt: str,
        payload: dict[str, Any],
        max_tokens: int,
    ) -> str:
        if self.settings.model_provider == "openai":
            return self._complete_openai(
                model_id,
                system_prompt,
                payload,
                max_tokens,
            )
        if self.settings.model_provider == "anthropic":
            return self._complete_anthropic(
                model_id,
                system_prompt,
                payload,
                max_tokens,
            )
        if self.settings.model_provider == "codex":
            return self._complete_codex(
                model_id,
                system_prompt,
                payload,
            )
        return self._complete_bedrock(
            model_id,
            system_prompt,
            payload,
            max_tokens,
        )

    def _complete_bedrock(
        self,
        model_id: str,
        system_prompt: str,
        payload: dict[str, Any],
        max_tokens: int,
    ) -> str:
        run_name = (
            "bedrock_subagent_converse"
            if system_prompt == SUBAGENT_SYSTEM_PROMPT
            else "bedrock_orchestrator_converse"
        )
        with traceRun(
            self.settings,
            run_name,
            "llm",
            inputs={
                "model_id": model_id,
                "payload": _payload_trace_metadata(payload),
            },
            metadata={"model_id": model_id, "temperature": 0.0},
            tags=["bedrock", "orchestrator"],
        ) as trace:
            response = self._client().converse(
                modelId=model_id,
                system=[{"text": system_prompt}],
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": json.dumps(
                                    payload,
                                    separators=(",", ":"),
                                )
                            }
                        ],
                    }
                ],
                inferenceConfig={"maxTokens": max_tokens, "temperature": 0.0},
            )
            text = _text_from_response(response)
            trace.end({"text_length": len(text)})
            return text

    def _complete_openai(
        self,
        model_id: str,
        system_prompt: str,
        payload: dict[str, Any],
        max_tokens: int,
    ) -> str:
        if not self.settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider.")
        run_name = (
            "openai_subagent_chat_completion"
            if system_prompt == SUBAGENT_SYSTEM_PROMPT
            else "openai_orchestrator_chat_completion"
        )
        with traceRun(
            self.settings,
            run_name,
            "llm",
            inputs={
                "model_id": model_id,
                "payload": _payload_trace_metadata(payload),
            },
            metadata={"model_id": model_id, "temperature": 0.0},
            tags=["openai", "orchestrator"],
        ) as trace:
            from openai import OpenAI

            client = OpenAI(api_key=self.settings.openai_api_key.get_secret_value())
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": json.dumps(payload, separators=(",", ":")),
                    },
                ],
                max_completion_tokens=max_tokens,
                temperature=0.0,
            )
            text = response.choices[0].message.content
            if not isinstance(text, str) or not text.strip():
                raise ValueError("OpenAI response did not include text.")
            trace.end({"text_length": len(text)})
            return text.strip()

    def _complete_anthropic(
        self,
        model_id: str,
        system_prompt: str,
        payload: dict[str, Any],
        max_tokens: int,
    ) -> str:
        if not self.settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider.")
        run_name = (
            "anthropic_subagent_messages"
            if system_prompt == SUBAGENT_SYSTEM_PROMPT
            else "anthropic_orchestrator_messages"
        )
        with traceRun(
            self.settings,
            run_name,
            "llm",
            inputs={
                "model_id": model_id,
                "payload": _payload_trace_metadata(payload),
            },
            metadata={"model_id": model_id, "temperature": 0.0},
            tags=["anthropic", "orchestrator"],
        ) as trace:
            from anthropic import Anthropic

            client = Anthropic(
                api_key=self.settings.anthropic_api_key.get_secret_value()
            )
            response = client.messages.create(
                model=model_id,
                max_tokens=max_tokens,
                temperature=0.0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": json.dumps(payload, separators=(",", ":")),
                    }
                ],
            )
            text = _text_from_anthropic_response(response)
            trace.end({"text_length": len(text)})
            return text

    def _complete_codex(
        self,
        model_id: str,
        system_prompt: str,
        payload: dict[str, Any],
    ) -> str:
        run_name = (
            "codex_subagent_exec"
            if system_prompt == SUBAGENT_SYSTEM_PROMPT
            else "codex_orchestrator_exec"
        )
        prompt = (
            system_prompt
            + "\nUse only the JSON payload below. Do not inspect files or run "
            + "commands. Return concise plain text.\n\n"
            + json.dumps(payload, separators=(",", ":"))
        )
        with traceRun(
            self.settings,
            run_name,
            "llm",
            inputs={
                "model_id": model_id,
                "payload": _payload_trace_metadata(payload),
            },
            metadata={
                "model_id": model_id,
                "command": self.settings.codex_command,
                "sandbox": "read-only",
            },
            tags=["codex", "orchestrator"],
        ) as trace:
            text = completeWithCodex(self.settings, prompt)
            if not text:
                raise ValueError("Codex response did not include text.")
            trace.end({"text_length": len(text)})
            return text

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


SUBAGENT_SYSTEM_PROMPT = """\
You are a PayPal tool sub-agent. Given the router decision and selected tool
metadata, produce the exact next-step plan. Do not invent PayPal IDs, request
bodies, emails, invoice numbers, or dates. If values are missing, list them.
"""

ORCHESTRATOR_SYSTEM_PROMPT = """\
You are the main PayPal orchestrator. Convert the sub-agent output into a concise
user-facing answer using the raw route_payload as the source of truth. Include
the requested PayPal details, status, errors, and debug ID. Keep operational
safeguards intact. Do not claim that a PayPal request was executed unless a tool
result says it was executed.
"""


def _payload_trace_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    routePayload = payload.get("route_payload")
    routePayloadKeys = list(routePayload) if isinstance(routePayload, dict) else []
    toolResultCount = 0
    if isinstance(routePayload, dict):
        toolResults = routePayload.get("tool_call_results")
        if isinstance(toolResults, list):
            toolResultCount = len(toolResults)
    routerDecision = payload.get("router_decision")
    routerIntent = (
        routerDecision.get("intent") if isinstance(routerDecision, dict) else None
    )
    userInput = payload.get("user_input")
    return {
        "user_input_length": len(userInput) if isinstance(userInput, str) else 0,
        "router_intent": routerIntent,
        "route_payload_keys": routePayloadKeys,
        "tool_result_count": toolResultCount,
        "has_subagent_output": "subagent_output" in payload,
    }


def _text_from_response(response: dict[str, Any]) -> str:
    content_blocks = response.get("output", {}).get("message", {}).get("content") or []
    texts = [
        block["text"]
        for block in content_blocks
        if isinstance(block, dict) and isinstance(block.get("text"), str)
    ]
    if not texts:
        raise ValueError("Bedrock response did not include text.")
    return "\n".join(texts).strip()


def _text_from_anthropic_response(response: Any) -> str:
    content_blocks = getattr(response, "content", [])
    texts = [
        block.text
        for block in content_blocks
        if getattr(block, "type", None) == "text"
        and isinstance(getattr(block, "text", None), str)
    ]
    if not texts:
        raise ValueError("Anthropic response did not include text.")
    return "\n".join(texts).strip()
