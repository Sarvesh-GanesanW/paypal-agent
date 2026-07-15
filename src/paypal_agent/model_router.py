from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
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
SUPPORT_TOOL_MESSAGES: dict[str, str] = {
    "rag_pipeline_search": "Searching the local knowledge base.",
    "system_search": "Searching system capabilities and recent requests.",
    "memory_grep": "Grepping local JSONL memory.",
    "memory_find": "Finding matching local memory entries.",
}
MEMORY_GREP_TERMS = {"grep"}
MEMORY_FIND_TERMS = {"memory", "memories", "remember", "recall"}
SYSTEM_TERMS = {"capabilities", "capability", "log", "logs", "tool", "tools"}
SYSTEM_PHRASES = {
    "available capabilities",
    "available tools",
    "last request",
    "last requests",
    "recent request",
    "recent requests",
    "request history",
    "request log",
    "request logs",
    "system log",
    "system logs",
    "system status",
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
TOOL_TERM_ALIASES = {
    "fetch": "show",
    "get": "show",
    "last": "list",
    "latest": "list",
    "recent": "list",
    "retrieve": "show",
    "sale": "transaction",
    "volume": "transaction",
}
TOOL_TERM_STOP_WORDS = {
    "a",
    "all",
    "an",
    "and",
    "detail",
    "details",
    "for",
    "information",
    "of",
    "the",
}
IDENTIFIER_SKIP_WORDS = {
    "called",
    "detail",
    "details",
    "id",
    "is",
    "named",
    "number",
    "please",
    "request",
    "with",
}
REQUIRED_DATE_QUERY_PARAMS = {
    "/v1/billing/subscriptions/{subscription_id}/transactions": (
        "start_time",
        "end_time",
    ),
    "/v1/reporting/transactions": ("start_date", "end_date"),
}
FIXED_QUERY_PARAMETER_NAMES = {"schema"}
SERVER_QUERY_PARAMETERS = {
    "/v1/reporting/transactions": {"page", "page_size"},
}
SERVER_QUERY_DEFAULTS = {
    "/v1/reporting/transactions": {"page_size": 100},
}
PROTECTED_HEADER_NAMES = {
    "authorization",
    "content-length",
    "content-type",
    "host",
    "paypal-auth-assertion",
    "paypal-request-id",
    "proxy-authorization",
}
DATE_PATTERN = re.compile(
    r"\b\d{4}-\d{2}-\d{2}"
    r"(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?\b"
)
WORD_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
VARIABLE_PATTERN = re.compile(r"\{\{([^{}]+)\}\}")


class BedrockRuntimeClient(Protocol):
    def converse(self, **kwargs: Any) -> dict[str, Any]: ...


class RoutedToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    path_params: dict[str, Any] = Field(default_factory=dict, alias="pathParams")
    query: dict[str, Any] = Field(default_factory=dict)
    body: Any = None
    headers: dict[str, str] = Field(default_factory=dict)


class RouterDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: RouterIntent
    selected_tool_names: list[str] = Field(max_length=1)
    tool_input: RoutedToolInput | None = None
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
        routableCandidates: list[ApiTool] = [
            tool for tool in candidates if tool.unsupported_reason is None
        ]
        multiStepDecision: RouterDecision | None = _multiStepDecision(user_input)
        if multiStepDecision is not None:
            return RouteResult(
                decision=multiStepDecision,
                mode="deterministic_multi_step",
            )
        if not self.settings.router_enabled:
            return RouteResult(
                decision=_fallback_decision(user_input, routableCandidates),
                mode="deterministic",
            )

        provider: str = self.settings.model_provider
        try:
            decision = await asyncio.wait_for(
                asyncio.to_thread(
                    self._route_with_provider,
                    user_input,
                    routableCandidates,
                ),
                timeout=self.settings.router_timeout_seconds,
            )
        except Exception:
            fallbackDecision: RouterDecision = _fallback_decision(
                user_input,
                routableCandidates,
            )
            if not fallbackDecision.missing_inputs:
                fallbackDecision = _provider_error_decision()
            return RouteResult(
                decision=fallbackDecision,
                mode=f"deterministic_after_{provider}_error",
                error="Model router unavailable.",
            )

        try:
            _validate_decision(decision, routableCandidates, user_input)
        except RouterModelError:
            validationFallback: RouterDecision | None = _validationFallback(
                user_input,
                routableCandidates,
                decision,
            )
            if validationFallback is not None:
                return RouteResult(
                    decision=validationFallback,
                    mode=f"deterministic_after_{provider}_validation",
                )
            return RouteResult(
                decision=_provider_error_decision(),
                mode=f"deterministic_after_{provider}_error",
                error="Model router unavailable.",
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
                "user_input_length": len(user_input),
                "candidate_tool_names": [tool.tool_name for tool in candidates],
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
            trace.end(_decision_trace_metadata(decision))
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
                "user_input_length": len(user_input),
                "candidate_tool_names": [tool.tool_name for tool in candidates],
            },
            metadata={
                "model_id": self.settings.openai_router_model_id,
                "temperature": 0.0,
                "response_format": "json_object",
            },
            tags=["openai", "router"],
        ) as trace:
            from openai import OpenAI

            client = OpenAI(api_key=self.settings.openai_api_key.get_secret_value())
            response = client.chat.completions.create(
                model=self.settings.openai_router_model_id,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            ROUTER_SYSTEM_PROMPT + DIRECT_JSON_ROUTER_INSTRUCTIONS
                        ),
                    },
                    {"role": "user", "content": payload},
                ],
                response_format=cast(Any, _openaiRouterResponseFormat()),
                temperature=0.0,
            )
            content = response.choices[0].message.content
            if not isinstance(content, str):
                raise RouterModelError("OpenAI router returned empty content.")
            decision = RouterDecision.model_validate_json(content)
            trace.end(_decision_trace_metadata(decision))
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
                "user_input_length": len(user_input),
                "candidate_tool_names": [tool.tool_name for tool in candidates],
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
            decision = RouterDecision.model_validate(_anthropicToolUseInput(response))
            trace.end(_decision_trace_metadata(decision))
            return decision

    def _route_with_codex(
        self,
        user_input: str,
        candidates: list[ApiTool],
    ) -> RouterDecision:
        payload = _router_payload(user_input, candidates)
        prompt = (
            ROUTER_SYSTEM_PROMPT
            + DIRECT_JSON_ROUTER_INSTRUCTIONS
            + "Do not inspect files or run commands.\n\n"
            + payload
        )
        with traceRun(
            self.settings,
            "codex_router_exec",
            "llm",
            inputs={
                "model_id": self.settings.router_model_id,
                "user_input_length": len(user_input),
                "candidate_tool_names": [tool.tool_name for tool in candidates],
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
            )
            decision = RouterDecision.model_validate_json(_jsonTextFromCodex(text))
            trace.end(_decision_trace_metadata(decision))
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
that shortlist or from the support tools. Never invent a tool name and never
select more than one. For a PayPal tool, copy every user-provided path, query,
header, and body value into tool_input. Copy only values explicitly marked as
fixed from tool metadata; other metadata values are not defaults. If required
IDs, dates, emails, amounts, or request body values are missing, list them in
missing_inputs. Never set confirm=true. Mutating actions may be selected, but
chat only prepares them for a separate confirmation gate.

Return only through the route_request tool.
"""

DIRECT_JSON_ROUTER_INSTRUCTIONS = """\

For this execution, do not call tools. Return one JSON object with exactly
these fields: intent, selected_tool_names, tool_input, missing_inputs,
user_message, and confidence. tool_input must be null or an object containing
pathParams, query, body, and headers. intent must be exactly one of
paypal_tool, rag_pipeline_search, system_search, memory_grep, memory_find, or
clarify. Use paypal_tool for every selected PayPal API tool; never put an
action description in intent. Set body to null when candidate metadata says
has_body=false, and never use an empty object as a placeholder body. Return
JSON only.
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
    return {"type": "json_object"}


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
                "path_parameters": list(tool.path_variables),
                "query_parameters": list(tool.query_params),
                "required_query_parameters": _required_query_parameters(tool),
                "fixed_query_parameters": _fixed_query_parameters(tool),
                "server_query_parameters": sorted(
                    SERVER_QUERY_PARAMETERS.get(tool.path, set())
                ),
                "header_parameters": [
                    name
                    for name in tool.headers
                    if name.lower() not in PROTECTED_HEADER_NAMES
                ],
                "body_fields": _body_fields(tool.body_template),
                "has_body": tool.body_template is not None,
                "is_mutating": tool.is_mutating,
            }
            for tool in candidates
            if tool.unsupported_reason is None
        ],
    }
    return json.dumps(payload, separators=(",", ":"))


