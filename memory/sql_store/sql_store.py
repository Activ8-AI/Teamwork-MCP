import sqlite3
import os

DB_PATH = "custody/custodian_ledger.db"

def connect():
    return sqlite3.connect(DB_PATH)

def write_record(event_type, payload):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ledger(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            payload TEXT
        )
    """)
    conn.commit()

    cursor.execute(
        "INSERT INTO ledger (timestamp, event_type, payload) VALUES (?, ?, ?)",
        (os.popen("date").read().strip(), event_type, str(payload)),
    )
    conn.commit()
    conn.close()
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent / "memory.db"


class SqlStore:
    """Very small helper for persisting key/value data in SQLite."""

    def __init__(self) -> None:
        self._conn = sqlite3.connect(DB_PATH)
        self._ensure_table()

    def close(self) -> None:
        if hasattr(self, "_conn") and self._conn:
            self._conn.close()

    def _ensure_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kv_store (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )
        self._conn.commit()

    def set(self, key: str, value: str) -> None:
        self._conn.execute(
            "REPLACE INTO kv_store (key, value) VALUES (?, ?)",
            (key, value),
        )
        self._conn.commit()

    def get(self, key: str) -> Optional[str]:
        row = self._conn.execute(
            "SELECT value FROM kv_store WHERE key = ?",
            (key,),
        ).fetchone()
        return row[0] if row else None


__all__ = ["SqlStore"]
