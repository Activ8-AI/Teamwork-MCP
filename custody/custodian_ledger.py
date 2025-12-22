import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent / "ledger.db"


def _ensure_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            event_type TEXT,
            payload TEXT
        )
        """
    )


def log_event(event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
    """Persist an event into the local ledger."""
    payload = payload or {}
    serialized_payload = json.dumps(payload)

    with sqlite3.connect(DB_PATH) as conn:
        _ensure_table(conn)
        conn.execute(
            "INSERT INTO ledger (timestamp, event_type, payload) VALUES (?, ?, ?)",
            (datetime.utcnow().isoformat(), event_type, serialized_payload),
        )
        conn.commit()


def get_last_events(n: int = 10) -> List[Dict[str, Any]]:
    """Fetch the most recent N events ordered from newest to oldest."""
    with sqlite3.connect(DB_PATH) as conn:
        _ensure_table(conn)
        rows = conn.execute(
            "SELECT timestamp, event_type, payload FROM ledger ORDER BY id DESC LIMIT ?",
            (n,),
        ).fetchall()

    events: List[Dict[str, Any]] = []
    for timestamp, event_type, payload_json in rows:
        try:
            payload = json.loads(payload_json)
        except json.JSONDecodeError:
            payload = {"raw": payload_json}

        events.append({"timestamp": timestamp, "event": event_type, "payload": payload})

    return events


def clear_ledger() -> None:
    """Clear all events from the ledger. Intended for test isolation."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM ledger")
        conn.commit()
