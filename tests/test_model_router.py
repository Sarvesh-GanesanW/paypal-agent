from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from paypal_agent.config import Settings
from paypal_agent.model_router import RouterDecision, SmallModelRouter
from paypal_agent.postman import load_postman_tools


class FakeBedrockClient:
    def __init__(self, selected_tool_name: str) -> None:
        self.selected_tool_name = selected_tool_name
        self.last_request: dict[str, Any] | None = None

    def converse(self, **kwargs: Any) -> dict[str, Any]:
        self.last_request = kwargs
        return {
            "output": {
                "message": {
                    "content": [
                        {
                            "toolUse": {
                                "name": "route_request",
                                "input": {
                                    "intent": "paypal_tool",
                                    "selected_tool_names": [self.selected_tool_name],
                                    "missing_inputs": [],
                                    "user_message": "selected",
                                    "confidence": 0.9,
                                },
                            }
                        }
                    ]
                }
            }
        }


@pytest.mark.asyncio
async def test_small_model_router_uses_bedrock_tool_choice(
    collection_path: Path,
) -> None:
    tools = load_postman_tools(collection_path)[:2]
    fake_client = FakeBedrockClient(tools[0].tool_name)
    router = SmallModelRouter(
        Settings(
            paypal_postman_collection_path=collection_path,
            bedrock_router_enabled=True,
        ),
        bedrock_client=fake_client,
    )

    result = await router.route("create order", tools)

    assert result.mode == "bedrock"
    assert result.decision.selected_tool_names == [tools[0].tool_name]
    assert fake_client.last_request is not None
    assert fake_client.last_request["inferenceConfig"]["temperature"] == 0.0
    assert fake_client.last_request["toolConfig"]["toolChoice"] == {
        "tool": {"name": "route_request"}
    }


def test_router_decision_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        RouterDecision.model_validate(
            {
                "intent": "clarify",
                "selected_tool_names": [],
                "missing_inputs": ["action"],
                "user_message": "clarify",
                "confidence": 0.2,
                "extra": "nope",
            }
        )
