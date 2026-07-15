from __future__ import annotations

from importlib.resources import files
from pathlib import Path

DEFAULT_POSTMAN_RELATIVE_PATH = Path(
    "data/postman/paypal_apis.postman_collection.json"
)


def defaultPostmanCollectionPath() -> Path:
    resource = files("paypal_agent").joinpath(
        "assets",
        "postman",
        "paypal_apis.postman_collection.json",
    )
    return Path(str(resource))


def defaultKnowledgeBasePath() -> Path:
    resource = files("paypal_agent").joinpath("assets", "knowledge_base")
    packagedPath: Path = Path(str(resource))
    projectPath: Path = Path(__file__).resolve().parents[2] / "data/paypal_docs"
    for candidatePath in (projectPath, packagedPath):
        if candidatePath.is_dir() and next(candidatePath.glob("*.md"), None):
            return candidatePath
    return packagedPath


def resolvePostmanCollectionPath(collectionPath: Path) -> Path:
    if collectionPath.exists():
        return collectionPath
    if (
        not collectionPath.is_absolute()
        and collectionPath == DEFAULT_POSTMAN_RELATIVE_PATH
    ):
        return defaultPostmanCollectionPath()
    return collectionPath
