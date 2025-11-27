from __future__ import annotations

import uuid
from typing import Dict


def activate_agent(agent_name: str = "default-agent") -> Dict[str, str]:
    """Return a payload describing the activated agent."""
    return {"agent_name": agent_name, "session_id": str(uuid.uuid4())}


__all__ = ["activate_agent"]
