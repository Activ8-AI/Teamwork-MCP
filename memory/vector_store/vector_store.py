from typing import Dict, List


class InMemoryVectorStore:
    """Naive vector store that tracks embeddings by key in memory."""

    def __init__(self):
from __future__ import annotations

from pathlib import Path
from typing import Dict, List


class VectorStore:
    """Placeholder vector store that keeps embeddings in-memory."""

    def __init__(self) -> None:
        self._vectors: Dict[str, List[float]] = {}

    def upsert(self, key: str, vector: List[float]) -> None:
        self._vectors[key] = vector

    def get(self, key: str) -> List[float]:
        return self._vectors.get(key, [])
    def get(self, key: str) -> List[float] | None:
        return self._vectors.get(key)

    def dump(self, path: Path) -> None:
        path.write_text(str(self._vectors))


__all__ = ["VectorStore"]
