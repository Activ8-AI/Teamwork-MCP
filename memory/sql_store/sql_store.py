from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_DB_PATH = Path(__file__).resolve().parent / "events.db"


class SQLStore:
    """Very small SQLite wrapper used by the custodian ledger."""

    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def log_event(self, event_type: str, payload: Dict[str, Any]) -> int:
        """Persist an event and return its row id."""
        serialized = json.dumps(payload)
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO ledger (event_type, payload) VALUES (?, ?)",
                (event_type, serialized),
            )
            conn.commit()
            return cursor.lastrowid

    def fetch_events(
        self, event_type: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        query = "SELECT id, event_type, payload, created_at FROM ledger"
        params: Iterable[Any] = ()
        if event_type:
            query += " WHERE event_type = ?"
            params = (event_type,)

        query += " ORDER BY id DESC LIMIT ?"
        params = (*params, limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        events: List[Dict[str, Any]] = []
        for row in rows:
            events.append(
                {
                    "id": row["id"],
                    "event_type": row["event_type"],
                    "payload": json.loads(row["payload"]),
                    "created_at": row["created_at"],
                }
            )
        return events


__all__ = ["SQLStore", "DEFAULT_DB_PATH"]
