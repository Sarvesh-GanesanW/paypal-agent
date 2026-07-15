from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, cast

from paypal_agent.agent_service import AgentService
from paypal_agent.config import ModelProvider, Settings
from paypal_agent.tracing import flushLangSmith
from paypal_agent.user_config import CONFIG_PATH, setProvider, settingsOverrides

EXIT_COMMANDS = {"/exit", "/quit", "exit", "quit"}
MODEL_PROVIDER_CHOICES: tuple[ModelProvider, ...] = (
    "bedrock",
    "openai",
    "anthropic",
    "codex",
)
HELP_TEXT = """\
Commands:
  /help             show this help
  /provider         show the active model provider
  /provider codex   save and switch provider: bedrock, openai, anthropic, codex
  /login codex      run Codex CLI login for ChatGPT/API-key auth
  /login codex device
                    run Codex device-code login
  /tools <query>    search available PayPal tools
  /rag <query>      search local PayPal documentation
  /grep <pattern>   grep local JSONL memory
  /find <query>     find local JSONL memory by keywords
  /quit             exit

Query commands use the same LangGraph chat and answer-model path as normal text.

Type normal user requests directly, for example:
  I need to send a $50 invoice to buyer@example.com. What do you need from me?
"""


@dataclass
class CliState:
    settings: Settings
    service: AgentService
    conversation_id: str
    no_stream: bool
    no_color: bool


def main() -> int:
    args = _parseArgs()
    if args.login_codex:
        return _loginCodex(
            Settings(**settingsOverrides()),
            device_auth=args.device_auth,
        )
    settings = _buildSettings(args)
    return asyncio.run(_run(args, settings))


def _parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chat with the PayPal agent.")
    parser.add_argument("--conversation-id", default="terminal")
    parser.add_argument("--once", help="send one prompt and exit")
    parser.add_argument("--provider", choices=MODEL_PROVIDER_CHOICES)
    parser.add_argument(
        "--save-provider",
        action="store_true",
        help="persist --provider to the global TUI config",
    )
    parser.add_argument(
        "--login-codex",
        action="store_true",
        help="run `codex login` and exit",
    )
    parser.add_argument(
        "--device-auth",
        action="store_true",
        help="use `codex login --device-auth` with --login-codex",
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="print the final response without streaming graph progress",
    )
    parser.add_argument("--no-color", action="store_true")
    return parser.parse_args()


def _buildSettings(args: argparse.Namespace) -> Settings:
    overrides = settingsOverrides()
    if args.provider:
        overrides["model_provider"] = args.provider
        if args.save_provider:
            setProvider(args.provider)
    return Settings(**overrides)