def _tool_use_input(response: dict[str, Any]) -> dict[str, Any]:
    content_blocks = response.get("output", {}).get("message", {}).get("content") or []
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


def _validate_decision(
    decision: RouterDecision,
    candidates: list[ApiTool],
    user_input: str,
) -> None:
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
    if decision.intent in SUPPORT_TOOL_NAMES:
        if decision.selected_tool_names != [decision.intent]:
            raise RouterModelError("Router intent and support tool do not match.")
        if decision.tool_input is not None:
            raise RouterModelError("Support tools cannot include PayPal input.")
        decision.missing_inputs = []
        decision.user_message = SUPPORT_TOOL_MESSAGES[decision.intent]
        return
    if decision.intent == "clarify":
        if decision.selected_tool_names or decision.tool_input is not None:
            raise RouterModelError("Clarification cannot select a PayPal tool.")
        decision.missing_inputs = ["one unambiguous PayPal action"]
        decision.user_message = (
            "Please specify one PayPal action and include its required IDs, "
            "dates, and filters."
        )
        return
    if decision.intent != "paypal_tool":
        raise RouterModelError("Router returned an unsupported intent.")
    if len(decision.selected_tool_names) != 1:
        raise RouterModelError("Router must select exactly one PayPal tool.")
    if decision.selected_tool_names[0] in SUPPORT_TOOL_NAMES:
        raise RouterModelError("PayPal intent cannot select a support tool.")

    tool_by_name = {tool.tool_name: tool for tool in candidates}
    tool = tool_by_name[decision.selected_tool_names[0]]
    boundPath, missingPathInputs = _boundPathParameters(user_input, tool)
    boundQuery, missingQueryInputs = _bound_query_parameters(user_input, tool)
    if decision.tool_input is not None:
        for name, value in boundPath.items():
            decision.tool_input.path_params[name] = value
        for name, value in boundQuery.items():
            decision.tool_input.query[name] = value
    missingContractInputs: list[str] = [
        *missingPathInputs,
        *missingQueryInputs,
    ]
    if (
        tool.is_mutating
        and tool.body_template is not None
        and _routedBodyIsMissing(tool, decision.tool_input)
    ):
        missingContractInputs.append("request body")
    decision.missing_inputs = list(dict.fromkeys(missingContractInputs))
    if decision.missing_inputs:
        decision.user_message = missingInputMessage(decision.missing_inputs)
        return
    if decision.tool_input is None:
        raise RouterModelError("Router did not provide PayPal tool_input.")

    _validate_tool_input(tool, decision.tool_input, user_input)
    decision.user_message = "Selected the exact PayPal tool and request values."


