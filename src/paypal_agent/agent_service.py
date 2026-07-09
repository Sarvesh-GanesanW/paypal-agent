from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any, Literal, NotRequired, TypedDict, cast

import httpx
from langgraph.graph import END, START, StateGraph

from paypal_agent.bedrock_agents import BedrockAgentStack
from paypal_agent.config import Settings, settings
from paypal_agent.hybrid_rag import HybridRagPipeline
from paypal_agent.local_memory import LocalMemoryStore
from paypal_agent.model_router import (
    BedrockRuntimeClient,
    RouteResult,
    SmallModelRouter,
)
from paypal_agent.package_assets import (
    defaultKnowledgeBasePath,
    resolvePostmanCollectionPath,
)
from paypal_agent.paypal_client import PayPalClient, ToolCallInput
from paypal_agent.postman import ApiTool
from paypal_agent.system_search import RequestLog, SystemSearch
from paypal_agent.tool_registry import ToolRegistry
from paypal_agent.tracing import traceRun

GraphRoute = Literal[
    "rag",
    "system",
    "memory_grep",
    "memory_find",
    "clarify",
    "paypal",
]
GraphNodeName = Literal[
    "shortlist_tools",
    "route_request",
    "run_rag_tool",
    "run_system_search",
    "run_memory_grep",
    "run_memory_find",
    "prepare_clarification",
    "prepare_paypal_plan",
    "orchestrate_answer",
    "record_request",
]


class ChatGraphState(TypedDict):
    user_input: str
    conversation_id: str
    candidates: NotRequired[list[ApiTool]]
    route_result: NotRequired[RouteResult]
    fallback_answer: NotRequired[str]
    route_payload: NotRequired[dict[str, Any]]
    answer: NotRequired[str]
    result: NotRequired[dict[str, Any]]


class ChatStreamEvent(TypedDict):
    event: Literal["node", "result"]
    node: NotRequired[GraphNodeName]
    result: NotRequired[dict[str, Any]]


