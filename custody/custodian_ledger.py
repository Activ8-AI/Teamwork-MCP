from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent / "ledger.db"

EVENT_AUTONOMY_LOOP = "AUTONOMY_LOOP"
EVENT_HEARTBEAT = "HEARTBEAT"


def _ensure_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL
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


@dataclass(frozen=True)
class LedgerEntry:
    timestamp: str
    event_type: str
    payload: Dict[str, Any]

    def as_datetime(self) -> datetime:
        return datetime.fromisoformat(self.timestamp)


class CustodianLedger:
    """Thin wrapper that writes events to the local SQLite ledger."""

    def record_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        log_event(event_type, payload)

    def record_heartbeat(self, status: str, meta: Dict[str, Any] | None = None) -> None:
        payload = {"status": status, **(meta or {})}
        self.record_event(EVENT_HEARTBEAT, payload)

    def record_autonomy_loop(self, cycle_id: str, meta: Dict[str, Any] | None = None) -> None:
        payload = {"cycle_id": cycle_id, **(meta or {})}
        self.record_event(EVENT_AUTONOMY_LOOP, payload)

    def recent(self, limit: int = 20) -> List[LedgerEntry]:
        raw = get_last_events(limit)
        return [
            LedgerEntry(timestamp=e["timestamp"], event_type=e["event_type"], payload=e["payload"])
            for e in raw
        ]


__all__ = [
    "CustodianLedger",
    "LedgerEntry",
    "EVENT_AUTONOMY_LOOP",
    "EVENT_HEARTBEAT",
    "get_last_events",
    "log_event",
]