def _routedBodyIsMissing(
    tool: ApiTool,
    toolInput: RoutedToolInput | None,
) -> bool:
    if toolInput is None:
        return True
    body: Any = toolInput.body
    template: Any = tool.body_template
    if isinstance(template, dict):
        return not isinstance(body, dict) or not body
    if isinstance(template, list):
        return not isinstance(body, list) or not body
    if isinstance(template, str):
        return not isinstance(body, str) or not body.strip()
    return body is None


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
    if _is_system_search(user_input, terms):
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
    selected_tool = _deterministic_tool(user_input, candidates)
    if selected_tool is None:
        return RouterDecision(
            intent="clarify",
            selected_tool_names=[],
            missing_inputs=["one unambiguous PayPal action"],
            user_message=(
                "Please specify one PayPal action and include its required "
                "IDs, dates, and filters."
            ),
            confidence=0.3,
        )

    tool_input, missing_inputs = _deterministic_tool_input(
        user_input,
        selected_tool,
    )
    return RouterDecision(
        intent="paypal_tool",
        selected_tool_names=[selected_tool.tool_name],
        tool_input=tool_input,
        missing_inputs=missing_inputs,
        user_message=(
            missingInputMessage(missing_inputs)
            if missing_inputs
            else "Selected the exact PayPal tool and request values."
        ),
        confidence=0.8 if not missing_inputs else 0.6,
    )


