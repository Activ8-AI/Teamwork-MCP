from __future__ import annotations

import uuid
from typing import Any, Dict

from custody.custodian_ledger import log_event
from telemetry.emit_heartbeat import generate_heartbeat


def activate() -> Dict[str, Any]:
    """Trigger a lightweight activation heartbeat and persist it to the ledger."""
    heartbeat = generate_heartbeat()
    log_event("AGENT_ACTIVATION", heartbeat)
    return heartbeat


def activate_agent(agent_name: str = "default-agent") -> Dict[str, str]:
    """Return a payload describing the activated agent."""
    return {"agent_name": agent_name, "session_id": str(uuid.uuid4())}


__all__ = ["activate", "activate_agent"]
