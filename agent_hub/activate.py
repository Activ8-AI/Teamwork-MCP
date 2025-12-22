from custody.custodian_ledger import log_event
from telemetry.emit_heartbeat import generate_heartbeat


def activate():
    """Trigger a lightweight activation heartbeat and persist it to the ledger."""
    heartbeat = generate_heartbeat()
    log_event("AGENT_ACTIVATION", heartbeat)
from __future__ import annotations

import uuid
from typing import Dict


def activate_agent(agent_name: str = "default-agent") -> Dict[str, str]:
    """Return a payload describing the activated agent."""
    return {"agent_name": agent_name, "session_id": str(uuid.uuid4())}


__all__ = ["activate_agent"]
