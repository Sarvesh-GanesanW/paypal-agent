from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
POSTMAN_COLLECTION_URL = (
    "https://www.postman.com/collections/"
    "19024122-92a85d0e-51e7-47da-9f83-c45dcb1cdf24"
)
VARIABLE_PATTERN = re.compile(r"{{([^{}]+)}}")
PATH_VARIABLE_PATTERN = re.compile(r"/:([A-Za-z_][A-Za-z0-9_]*)")


@dataclass(frozen=True)
class ApiTool:
    tool_name: str
    display_name: str
    folder_path: str
    method: str
    raw_url: str
    path: str
    description: str
    headers: dict[str, str] = field(default_factory=dict)
    query_params: dict[str, str] = field(default_factory=dict)
    path_variables: tuple[str, ...] = ()
    body_template: Any = None

    @property
    def is_mutating(self) -> bool:
        return self.method in MUTATING_METHODS

    @property
    def search_text(self) -> str:
        parts = [
            self.tool_name,
            self.display_name,
            self.folder_path,
            self.method,
            self.path,
            self.description,
        ]
        return " ".join(part for part in parts if part).lower()

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_name": self.tool_name,
            "display_name": self.display_name,
            "folder_path": self.folder_path,
            "method": self.method,
            "path": self.path,
            "description": self.description,
            "headers": self.headers,
            "query_params": self.query_params,
            "path_variables": list(self.path_variables),
            "has_body_template": self.body_template is not None,
            "is_mutating": self.is_mutating,
        }


def load_postman_tools(collection_path: Path) -> list[ApiTool]:
    with collection_path.open(encoding="utf-8") as file:
        collection: dict[str, Any] = json.load(file)

    tools: list[ApiTool] = []
    seen_names: dict[str, int] = {}
    _walk_items(collection.get("item") or [], "", tools, seen_names)
    return tools


def _walk_items(
    items: list[dict[str, Any]],
    folder_path: str,
    tools: list[ApiTool],
    seen_names: dict[str, int],
) -> None:
    for item in items:
        item_name = str(item.get("name") or "").strip()
        request = item.get("request")
        if isinstance(request, dict):
            tools.append(_parse_request(item_name, folder_path, request, seen_names))
            continue

        nested_path = "/".join(part for part in (folder_path, item_name) if part)
        child_items = item.get("item") or []
        if isinstance(child_items, list):
            _walk_items(child_items, nested_path, tools, seen_names)


def _parse_request(
    item_name: str,
    folder_path: str,
    request: dict[str, Any],
    seen_names: dict[str, int],
) -> ApiTool:
    raw_url = _raw_url(request.get("url"))
    path = _path_from_url(raw_url)
    base_name = _slug(f"paypal {folder_path} {item_name}")
    tool_name = _unique_name(base_name, seen_names)
    return ApiTool(
        tool_name=tool_name,
        display_name=item_name,
        folder_path=folder_path,
        method=str(request.get("method") or "GET").upper(),
        raw_url=raw_url,
        path=path,
        description=_description(request.get("description")),
        headers=_headers(request.get("header") or []),
        query_params=_query_params(request.get("url")),
        path_variables=_path_variables(raw_url, path),
        body_template=_body_template(request.get("body")),
    )


def _raw_url(url: Any) -> str:
    if isinstance(url, str):
        return url
    if not isinstance(url, dict):
        return ""
    raw = url.get("raw")
    if isinstance(raw, str):
        return raw
    protocol = url.get("protocol") or "https"
    host = ".".join(url.get("host") or [])
    path = "/".join(url.get("path") or [])
    return f"{protocol}://{host}/{path}".rstrip("/")


def _path_from_url(raw_url: str) -> str:
    normalized = VARIABLE_PATTERN.sub(lambda match: f"{{{match.group(1)}}}", raw_url)
    normalized = normalized.replace("{base_url}", "")
    split_url = urlsplit(normalized)
    path = split_url.path if split_url.scheme else normalized.split("?", 1)[0]
    path = PATH_VARIABLE_PATTERN.sub(r"/{\1}", path)
    if not path.startswith("/"):
        path = "/" + path
    return path or "/"


def _description(description: Any) -> str:
    if isinstance(description, str):
        return " ".join(description.split())
    if isinstance(description, dict):
        content = description.get("content")
        if isinstance(content, str):
            return " ".join(content.split())
    return ""


def _headers(headers: list[dict[str, Any]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for header in headers:
        if header.get("disabled"):
            continue
        key = header.get("key")
        value = header.get("value")
        if isinstance(key, str) and isinstance(value, str):
            result[key] = value
    return result


def _query_params(url: Any) -> dict[str, str]:
    if not isinstance(url, dict):
        return {}
    result: dict[str, str] = {}
    for query_param in url.get("query") or []:
        if query_param.get("disabled"):
            continue
        key = query_param.get("key")
        value = query_param.get("value", "")
        if isinstance(key, str):
            result[key] = str(value)
    return result


def _path_variables(_raw_url: str, path: str) -> tuple[str, ...]:
    variables = {
        variable
        for variable in re.findall(r"{([^{}]+)}", path)
        if variable != "base_url"
    }
    return tuple(sorted(variables))


def _body_template(body: Any) -> Any:
    if not isinstance(body, dict):
        return None
    mode = body.get("mode")
    if mode == "raw":
        raw_body = body.get("raw")
        if not isinstance(raw_body, str) or not raw_body.strip():
            return None
        try:
            return json.loads(raw_body)
        except json.JSONDecodeError:
            return raw_body
    if mode == "urlencoded":
        encoded: dict[str, str] = {}
        for item in body.get("urlencoded") or []:
            if item.get("disabled"):
                continue
            key = item.get("key")
            value = item.get("value", "")
            if isinstance(key, str):
                encoded[key] = str(value)
        return encoded or None
    return None


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return slug or "paypal_tool"


def _unique_name(base_name: str, seen_names: dict[str, int]) -> str:
    count = seen_names.get(base_name, 0)
    seen_names[base_name] = count + 1
    if count == 0:
        return base_name
    return f"{base_name}_{count + 1}"