def missingInputMessage(missingInputs: list[str]) -> str:
    displayNames: list[str] = [
        (
            "the exact non-empty request body"
            if name in {"body", "request body"}
            else name
        )
        for name in missingInputs
    ]
    if len(displayNames) == 1:
        names: str = displayNames[0]
    else:
        names = ", ".join(displayNames[:-1]) + " and " + displayNames[-1]
    return f"I need {names} before calling PayPal."


def _multiStepDecision(userInput: str) -> RouterDecision | None:
    terms: set[str] = {
        match.group(0).lower().strip("._-")
        for match in WORD_PATTERN.finditer(userInput)
    }
    if terms & RAG_TERMS or not {"create", "send", "invoice"} <= terms:
        return None
    return RouterDecision(
        intent="clarify",
        selected_tool_names=[],
        missing_inputs=["complete draft invoice body"],
        user_message=(
            "Creating and sending an invoice requires two confirmed PayPal "
            "calls. Start a new request to create a draft invoice and include "
            "the complete body. After PayPal returns invoice_id, start a "
            "separate request to send that invoice."
        ),
        confidence=1.0,
    )


def _validationFallback(
    userInput: str,
    candidates: list[ApiTool],
    decision: RouterDecision,
) -> RouterDecision | None:
    if decision.intent != "paypal_tool" or len(decision.selected_tool_names) != 1:
        return None
    deterministicDecision: RouterDecision = _fallback_decision(
        userInput,
        candidates,
    )
    if (
        deterministicDecision.intent != "paypal_tool"
        or deterministicDecision.selected_tool_names
        != decision.selected_tool_names
    ):
        return None
    return deterministicDecision.model_copy(
        update={"confidence": min(decision.confidence, 0.8)}
    )


def _provider_error_decision() -> RouterDecision:
    return RouterDecision(
        intent="clarify",
        selected_tool_names=[],
        missing_inputs=["a verified PayPal tool selection"],
        user_message=(
            "I could not safely verify one exact PayPal request. Please restate "
            "the action with its required IDs, dates, and filters."
        ),
        confidence=0.0,
    )


def _decision_trace_metadata(decision: RouterDecision) -> dict[str, Any]:
    return {
        "intent": decision.intent,
        "selected_tool_names": decision.selected_tool_names,
        "missing_input_names": decision.missing_inputs,
        "has_tool_input": decision.tool_input is not None,
        "confidence": decision.confidence,
    }


def _body_fields(body_template: Any) -> list[str]:
    if not isinstance(body_template, dict):
        return []
    return [str(name) for name in body_template]


def _required_query_parameters(tool: ApiTool) -> list[str]:
    parameters = [
        name
        for name, value in tool.query_params.items()
        if VARIABLE_PATTERN.fullmatch(value)
    ]
    for name in REQUIRED_DATE_QUERY_PARAMS.get(tool.path, ()):
        if name not in parameters:
            parameters.append(name)
    return parameters


def _fixed_query_parameters(tool: ApiTool) -> dict[str, str]:
    return {
        name: value
        for name, value in tool.query_params.items()
        if name in FIXED_QUERY_PARAMETER_NAMES
        and value
        and not VARIABLE_PATTERN.fullmatch(value)
    }


def _is_system_search(user_input: str, terms: set[str]) -> bool:
    normalized_input = " ".join(
        match.group(0).lower() for match in WORD_PATTERN.finditer(user_input)
    )
    return bool(terms & SYSTEM_TERMS) or any(
        phrase in normalized_input for phrase in SYSTEM_PHRASES
    )


def _deterministic_tool(
    user_input: str,
    candidates: list[ApiTool],
) -> ApiTool | None:
    user_terms = _tool_terms(user_input)
    matches: list[tuple[int, ApiTool]] = []
    for tool in candidates:
        if tool.unsupported_reason is not None:
            continue
        display_terms = _tool_terms(tool.display_name)
        if display_terms and display_terms <= user_terms:
            matches.append((len(display_terms), tool))
    if not matches:
        return None

    best_score = max(score for score, _tool in matches)
    best_tools = [tool for score, tool in matches if score == best_score]
    if len(best_tools) != 1:
        return None
    return best_tools[0]


