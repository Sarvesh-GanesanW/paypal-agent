from __future__ import annotations

from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from paypal_agent.agent_service import AgentService
from paypal_agent.paypal_client import ClientInputError, ToolCallInput
from paypal_agent.tracing import flushLangSmith

app = FastAPI(title="Datazoic PayPal Agent", version="0.1.0")
service = AgentService()


class ChatRequest(BaseModel):
    user_input: str = Field(alias="userInput", min_length=1)
    conversation_id: str = Field(default="default", alias="conversationId")

    model_config = {"populate_by_name": True}


@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "name": "Datazoic PayPal Agent",
        "status": "healthy",
        "paypal_tool_count": len(service.registry.tools),
        "router": "small_model_strict_schema",
        "orchestrator": "langgraph_state_graph",
        "model_provider": service.settings.model_provider,
        "router_model": service.settings.router_model_id,
        "main_model": service.settings.main_model_id,
        "paypal_environment": service.settings.paypal_environment,
        "paypal_mutations_enabled": service.settings.paypal_allow_mutations,
        "langsmith_tracing": service.settings.langsmith_tracing
        and service.settings.langsmith_api_key is not None,
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/chat")
async def chat(request: ChatRequest) -> dict[str, Any]:
    return await service.chat(request.user_input, request.conversation_id)


@app.get("/tools")
async def tools() -> dict[str, Any]:
    return service.catalog()


@app.get("/tools/search")
async def search_tools(query: str, limit: int = 12) -> dict[str, Any]:
    return {
        "query": query,
        "tools": service.search_tools(query, limit=limit),
    }


@app.post("/tools/{tool_name}/call")
async def call_tool(tool_name: str, payload: ToolCallInput) -> dict[str, Any]:
    try:
        return await service.call_tool(tool_name, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ClientInputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=504,
            detail="PayPal request timed out.",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="PayPal request failed.",
        ) from exc


@app.get("/rag/search")
async def search_rag(query: str, limit: int = 5) -> dict[str, Any]:
    return service.rag.search(query, limit=limit)


@app.get("/system/search")
async def search_system(query: str, limit: int = 10) -> dict[str, Any]:
    return service.system_search.search(query, limit=limit)


@app.get("/memory/grep")
async def grep_memory(query: str, limit: int = 20) -> dict[str, Any]:
    return {
        "status": "success",
        "mode": "jsonl_grep",
        "query": query,
        "matches": service.memory.grep(query, limit=limit),
    }


@app.get("/memory/find")
async def find_memory(query: str, limit: int = 20) -> dict[str, Any]:
    return {
        "status": "success",
        "mode": "jsonl_find",
        "query": query,
        "matches": service.memory.find(query, limit=limit),
    }


@app.get("/observability")
async def observability() -> dict[str, Any]:
    return {
        "langsmith_tracing": service.settings.langsmith_tracing
        and service.settings.langsmith_api_key is not None,
        "langsmith_project": service.settings.langsmith_project,
        "model_provider": service.settings.model_provider,
        "router_model": service.settings.router_model_id,
        "main_model": service.settings.main_model_id,
        "paypal_environment": service.settings.paypal_environment,
        "paypal_mutations_enabled": service.settings.paypal_allow_mutations,
        "orchestrator": "langgraph_state_graph",
    }


@app.post("/observability/flush")
async def flush_observability() -> dict[str, str]:
    flushLangSmith(service.settings)
    return {"status": "flushed"}
