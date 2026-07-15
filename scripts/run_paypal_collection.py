from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx

from paypal_agent.agent_service import AgentService
from paypal_agent.config import Settings
from paypal_agent.paypal_client import ClientInputError, ToolCallInput
from paypal_agent.postman import ApiTool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run PayPal Postman collection tools against configured PayPal.",
    )
    parser.add_argument("--tool", action="append", default=[])
    parser.add_argument("--include-mutations", action="store_true")
    parser.add_argument("--confirm-mutations", action="store_true")
    parser.add_argument("--fixtures", type=Path)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    if args.confirm_mutations and not args.include_mutations:
        raise SystemExit("--confirm-mutations requires --include-mutations")

    service = AgentService(Settings())
    fixtures = _load_fixtures(args.fixtures)
    tools = _selected_tools(service.registry.tools, args.tool)
    results: list[dict[str, Any]] = []

    for tool in tools:
        result = await _run_tool(
            service,
            tool,
            fixtures.get(tool.tool_name, {}),
            include_mutations=args.include_mutations,
            confirm_mutations=args.confirm_mutations,
        )
        results.append(result)

    output = {"summary": _summary(results), "results": results}
    output_path = args.out or _default_output_path()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({"summary": output["summary"], "output": str(output_path)}))
    return 0


async def _run_tool(
    service: AgentService,
    tool: ApiTool,
    fixture: dict[str, Any],
    *,
    include_mutations: bool,
    confirm_mutations: bool,
) -> dict[str, Any]:
    if tool.is_mutating and not include_mutations:
        return _skipped(tool, "mutation skipped")
    path_params = fixture.get("pathParams") or fixture.get("path_params")
    if tool.path_variables and not path_params:
        return _skipped(tool, "path fixture required")
    if tool.is_mutating and not fixture:
        return _skipped(tool, "mutation fixture required")

    payload = ToolCallInput.model_validate(
        {
            **fixture,
            "confirm": bool(confirm_mutations and tool.is_mutating),
        }
    )
    try:
        result = await service.call_tool(tool.tool_name, payload)
    except (ClientInputError, KeyError) as exc:
        return {**_tool_fields(tool), "status": "client_error", "error": str(exc)}
    except httpx.TimeoutException:
        return {
            **_tool_fields(tool),
            "status": "client_error",
            "error": "PayPal request timed out.",
        }
    except httpx.RequestError:
        return {
            **_tool_fields(tool),
            "status": "client_error",
            "error": "PayPal request failed.",
        }
    return {
        **_tool_fields(tool),
        "status": result["status"],
        "status_code": result.get("status_code"),
    }


def _selected_tools(tools: list[ApiTool], tool_names: list[str]) -> list[ApiTool]:
    if not tool_names:
        return tools
    wanted = set(tool_names)
    selected = [tool for tool in tools if tool.tool_name in wanted]
    missing = sorted(wanted - {tool.tool_name for tool in selected})
    if missing:
        raise SystemExit("Unknown tools: " + ", ".join(missing))
    return selected


def _load_fixtures(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    with path.open(encoding="utf-8") as file:
        payload: Any = json.load(file)
    if not isinstance(payload, dict):
        raise SystemExit("Fixture file must contain a JSON object.")
    tools = payload.get("tools", payload)
    if not isinstance(tools, dict):
        raise SystemExit("Fixture tools must be a JSON object.")
    return tools


def _summary(results: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(results),
        "sent": sum(1 for result in results if result["status"] != "skipped"),
        "skipped": sum(1 for result in results if result["status"] == "skipped"),
        "success": sum(1 for result in results if result["status"] == "success"),
        "paypal_errors": sum(1 for result in results if result["status"] == "error"),
        "client_errors": sum(
            1 for result in results if result["status"] == "client_error"
        ),
        "requires_confirmation": sum(
            1 for result in results if result["status"] == "requires_confirmation"
        ),
    }


def _skipped(tool: ApiTool, reason: str) -> dict[str, Any]:
    return {**_tool_fields(tool), "status": "skipped", "reason": reason}


def _tool_fields(tool: ApiTool) -> dict[str, Any]:
    return {
        "tool_name": tool.tool_name,
        "method": tool.method,
        "path": tool.path,
        "is_mutating": tool.is_mutating,
    }


def _default_output_path() -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    return Path("logs") / f"paypal_collection_run_{timestamp}.json"


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
