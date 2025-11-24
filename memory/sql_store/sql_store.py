import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent / "memory.db"


class SqlStore:
    """Very small helper for persisting key/value data in SQLite."""

    def __init__(self):
        self._ensure_table()

    def _ensure_table(self) -> None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS kv_store (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
                """
            )
            conn.commit()

    def set(self, key: str, value: str) -> None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "REPLACE INTO kv_store (key, value) VALUES (?, ?)",
                (key, value),
            )
            conn.commit()

    def get(self, key: str) -> Optional[str]:
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                "SELECT value FROM kv_store WHERE key = ?",
                (key,),
            ).fetchone()
        return row[0] if row else None
