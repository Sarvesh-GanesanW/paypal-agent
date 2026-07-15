from __future__ import annotations

from pathlib import Path
from typing import Any

from paypal_agent.postman import (
    POSTMAN_COLLECTION_URL,
    ApiTool,
    load_postman_tools,
)
from paypal_agent.tool_search import ToolCatalogSearch


class ToolRegistry:
    def __init__(self, collection_path: Path) -> None:
        self.collection_path: Path = collection_path
        self.tools: list[ApiTool] = load_postman_tools(collection_path)
        self.by_name: dict[str, ApiTool] = {
            tool.tool_name: tool for tool in self.tools
        }
        self.catalogSearch: ToolCatalogSearch = ToolCatalogSearch(self.tools)

    def get(self, tool_name: str) -> ApiTool:
        try:
            return self.by_name[tool_name]
        except KeyError as exc:
            raise KeyError(f"Unknown tool: {tool_name}") from exc

    def search(self, query: str, *, limit: int = 12) -> list[ApiTool]:
        return self.catalogSearch.search(query, limit=limit)

    def catalog(self) -> dict[str, Any]:
        folders: dict[str, list[dict[str, Any]]] = {}
        for tool in self.tools:
            folders.setdefault(tool.folder_path or "Root", []).append(tool.to_dict())
        return {
            "source": POSTMAN_COLLECTION_URL,
            "collection_path": str(self.collection_path),
            "tool_count": len(self.tools),
            "folder_count": len(folders),
            "folders": folders,
        }
