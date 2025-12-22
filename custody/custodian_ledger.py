import json
import sqlite3
from datetime import datetime, timezone
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
            (datetime.now(timezone.utc).isoformat(), event_type, serialized_payload),
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
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from memory.sql_store.sql_store import SQLStore


EVENT_AUTONOMY_LOOP = "AUTONOMY_LOOP"
EVENT_HEARTBEAT = "HEARTBEAT"


@dataclass
class LedgerEntry:
    id: int
    event_type: str
    payload: Dict[str, Any]
    created_at: str

    def as_datetime(self) -> datetime:
        return datetime.fromisoformat(self.created_at)


class CustodianLedger:
    """Thin layer over the SQL store that understands the event types we emit."""

    def __init__(self, store: Optional[SQLStore] = None) -> None:
        self.store = store or SQLStore()

    def record_event(self, event_type: str, payload: Dict[str, Any]) -> int:
        return self.store.log_event(event_type, payload)

    def record_heartbeat(self, status: str, meta: Dict[str, Any] | None = None) -> int:
        payload = {"status": status, **(meta or {})}
        return self.record_event(EVENT_HEARTBEAT, payload)

    def record_autonomy_loop(self, cycle_id: str, meta: Dict[str, Any] | None = None) -> int:
        payload = {"cycle_id": cycle_id, **(meta or {})}
        return self.record_event(EVENT_AUTONOMY_LOOP, payload)

    def recent(self, event_type: Optional[str] = None, limit: int = 20) -> List[LedgerEntry]:
        raw_entries = self.store.fetch_events(event_type=event_type, limit=limit)
        return [
            LedgerEntry(
                id=entry["id"],
                event_type=entry["event_type"],
                payload=entry["payload"],
                created_at=entry["created_at"],
            )
            for entry in raw_entries
        ]


__all__ = [
    "CustodianLedger",
    "LedgerEntry",
    "EVENT_AUTONOMY_LOOP",
    "EVENT_HEARTBEAT",
]
