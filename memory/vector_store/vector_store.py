from typing import Dict, List


class InMemoryVectorStore:
    """Naive vector store that tracks embeddings by key in memory."""

    def __init__(self):
        self._vectors: Dict[str, List[float]] = {}

    def upsert(self, key: str, vector: List[float]) -> None:
        self._vectors[key] = vector

    def get(self, key: str) -> List[float]:
        return self._vectors.get(key, [])