def _tool_terms(value: str) -> set[str]:
    terms: set[str] = set()
    for match in WORD_PATTERN.finditer(value.lower()):
        term = match.group(0).strip("._-")
        if term.endswith("s") and len(term) > 3:
            term = term[:-1]
        term = TOOL_TERM_ALIASES.get(term, term)
        if len(term) > 1 and term not in TOOL_TERM_STOP_WORDS:
            terms.add(term)
    return terms


def _deterministic_tool_input(
    user_input: str,
    tool: ApiTool,
) -> tuple[RoutedToolInput, list[str]]:
    pathParams, missingInputs = _boundPathParameters(user_input, tool)
    query, missing_query_inputs = _bound_query_parameters(user_input, tool)
    missingInputs.extend(missing_query_inputs)
    if tool.is_mutating and tool.body_template is not None:
        missingInputs.append("request body")

    return RoutedToolInput(pathParams=pathParams, query=query), missingInputs


def _boundPathParameters(
    userInput: str,
    tool: ApiTool,
) -> tuple[dict[str, Any], list[str]]:
    pathParams: dict[str, Any] = {}
    missingInputs: list[str] = []
    for parameterName in tool.path_variables:
        value: str | None = _identifier_parameter_value(userInput, parameterName)
        if value is None:
            missingInputs.append(parameterName)
        else:
            pathParams[parameterName] = value
    return pathParams, missingInputs


def _bound_query_parameters(
    user_input: str,
    tool: ApiTool,
) -> tuple[dict[str, Any], list[str]]:
    query: dict[str, Any] = dict(_fixed_query_parameters(tool))
    missing_inputs: list[str] = []
    for parameter_name, template_value in tool.query_params.items():
        if not VARIABLE_PATTERN.fullmatch(template_value):
            continue
        value = _identifier_parameter_value(user_input, parameter_name)
        if value is None:
            missing_inputs.append(parameter_name)
        else:
            query[parameter_name] = value

    date_parameters = REQUIRED_DATE_QUERY_PARAMS.get(tool.path, ())
    dates = DATE_PATTERN.findall(user_input)
    relativeDates: tuple[str, str] | None = _relativeDateRange(user_input)
    for index, parameter_name in enumerate(date_parameters):
        if index < len(dates):
            query[parameter_name] = _rfc3339_date(
                dates[index],
                is_end=parameter_name.startswith("end_"),
            )
        elif relativeDates is not None and index < len(relativeDates):
            query[parameter_name] = relativeDates[index]
        else:
            missing_inputs.append(parameter_name)
    query.update(SERVER_QUERY_DEFAULTS.get(tool.path, {}))

    return query, missing_inputs


def _rfc3339_date(value: str, *, is_end: bool) -> str:
    if len(value) != 10:
        return value
    time = "23:59:59Z" if is_end else "00:00:00Z"
    return f"{value}T{time}"


def _relativeDateRange(userInput: str) -> tuple[str, str] | None:
    if re.search(r"\blast\s+month\b", userInput, re.IGNORECASE) is None:
        return None
    return _previousMonthDates()


def _previousMonthDates(referenceDate: date | None = None) -> tuple[str, str]:
    currentDate: date = referenceDate or datetime.now(UTC).date()
    firstCurrentMonth: date = currentDate.replace(day=1)
    lastPreviousMonth: date = firstCurrentMonth - timedelta(days=1)
    firstPreviousMonth: date = lastPreviousMonth.replace(day=1)
    return (
        f"{firstPreviousMonth.isoformat()}T00:00:00Z",
        f"{lastPreviousMonth.isoformat()}T23:59:59Z",
    )


def _identifier_parameter_value(
    user_input: str,
    parameter_name: str,
) -> str | None:
    entity_name = parameter_name.removesuffix("_id").replace("_", " ")
    explicit_name = parameter_name.replace("_", " ")
    if explicit_name != entity_name:
        value = _value_after_label(
            user_input,
            explicit_name,
            require_identifier_shape=False,
        )
        if value is not None:
            return value
    return _value_after_label(
        user_input,
        entity_name,
        require_identifier_shape=True,
    )