async def _run(args: argparse.Namespace, settings: Settings) -> int:
    state = CliState(
        settings=settings,
        service=AgentService(settings),
        conversation_id=args.conversation_id,
        no_stream=args.no_stream,
        no_color=args.no_color,
    )
    if args.once:
        await _handleInput(
            state,
            args.once,
        )
        flushLangSmith(settings)
        return 0

    print(_color("Datazoic PayPal Agent", "cyan", args.no_color))
    print(f"Provider: {settings.model_provider}. Type /help for commands.")
    while True:
        try:
            userInput = input("\nuser> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not userInput:
            continue
        if userInput.lower() in EXIT_COMMANDS:
            break
        await _handleInput(
            state,
            userInput,
        )
    flushLangSmith(settings)
    return 0


async def _handleInput(
    state: CliState,
    userInput: str,
) -> None:
    if userInput == "/help":
        print(HELP_TEXT)
        return
    if userInput.startswith("/provider"):
        _handleProviderCommand(state, userInput)
        return
    if userInput.startswith("/login "):
        await _handleLoginCommand(state, userInput)
        return

    if state.no_stream:
        result = await state.service.chat(userInput, state.conversation_id)
        print(formatChatResult(result, no_color=state.no_color))
        return
    await _printStreamedChatResult(state, userInput)


async def _printStreamedChatResult(
    state: CliState,
    userInput: str,
) -> None:
    print(_color("assistant>", "green", state.no_color))
    finalResult: dict[str, Any] | None = None
    async for event in state.service.stream_chat(
        userInput,
        state.conversation_id,
    ):
        if event["event"] == "node":
            node = event.get("node")
            if node:
                print(_color(f"[{node}]", "cyan", state.no_color))
            continue
        result = event.get("result")
        if isinstance(result, dict):
            finalResult = result
    if finalResult is None:
        print("No response was produced.")
        return
    _streamText(finalResult["answer"])
    print()
    print(formatRouteSummary(finalResult, no_color=state.no_color))


def _handleProviderCommand(state: CliState, userInput: str) -> None:
    parts = userInput.split()
    if len(parts) == 1:
        print(
            "provider="
            + state.settings.model_provider
            + f" router_model={state.settings.router_model_id}"
        )
        print(f"config={CONFIG_PATH}")
        return
    provider = parts[1]
    if provider not in MODEL_PROVIDER_CHOICES:
        print("Use one of: " + ", ".join(MODEL_PROVIDER_CHOICES))
        return
    setProvider(cast(ModelProvider, provider))
    overrides = settingsOverrides()
    state.settings = Settings(**overrides)
    state.service = AgentService(state.settings)
    print(f"provider={state.settings.model_provider} saved to {CONFIG_PATH}")


async def _handleLoginCommand(state: CliState, userInput: str) -> None:
    parts = userInput.split()
    if len(parts) < 2 or parts[1] != "codex":
        print("Only `/login codex` is supported.")
        return
    deviceAuth = len(parts) > 2 and parts[2] == "device"
    code = await asyncio.to_thread(
        _loginCodex,
        state.settings,
        device_auth=deviceAuth,
    )
    if code == 0:
        print("codex_login=ok")
    else:
        print(f"codex_login=failed exit_code={code}")


def _loginCodex(settings: Settings, *, device_auth: bool) -> int:
    command = [settings.codex_command, "login"]
    if device_auth:
        command.append("--device-auth")
    try:
        return subprocess.run(command, check=False).returncode
    except FileNotFoundError:
        print(f"Codex command not found: {settings.codex_command}")
        return 127


def formatChatResult(result: dict[str, Any], *, no_color: bool = False) -> str:
    return "\n".join(
        [
            _color("assistant>", "green", no_color),
            result["answer"],
            "",
            formatRouteSummary(result, no_color=no_color),
        ]
    )


def formatRouteSummary(result: dict[str, Any], *, no_color: bool = False) -> str:
    decision = result["router_decision"]
    metadata = result["metadata"]
    lines = [
        _color("route", "cyan", no_color)
        + (
            f": intent={decision['intent']} "
            f"mode={metadata['router_mode']} "
            f"confidence={decision['confidence']}"
        ),
    ]
    selectedTools = result.get("selected_tool_names", [])
    if selectedTools:
        lines.append("selected_tools=" + ", ".join(selectedTools[:8]))
    if metadata.get("answer_model_used"):
        lines.append("router_model=" + str(metadata["router_model"]))
        lines.append("subagent_model=" + str(metadata["subagent_model"]))
        lines.append("answer_model=" + str(metadata["answer_model"]))
    for toolResult in result.get("tool_results", [])[:3]:
        tool = toolResult.get("tool", {})
        toolName = tool.get("tool_name", "unknown_tool")
        lines.append(
            "tool_call="
            + str(toolName)
            + f" status={toolResult.get('status')}"
            + f" status_code={toolResult.get('status_code')}"
        )
        paypalDebugId = toolResult.get("paypal_debug_id")
        if paypalDebugId:
            lines.append("paypal_debug_id=" + str(paypalDebugId))
    if metadata.get("router_error"):
        lines.append("router_error=" + str(metadata["router_error"]))
    return "\n".join(lines)


def _streamText(text: str) -> None:
    for index, chunk in enumerate(text.split(" ")):
        if index:
            print(" ", end="", flush=True)
        print(chunk, end="", flush=True)
    sys.stdout.flush()


def _color(text: str, color: str, no_color: bool) -> str:
    if no_color:
        return text
    codes = {"cyan": "36", "green": "32"}
    return f"\033[{codes[color]}m{text}\033[0m"


if __name__ == "__main__":
    raise SystemExit(main())
