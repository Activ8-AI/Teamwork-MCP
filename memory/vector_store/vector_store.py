import os, json

VECTOR_DB = "memory/vector_store/vector_index.json"

def load_vectors():
    if not os.path.exists(VECTOR_DB):
        return {}
    with open(VECTOR_DB, "r") as f:
        return json.load(f)

def save_vectors(data):
    os.makedirs("memory/vector_store", exist_ok=True)
    with open(VECTOR_DB, "w") as f:
        json.dump(data, f, indent=2)
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional


class VectorStore:
    """Placeholder vector store that keeps embeddings in-memory."""

    def __init__(self) -> None:
        self._vectors: Dict[str, List[float]] = {}

    def upsert(self, key: str, vector: List[float]) -> None:
        self._vectors[key] = vector

    def get(self, key: str) -> Optional[List[float]]:
        return self._vectors.get(key)

    def dump(self, path: Path) -> None:
        path.write_text(str(self._vectors), encoding="utf-8")


__all__ = ["VectorStore"]