def _value_after_label(
    user_input: str,
    label: str,
    *,
    require_identifier_shape: bool,
) -> str | None:
    label_pattern = r"\s+".join(re.escape(part) for part in label.split())
    entity_pattern = re.compile(rf"\b{label_pattern}\b", re.IGNORECASE)
    for match in entity_pattern.finditer(user_input):
        remainder = user_input[match.end() : match.end() + 100]
        for token_match in WORD_PATTERN.finditer(remainder):
            token = token_match.group(0).strip("._-")
            if token.lower() in IDENTIFIER_SKIP_WORDS:
                continue
            if (
                not require_identifier_shape
                or any(character.isdigit() for character in token)
                or (len(token) >= 6 and token.isupper())
            ):
                return token_match.group(0).strip(".,;:!?'\"")
            break
    return None


def _validate_tool_input(
    tool: ApiTool,
    tool_input: RoutedToolInput,
    user_input: str,
) -> None:
    if set(tool_input.path_params) != set(tool.path_variables):
        raise RouterModelError("Router did not provide the exact path parameters.")
    if not tool.is_mutating and tool_input.body is not None:
        raise RouterModelError("Read-only PayPal tools cannot include a body.")
    if PROTECTED_HEADER_NAMES & {name.lower() for name in tool_input.headers}:
        raise RouterModelError("Router supplied a protected authentication header.")

    allowed_query_names = set(tool.query_params) | SERVER_QUERY_PARAMETERS.get(
        tool.path,
        set(),
    )
    unknown_query_names = set(tool_input.query) - allowed_query_names
    if unknown_query_names:
        raise RouterModelError(
            "Router supplied unsupported query parameters: "
            + ", ".join(sorted(unknown_query_names))
        )
    missing_query_names = set(_required_query_parameters(tool)) - set(tool_input.query)
    if missing_query_names:
        raise RouterModelError(
            "Router did not provide required query parameters: "
            + ", ".join(sorted(missing_query_names))
        )

    for value in tool_input.path_params.values():
        if not _is_grounded_value(value, user_input):
            raise RouterModelError(
                "Router supplied a request value that was not in the user input."
            )
    fixed_query = _fixed_query_parameters(tool)
    server_defaults = SERVER_QUERY_DEFAULTS.get(tool.path, {})
    boundQuery, _missingInputs = _bound_query_parameters(user_input, tool)
    for name, value in tool_input.query.items():
        if name in fixed_query:
            if str(value) != fixed_query[name]:
                raise RouterModelError(f"Router changed fixed query parameter: {name}")
            continue
        if name in server_defaults and str(value) == str(server_defaults[name]):
            continue
        if name in boundQuery and str(value) == str(boundQuery[name]):
            continue
        isGrounded = _is_grounded_value(value, user_input)
        if name in {"start_date", "end_date", "start_time", "end_time"}:
            isGrounded = isGrounded or (
                isinstance(value, str) and _is_grounded_value(value[:10], user_input)
            )
        if not isGrounded:
            raise RouterModelError(
                "Router supplied a request value that was not in the user input."
            )
    for value in tool_input.headers.values():
        if not _is_grounded_value(value, user_input):
            raise RouterModelError(
                "Router supplied a request value that was not in the user input."
            )
    for value in _scalar_values(tool_input.body):
        if not _is_grounded_value(value, user_input):
            raise RouterModelError(
                "Router supplied a body value that was not in the user input."
            )


def _is_grounded_value(value: Any, user_input: str) -> bool:
    if not isinstance(value, str | int | float):
        return False
    text_value = str(value).strip()
    if not text_value:
        return False
    value_pattern = re.compile(
        rf"(?<![A-Za-z0-9._-]){re.escape(text_value)}"
        r"(?![A-Za-z0-9._-])",
        re.IGNORECASE,
    )
    return value_pattern.search(user_input) is not None


def _scalar_values(value: Any) -> list[str | int | float]:
    if isinstance(value, dict):
        values: list[str | int | float] = []
        for child in value.values():
            values.extend(_scalar_values(child))
        return values
    if isinstance(value, list):
        values = []
        for child in value:
            values.extend(_scalar_values(child))
        return values
    if isinstance(value, str | int | float):
        return [value]
    return []