class AgentService:
    def __init__(
        self,
        app_settings: Settings = settings,
        *,
        paypal_http_client: httpx.AsyncClient | None = None,
        bedrock_client: BedrockRuntimeClient | None = None,
        knowledge_dir: Path | None = None,
    ) -> None:
        self.settings = app_settings
        collectionPath = resolvePostmanCollectionPath(
            app_settings.paypal_postman_collection_path
        )
        self.registry = ToolRegistry(collectionPath)
        self.paypal_client = PayPalClient(
            app_settings,
            http_client=paypal_http_client,
        )
        self.router = SmallModelRouter(
            app_settings,
            bedrock_client=bedrock_client,
        )
        self.agent_stack = BedrockAgentStack(
            app_settings,
            bedrock_client=bedrock_client,
        )
        self.request_log = RequestLog()
        self.memory = LocalMemoryStore(app_settings.memory_dir)
        self.rag = HybridRagPipeline(
            app_settings,
            knowledge_dir or defaultKnowledgeBasePath(),
        )
        self.system_search = SystemSearch(self.registry, self.request_log)
        self.chat_graph: Any = self._build_chat_graph()

    async def chat(self, user_input: str, conversation_id: str) -> dict[str, Any]:
        with traceRun(
            self.settings,
            "paypal_agent_chat",
            inputs={
                "conversation_id": conversation_id,
                "user_input": user_input,
            },
            metadata={
                "paypal_tool_count": len(self.registry.tools),
                "model_provider": self.settings.model_provider,
                "router_model": self.settings.router_model_id,
                "main_model": self.settings.main_model_id,
                "subagent_model": self.settings.subagent_model_id,
            },
            tags=["chat", "paypal-agent"],
        ) as chat_trace:
            finalState = await self.chat_graph.ainvoke(
                {
                    "user_input": user_input,
                    "conversation_id": conversation_id,
                }
            )
            result = finalState["result"]
            route_result = finalState["route_result"]
            chat_trace.end(
                {
                    "intent": route_result.decision.intent,
                    "selected_tool_names": route_result.decision.selected_tool_names,
                    "router_mode": route_result.mode,
                    "answer": result["answer"],
                }
            )
            return result

    async def stream_chat(
        self,
        user_input: str,
        conversation_id: str,
    ) -> AsyncIterator[ChatStreamEvent]:
        with traceRun(
            self.settings,
            "paypal_agent_chat",
            inputs={
                "conversation_id": conversation_id,
                "user_input": user_input,
            },
            metadata={
                "paypal_tool_count": len(self.registry.tools),
                "model_provider": self.settings.model_provider,
                "router_model": self.settings.router_model_id,
                "main_model": self.settings.main_model_id,
                "subagent_model": self.settings.subagent_model_id,
                "orchestration": "langgraph",
            },
            tags=["chat", "paypal-agent", "langgraph"],
        ) as chat_trace:
            finalResult: dict[str, Any] | None = None
            finalRoute: RouteResult | None = None
            async for update in self.chat_graph.astream(
                {
                    "user_input": user_input,
                    "conversation_id": conversation_id,
                },
                stream_mode="updates",
            ):
                if not isinstance(update, dict):
                    continue
                for nodeName, nodeUpdate in update.items():
                    if nodeName == "__end__":
                        continue
                    yield ChatStreamEvent(
                        event="node",
                        node=cast(GraphNodeName, nodeName),
                    )
                    if isinstance(nodeUpdate, dict):
                        if "result" in nodeUpdate:
                            finalResult = cast(
                                dict[str, Any],
                                nodeUpdate["result"],
                            )
                        if "route_result" in nodeUpdate:
                            finalRoute = cast(
                                RouteResult,
                                nodeUpdate["route_result"],
                            )
            if finalResult is None:
                finalState = await self.chat_graph.ainvoke(
                    {
                        "user_input": user_input,
                        "conversation_id": conversation_id,
                    }
                )
                finalResult = finalState["result"]
                finalRoute = finalState["route_result"]
            assert finalResult is not None
            if finalRoute is not None:
                chat_trace.end(
                    {
                        "intent": finalRoute.decision.intent,
                        "selected_tool_names": (
                            finalRoute.decision.selected_tool_names
                        ),
                        "router_mode": finalRoute.mode,
                        "answer": finalResult["answer"],
                    }
                )
            yield ChatStreamEvent(event="result", result=finalResult)

    def _build_chat_graph(self) -> Any:
        graph = StateGraph(ChatGraphState)
        graph.add_node("shortlist_tools", self._graph_shortlist_tools)
        graph.add_node("route_request", self._graph_route_request)
        graph.add_node("run_rag_tool", self._graph_run_rag_tool)
        graph.add_node("run_system_search", self._graph_run_system_search)
        graph.add_node("run_memory_grep", self._graph_run_memory_grep)
        graph.add_node("run_memory_find", self._graph_run_memory_find)
        graph.add_node("prepare_clarification", self._graph_prepare_clarification)
        graph.add_node("prepare_paypal_plan", self._graph_prepare_paypal_plan)
        graph.add_node("orchestrate_answer", self._graph_orchestrate_answer)
        graph.add_node("record_request", self._graph_record_request)

        graph.add_edge(START, "shortlist_tools")
        graph.add_edge("shortlist_tools", "route_request")
        graph.add_conditional_edges(
            "route_request",
            self._graph_route_key,
            {
                "rag": "run_rag_tool",
                "system": "run_system_search",
                "memory_grep": "run_memory_grep",
                "memory_find": "run_memory_find",
                "clarify": "prepare_clarification",
                "paypal": "prepare_paypal_plan",
            },
        )
        graph.add_edge("run_rag_tool", "orchestrate_answer")
        graph.add_edge("run_system_search", "orchestrate_answer")
        graph.add_edge("run_memory_grep", "orchestrate_answer")
        graph.add_edge("run_memory_find", "orchestrate_answer")
        graph.add_edge("prepare_clarification", "orchestrate_answer")
        graph.add_edge("prepare_paypal_plan", "orchestrate_answer")
        graph.add_edge("orchestrate_answer", "record_request")
        graph.add_edge("record_request", END)
        return graph.compile(name="paypal_agent_chat_graph")

    def _graph_shortlist_tools(
        self,
        state: ChatGraphState,
    ) -> dict[str, list[ApiTool]]:
        return {"candidates": self._shortlist_tools(state["user_input"])}

    async def _graph_route_request(
        self,
        state: ChatGraphState,
    ) -> dict[str, RouteResult]:
        return {
            "route_result": await self._route_request(
                state["user_input"],
                self._state_candidates(state),
            )
        }

    def _graph_route_key(self, state: ChatGraphState) -> GraphRoute:
        intent = self._state_route_result(state).decision.intent
        if intent == "rag_pipeline_search":
            return "rag"
        if intent == "system_search":
            return "system"
        if intent == "memory_grep":
            return "memory_grep"
        if intent == "memory_find":
            return "memory_find"
        if intent == "clarify":
            return "clarify"
        return "paypal"

    def _graph_run_rag_tool(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        fallbackAnswer, routePayload = self._rag_answer(state["user_input"])
        return {"fallback_answer": fallbackAnswer, "route_payload": routePayload}

    def _graph_run_system_search(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        fallbackAnswer, routePayload = self._system_search_answer(
            state["user_input"]
        )
        return {"fallback_answer": fallbackAnswer, "route_payload": routePayload}

    def _graph_run_memory_grep(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        fallbackAnswer, routePayload = self._memory_grep_answer(
            state["user_input"]
        )
        return {"fallback_answer": fallbackAnswer, "route_payload": routePayload}

    def _graph_run_memory_find(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        fallbackAnswer, routePayload = self._memory_find_answer(
            state["user_input"]
        )
        return {"fallback_answer": fallbackAnswer, "route_payload": routePayload}

    def _graph_prepare_clarification(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        decision = self._state_route_result(state).decision
        return {
            "fallback_answer": decision.user_message,
            "route_payload": {"missing_inputs": decision.missing_inputs},
        }

    async def _graph_prepare_paypal_plan(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        fallbackAnswer, routePayload = await self._paypal_answer(
            self._state_route_result(state).decision.selected_tool_names
        )
        return {"fallback_answer": fallbackAnswer, "route_payload": routePayload}

    async def _graph_orchestrate_answer(
        self,
        state: ChatGraphState,
    ) -> dict[str, str]:
        answer = await self._orchestrate_answer(
            state["user_input"],
            self._state_route_result(state),
            self._state_route_payload(state),
            self._state_fallback_answer(state),
        )
        return {"answer": answer}

    def _graph_record_request(
        self,
        state: ChatGraphState,
    ) -> dict[str, dict[str, Any]]:
        routeResult = self._state_route_result(state)
        candidates = self._state_candidates(state)
        self.request_log.append(
            {
                "conversation_id": state["conversation_id"],
                "user_input": state["user_input"],
                "intent": routeResult.decision.intent,
                "selected_tool_names": routeResult.decision.selected_tool_names,
                "router_mode": routeResult.mode,
            }
        )
        self.memory.append(
            "chat",
            {
                "conversation_id": state["conversation_id"],
                "user_input": state["user_input"],
                "answer": self._state_answer(state),
                "intent": routeResult.decision.intent,
                "selected_tool_names": routeResult.decision.selected_tool_names,
                "router_mode": routeResult.mode,
            },
        )
        return {
            "result": {
                "answer": self._state_answer(state),
                "selected_tool_names": routeResult.decision.selected_tool_names,
                "tool_results": self._state_route_payload(state).get(
                    "tool_call_results",
                    [],
                ),
                "router_decision": routeResult.decision.model_dump(),
                "metadata": {
                    "router_mode": routeResult.mode,
                    "router_error": routeResult.error,
                    "candidate_tools": [tool.to_dict() for tool in candidates],
                    "tool_count": len(self.registry.tools),
                    "orchestration": "langgraph",
                    "graph": "paypal_agent_chat_graph",
                },
            }
        }

    def _state_candidates(self, state: ChatGraphState) -> list[ApiTool]:
        return cast(list[ApiTool], state.get("candidates", []))

    def _state_route_result(self, state: ChatGraphState) -> RouteResult:
        routeResult = state.get("route_result")
        if routeResult is None:
            raise RuntimeError("LangGraph state is missing route_result.")
        return routeResult

    def _state_route_payload(self, state: ChatGraphState) -> dict[str, Any]:
        return cast(dict[str, Any], state.get("route_payload", {}))

    def _state_fallback_answer(self, state: ChatGraphState) -> str:
        return str(state.get("fallback_answer", ""))

    def _state_answer(self, state: ChatGraphState) -> str:
        return str(state.get("answer", ""))

    def _shortlist_tools(self, user_input: str) -> list[ApiTool]:
        with traceRun(
            self.settings,
            "tool_registry_shortlist",
            "retriever",
            inputs={"query": user_input, "limit": self.settings.max_selected_tools},
            tags=["router", "shortlist"],
        ) as trace:
            candidates = self.registry.search(
                user_input,
                limit=self.settings.max_selected_tools,
            )
            trace.end(
                {
                    "candidate_tool_names": [
                        tool.tool_name for tool in candidates
                    ],
                    "candidate_count": len(candidates),
                }
            )
            return candidates

    async def _route_request(
        self,
        user_input: str,
        candidates: list[ApiTool],
    ) -> RouteResult:
        with traceRun(
            self.settings,
            "small_model_router",
            inputs={
                "user_input": user_input,
                "candidate_tool_names": [tool.tool_name for tool in candidates],
            },
            metadata={
                "model_provider": self.settings.model_provider,
                "router_model": self.settings.router_model_id,
            },
            tags=["router"],
        ) as trace:
            route_result = await self.router.route(user_input, candidates)
            trace.end(
                {
                    "decision": route_result.decision.model_dump(),
                    "mode": route_result.mode,
                    "error": route_result.error,
                }
            )
            return route_result

    async def _orchestrate_answer(
        self,
        user_input: str,
        route_result: RouteResult,
        route_payload: dict[str, Any],
        fallback_answer: str,
    ) -> str:
        with traceRun(
            self.settings,
            "main_orchestrator_answer",
            inputs={
                "user_input": user_input,
                "router_decision": route_result.decision.model_dump(),
                "route_payload": route_payload,
            },
            metadata={
                "model_provider": self.settings.model_provider,
                "main_model": self.settings.main_model_id,
            },
            tags=["orchestrator"],
        ) as trace:
            answer = await self.agent_stack.answer(
                user_input,
                route_result,
                route_payload,
                fallback_answer,
            )
            trace.end({"answer": answer})
            return answer

    async def call_tool(
        self,
        tool_name: str,
        payload: ToolCallInput,
    ) -> dict[str, Any]:
        with traceRun(
            self.settings,
            "paypal_tool_execution",
            "tool",
            inputs={
                "tool_name": tool_name,
                "payload": payload.model_dump(by_alias=True),
            },
            tags=["paypal-tool"],
        ) as trace:
            tool = self.registry.get(tool_name)
            result = await self.paypal_client.execute(tool, payload)
            self.request_log.append(
                {
                    "tool_name": tool_name,
                    "status": result["status"],
                    "status_code": result.get("status_code"),
                }
            )
            self.memory.append(
                "paypal_tool",
                {
                    "tool_name": tool_name,
                    "status": result["status"],
                    "status_code": result.get("status_code"),
                    "request": result.get("request"),
                    "response": result.get("response"),
                },
            )
            trace.end(
                {
                    "status": result["status"],
                    "status_code": result.get("status_code"),
                }
            )
            return result

    def catalog(self) -> dict[str, Any]:
        catalog = self.registry.catalog()
        catalog["support_tools"] = [
            {
                "tool_name": "rag_pipeline_search",
                "description": "Search local docs and operating guidance.",
            },
            {
                "tool_name": "system_search",
                "description": "Search tool capabilities and recent requests.",
            },
            {
                "tool_name": "memory_grep",
                "description": "Grep local JSONL memory with a regex pattern.",
            },
            {
                "tool_name": "memory_find",
                "description": "Find local JSONL memory entries by keywords.",
            },
        ]
        catalog["total_tool_count"] = catalog["tool_count"] + 4
        return catalog

    def search_tools(self, query: str, *, limit: int) -> list[dict[str, Any]]:
        with traceRun(
            self.settings,
            "tool_catalog_search",
            "retriever",
            inputs={"query": query, "limit": limit},
            tags=["system-search"],
        ) as trace:
            tools = [
                tool.to_dict()
                for tool in self.registry.search(query, limit=limit)
            ]
            trace.end(
                {
                    "tool_names": [tool["tool_name"] for tool in tools],
                    "tool_count": len(tools),
                }
            )
            return tools

    def _rag_answer(self, user_input: str) -> tuple[str, dict[str, Any]]:
        with traceRun(
            self.settings,
            "rag_pipeline_tool",
            "tool",
            inputs={"query": user_input},
            tags=["rag"],
        ) as trace:
            result = self.rag.search(user_input)
            if not result["matches"]:
                trace.end({"match_count": 0})
                return "No matching local documentation was found.", result
            answer = "\n".join(
                f"{match['source']}: {match['snippet']}"
                for match in result["matches"]
            )
            trace.end(
                {
                    "mode": result.get("mode"),
                    "match_count": len(result["matches"]),
                }
            )
            return answer, result

    def _system_search_answer(self, user_input: str) -> tuple[str, dict[str, Any]]:
        with traceRun(
            self.settings,
            "system_search_tool",
            "tool",
            inputs={"query": user_input},
            tags=["system-search"],
        ) as trace:
            result = self.system_search.search(user_input)
            trace.end(
                {
                    "matching_tool_count": len(result["matching_tools"]),
                    "matching_request_count": len(
                        result["matching_requests"]
                    ),
                }
            )
            return (
                "Matching tools: "
                + ", ".join(
                    tool["tool_name"] for tool in result["matching_tools"][:5]
                )
            ), result

    def _memory_grep_answer(self, user_input: str) -> tuple[str, dict[str, Any]]:
        with traceRun(
            self.settings,
            "memory_grep_tool",
            "tool",
            inputs={"query": user_input},
            tags=["memory"],
        ) as trace:
            pattern = _memory_query(user_input, command="grep")
            matches = self.memory.grep(pattern)
            result = {
                "status": "success",
                "mode": "jsonl_grep",
                "query": pattern,
                "matches": matches,
            }
            trace.end({"match_count": len(matches)})
            return _format_memory_matches("Memory grep", matches), result

    def _memory_find_answer(self, user_input: str) -> tuple[str, dict[str, Any]]:
        with traceRun(
            self.settings,
            "memory_find_tool",
            "tool",
            inputs={"query": user_input},
            tags=["memory"],
        ) as trace:
            query = _memory_query(user_input, command="find")
            matches = self.memory.find(query)
            result = {
                "status": "success",
                "mode": "jsonl_find",
                "query": query,
                "matches": matches,
            }
            trace.end({"match_count": len(matches)})
            return _format_memory_matches("Memory find", matches), result

    async def _paypal_answer(
        self,
        selected_tool_names: list[str],
    ) -> tuple[str, dict[str, Any]]:
        selectedTools = [
            self.registry.get(tool_name)
            for tool_name in selected_tool_names
            if tool_name in self.registry.by_name
        ]
        toolResults: list[dict[str, Any]] = []
        executionTool = _execution_tool(selectedTools)
        if executionTool is not None:
            tool = executionTool
            payload = _auto_tool_payload(tool)
            try:
                result = await self.paypal_client.execute(
                    tool,
                    payload,
                    force_request=True,
                )
            except Exception as exc:
                result = {
                    "status": "client_error",
                    "status_code": None,
                    "tool": tool.to_dict(),
                    "error": str(exc),
                }
            toolResults.append(result)

        return _format_paypal_tool_results(selectedTools, toolResults), {
            "selected_tools": [tool.to_dict() for tool in selectedTools],
            "tool_call_results": toolResults,
        }

    def _paypal_plan(self, selected_tool_names: list[str]) -> str:
        if not selected_tool_names:
            return "No PayPal tool matched the request."
        lines: list[str] = []
        for tool_name in selected_tool_names:
            if tool_name not in self.registry.by_name:
                continue
            tool = self.registry.get(tool_name)
            required = ", ".join(tool.path_variables) or "none"
            lines.append(
                f"- {tool.tool_name}: {tool.method} {tool.path}; "
                f"required path params: {required}"
            )
        return "Selected PayPal tools:\n" + "\n".join(lines)


def _memory_query(user_input: str, *, command: str) -> str:
    lowered = user_input.lower()
    marker = command.lower()
    if marker in lowered:
        index = lowered.find(marker) + len(marker)
        remainder = user_input[index:].strip(" :\"'")
        if remainder:
            return remainder
    stop_terms = {
        "find",
        "grep",
        "memory",
        "memories",
        "remember",
        "recall",
        "previous",
        "prior",
        "local",
        "jsonl",
    }
    terms = [
        term.strip(".,:;?!\"'").lower()
        for term in user_input.split()
        if term.strip(".,:;?!\"'").lower() not in stop_terms
    ]
    return " ".join(terms) or user_input


def _auto_tool_payload(tool: ApiTool) -> ToolCallInput:
    return ToolCallInput(
        pathParams={
            name: f"missing_{name}"
            for name in tool.path_variables
        }
    )


def _execution_tool(selectedTools: list[ApiTool]) -> ApiTool | None:
    for tool in selectedTools:
        if not tool.is_mutating:
            return tool
    if not selectedTools:
        return None
    return selectedTools[0]


def _format_paypal_tool_results(
    selectedTools: list[ApiTool],
    toolResults: list[dict[str, Any]],
) -> str:
    if not selectedTools:
        return "No PayPal tool matched the request."
    if not toolResults:
        return "Selected PayPal tools:\n" + _paypal_tool_lines(selectedTools)

    lines = ["Executed PayPal tool call:"]
    for result in toolResults:
        tool = result.get("tool", {})
        toolName = tool.get("tool_name", "unknown_tool")
        method = tool.get("method", "UNKNOWN")
        path = tool.get("path", "")
        statusCode = result.get("status_code")
        status = result.get("status")
        lines.append(
            f"- {toolName}: {method} {path}; "
            f"status={status}; status_code={statusCode}"
        )
        if result.get("error"):
            lines.append(f"  error={result['error']}")
    return "\n".join(lines)


def _paypal_tool_lines(selectedTools: list[ApiTool]) -> str:
    lines: list[str] = []
    for tool in selectedTools:
        required = ", ".join(tool.path_variables) or "none"
        lines.append(
            f"- {tool.tool_name}: {tool.method} {tool.path}; "
            f"required path params: {required}"
        )
    return "\n".join(lines)


def _format_memory_matches(
    title: str,
    matches: list[dict[str, Any]],
) -> str:
    if not matches:
        return f"{title}: no matching local JSONL memory entries found."
    lines = [f"{title} matches:"]
    for match in matches[:5]:
        event = match.get("event", {})
        if not isinstance(event, dict):
            continue
        summary = event.get("user_input") or event.get("tool_name") or event
        lines.append(
            f"- {match['file']}:{match['line_number']} "
            f"{event.get('event_type', 'memory')}: {summary}"
        )
    return "\n".join(lines)
