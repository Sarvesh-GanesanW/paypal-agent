from __future__ import annotations

import json
import uuid
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
    RoutedToolInput,
    RouterDecision,
    RouteResult,
    SmallModelRouter,
)
from paypal_agent.package_assets import (
    defaultKnowledgeBasePath,
    resolvePostmanCollectionPath,
)
from paypal_agent.paypal_client import (
    ClientInputError,
    PayPalClient,
    ToolCallInput,
)
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
                "conversation_id_length": len(conversation_id),
                "user_input_length": len(user_input),
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
                    "answer_length": len(result["answer"]),
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
                "conversation_id_length": len(conversation_id),
                "user_input_length": len(user_input),
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
                        "answer_length": len(finalResult["answer"]),
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
        routeResult: RouteResult = await self._route_request(
            state["user_input"],
            self._state_candidates(state),
        )
        return {
            "route_result": self._requireMutationBody(routeResult),
        }

    def _requireMutationBody(self, routeResult: RouteResult) -> RouteResult:
        decision: RouterDecision = routeResult.decision
        if len(decision.selected_tool_names) != 1 or decision.tool_input is None:
            return routeResult
        tool: ApiTool = self.registry.get(decision.selected_tool_names[0])
        if not tool.is_mutating or not _mutationBodyIsMissing(
            tool,
            decision.tool_input.body,
        ):
            return routeResult
        missingInputs: list[str] = list(decision.missing_inputs)
        if "body" not in missingInputs:
            missingInputs.append("body")
        updatedDecision: RouterDecision = decision.model_copy(
            update={
                "missing_inputs": missingInputs,
                "user_message": (
                    "I need the exact non-empty request body before "
                    "preparing this mutating PayPal call."
                ),
            }
        )
        return RouteResult(
            decision=updatedDecision,
            mode=routeResult.mode,
            error=routeResult.error,
        )

    def _graph_route_key(self, state: ChatGraphState) -> GraphRoute:
        routeResult = self._state_route_result(state)
        decision = routeResult.decision
        if routeResult.error or decision.missing_inputs or decision.confidence < 0.5:
            return "clarify"
        intent = decision.intent
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
        if len(decision.selected_tool_names) != 1 or decision.tool_input is None:
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
        fallbackAnswer, routePayload = self._system_search_answer(state["user_input"])
        return {"fallback_answer": fallbackAnswer, "route_payload": routePayload}

    def _graph_run_memory_grep(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        fallbackAnswer, routePayload = self._memory_grep_answer(state["user_input"])
        return {"fallback_answer": fallbackAnswer, "route_payload": routePayload}

    def _graph_run_memory_find(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        fallbackAnswer, routePayload = self._memory_find_answer(state["user_input"])
        return {"fallback_answer": fallbackAnswer, "route_payload": routePayload}

    def _graph_prepare_clarification(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        decision = self._state_route_result(state).decision
        return {
            "fallback_answer": decision.user_message,
            "route_payload": {
                "missing_inputs": decision.missing_inputs,
                "router_decision": decision.model_dump(by_alias=True),
                "router_error": self._state_route_result(state).error,
            },
        }

    async def _graph_prepare_paypal_plan(
        self,
        state: ChatGraphState,
    ) -> dict[str, Any]:
        fallbackAnswer, routePayload = await self._paypal_answer(
            self._state_route_result(state).decision
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
                "event_type": "chat",
                "conversation_id_length": len(state["conversation_id"]),
                "user_input_length": len(state["user_input"]),
                "intent": routeResult.decision.intent,
                "selected_tool_names": routeResult.decision.selected_tool_names,
                "router_mode": routeResult.mode,
            }
        )
        memoryEvent: dict[str, Any] = {
            "conversation_id_length": len(state["conversation_id"]),
            "user_input_length": len(state["user_input"]),
            "intent": routeResult.decision.intent,
            "selected_tool_names": routeResult.decision.selected_tool_names,
            "router_mode": routeResult.mode,
        }
        toolResults = self._state_route_payload(state).get(
            "tool_call_results",
            [],
        )
        memoryEvent["tool_results"] = [
            _tool_result_metadata(result)
            for result in toolResults
            if isinstance(result, dict)
        ]
        try:
            self.memory.append("chat", memoryEvent)
        except OSError:
            pass
        return {
            "result": {
                "answer": self._state_answer(state),
                "selected_tool_names": routeResult.decision.selected_tool_names,
                "tool_results": self._state_route_payload(state).get(
                    "tool_call_results",
                    [],
                ),
                "router_decision": routeResult.decision.model_dump(),
                "required_direct_call": self._state_route_payload(state).get(
                    "required_direct_call"
                ),
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
            inputs={
                "query_length": len(user_input),
                "limit": self.settings.max_selected_tools,
            },
            tags=["router", "shortlist"],
        ) as trace:
            candidates = self.registry.search(
                user_input,
                limit=self.settings.max_selected_tools,
            )
            trace.end(
                {
                    "candidate_tool_names": [tool.tool_name for tool in candidates],
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
                "user_input_length": len(user_input),
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
                    "intent": route_result.decision.intent,
                    "selected_tool_names": (route_result.decision.selected_tool_names),
                    "missing_input_names": route_result.decision.missing_inputs,
                    "mode": route_result.mode,
                    "has_error": route_result.error is not None,
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
                "user_input_length": len(user_input),
                "router_intent": route_result.decision.intent,
                "selected_tool_names": (route_result.decision.selected_tool_names),
                "route_payload_keys": list(route_payload),
                "tool_result_count": len(route_payload.get("tool_call_results", [])),
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
            trace.end({"answer_length": len(answer)})
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
                "path_parameter_names": list(payload.path_params),
                "query_parameter_names": list(payload.query),
                "header_names": list(payload.headers),
                "has_body": payload.body is not None,
                "confirmed": payload.confirm,
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
            try:
                self.memory.append(
                    "paypal_tool",
                    _tool_result_metadata(result),
                )
            except OSError:
                pass
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
            inputs={"query_length": len(query), "limit": limit},
            tags=["system-search"],
        ) as trace:
            tools = [
                tool.to_dict() for tool in self.registry.search(query, limit=limit)
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
            inputs={"query_length": len(user_input)},
            tags=["rag"],
        ) as trace:
            result = self.rag.search(user_input)
            if not result["matches"]:
                trace.end({"match_count": 0})
                return "No matching local documentation was found.", result
            answer = "\n".join(
                f"{match['source']}: {match['snippet']}" for match in result["matches"]
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
            inputs={"query_length": len(user_input)},
            tags=["system-search"],
        ) as trace:
            result = self.system_search.search(user_input)
            trace.end(
                {
                    "matching_tool_count": len(result["matching_tools"]),
                    "matching_request_count": len(result["matching_requests"]),
                }
            )
            return (
                "Matching tools: "
                + ", ".join(tool["tool_name"] for tool in result["matching_tools"][:5])
            ), result

    def _memory_grep_answer(self, user_input: str) -> tuple[str, dict[str, Any]]:
        with traceRun(
            self.settings,
            "memory_grep_tool",
            "tool",
            inputs={"query_length": len(user_input)},
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
            inputs={"query_length": len(user_input)},
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
        decision: RouterDecision,
    ) -> tuple[str, dict[str, Any]]:
        selectedToolNames: list[str] = decision.selected_tool_names
        routedInput: RoutedToolInput | None = decision.tool_input
        if len(selectedToolNames) != 1 or routedInput is None:
            return (
                "I need one exact PayPal tool and its complete request values.",
                {"selected_tools": [], "tool_call_results": []},
            )

        tool: ApiTool = self.registry.get(selectedToolNames[0])
        payload: ToolCallInput = ToolCallInput(
            pathParams=routedInput.path_params,
            query=routedInput.query,
            body=routedInput.body,
            headers=routedInput.headers,
        )
        if tool.is_mutating:
            if tool.method == "POST" and not any(
                name.lower() == "paypal-request-id" for name in payload.headers
            ):
                payload = payload.model_copy(
                    update={
                        "headers": {
                            **payload.headers,
                            "PayPal-Request-Id": str(uuid.uuid4()),
                        }
                    }
                )
            directPayload: dict[str, Any] = payload.model_dump(
                by_alias=True,
                exclude_defaults=True,
                exclude_none=True,
            )
            return _format_mutation_plan(tool, directPayload), {
                "selected_tools": [tool.to_dict()],
                "tool_input": routedInput.model_dump(
                    by_alias=True,
                    exclude_none=True,
                ),
                "required_direct_call": {
                    "method": "POST",
                    "path": f"/tools/{tool.tool_name}/call",
                    "payload": directPayload,
                    "requires": [
                        "explicit user review",
                        "separate direct caller sets confirm=true",
                        "reuse PayPal-Request-Id for every retry",
                        "PAYPAL_ALLOW_MUTATIONS=true",
                    ],
                },
                "tool_call_results": [],
            }

        result: dict[str, Any]
        try:
            result = await self.paypal_client.execute(tool, payload)
        except ClientInputError as error:
            result = {
                "status": "rejected",
                "status_code": None,
                "request_sent": False,
                "tool": tool.to_dict(),
                "error": str(error),
            }
        except httpx.TimeoutException:
            result = {
                "status": "client_error",
                "status_code": None,
                "tool": tool.to_dict(),
                "error": "PayPal request timed out.",
            }
        except httpx.RequestError:
            result = {
                "status": "client_error",
                "status_code": None,
                "tool": tool.to_dict(),
                "error": "PayPal request failed before a response was received.",
            }
        toolResults: list[dict[str, Any]] = [result]
        return _format_paypal_tool_results([tool], toolResults), {
            "selected_tools": [tool.to_dict()],
            "tool_input": routedInput.model_dump(
                by_alias=True,
                exclude_none=True,
            ),
            "tool_call_results": toolResults,
        }


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


def _format_paypal_tool_results(
    selectedTools: list[ApiTool],
    toolResults: list[dict[str, Any]],
) -> str:
    if not selectedTools:
        return "No PayPal tool matched the request."
    if not toolResults:
        return "Selected PayPal tools:\n" + _paypal_tool_lines(selectedTools)

    if all(result.get("request_sent") is False for result in toolResults):
        lines: list[str] = ["PayPal request rejected before execution:"]
    elif all(
        result.get("status") == "client_error" and result.get("status_code") is None
        for result in toolResults
    ):
        lines = ["PayPal tool call failed before receiving a response:"]
    else:
        lines = ["Executed PayPal tool call:"]
    for result in toolResults:
        tool = result.get("tool", {})
        toolName = tool.get("tool_name", "unknown_tool")
        method = tool.get("method", "UNKNOWN")
        path = tool.get("path", "")
        statusCode = result.get("status_code")
        status = result.get("status")
        lines.append(
            f"- {toolName}: {method} {path}; status={status}; status_code={statusCode}"
        )
        paypalDebugId = _paypal_debug_id(result)
        if paypalDebugId:
            lines.append(f"  paypal_debug_id={paypalDebugId}")
        if result.get("error"):
            lines.append(f"  error={result['error']}")
        if result.get("message"):
            lines.append(
                "  message=" + str(_bounded_paypal_value(result.get("message")))
            )
        if "response" in result:
            lines.append(
                "  response="
                + json.dumps(
                    _bounded_paypal_value(result.get("response")),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
    return "\n".join(lines)


def _format_mutation_plan(
    tool: ApiTool,
    directPayload: dict[str, Any],
) -> str:
    return (
        "This mutating PayPal request was not executed. Review the exact "
        "payload below. A separate direct caller must explicitly confirm it "
        "and enable PAYPAL_ALLOW_MUTATIONS=true before posting it to "
        f"/tools/{tool.tool_name}/call:\n"
        + json.dumps(
            directPayload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def _bounded_paypal_value(
    value: Any,
    *,
    depth: int = 0,
) -> Any:
    if depth >= 6:
        return "...[nested response truncated]"
    if isinstance(value, dict):
        items = list(value.items())
        bounded = {
            str(key): _bounded_paypal_value(child, depth=depth + 1)
            for key, child in items[:40]
        }
        if len(items) > 40:
            bounded["__truncated__"] = f"{len(items) - 40} fields omitted"
        return bounded
    if isinstance(value, list):
        boundedList = [
            _bounded_paypal_value(child, depth=depth + 1) for child in value[:10]
        ]
        if len(value) > 10:
            boundedList.append(f"...{len(value) - 10} items omitted")
        return boundedList
    if isinstance(value, str) and len(value) > 1000:
        return value[:1000] + "...[truncated]"
    return value


def _mutationBodyIsMissing(tool: ApiTool, body: Any) -> bool:
    template: Any = tool.body_template
    if template is None:
        return False
    if isinstance(template, dict):
        return not isinstance(body, dict) or not body
    if isinstance(template, list):
        return not isinstance(body, list) or not body
    if isinstance(template, str):
        return not isinstance(body, str) or not body.strip()
    return body is None


def _tool_result_metadata(result: dict[str, Any]) -> dict[str, Any]:
    tool = result.get("tool")
    toolName = tool.get("tool_name") if isinstance(tool, dict) else None
    return {
        "tool_name": toolName,
        "status": result.get("status"),
        "status_code": result.get("status_code"),
        "paypal_debug_id": _paypal_debug_id(result),
    }


def _paypal_debug_id(result: dict[str, Any]) -> str | None:
    paypalDebugId = result.get("paypal_debug_id")
    if isinstance(paypalDebugId, str):
        return paypalDebugId
    debugId = result.get("debug_id")
    if isinstance(debugId, str):
        return debugId
    response = result.get("response")
    if isinstance(response, dict):
        responseDebugId = response.get("debug_id")
        if isinstance(responseDebugId, str):
            return responseDebugId
    return None


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
