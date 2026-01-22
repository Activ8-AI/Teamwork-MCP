from __future__ import annotations

import socket
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from custody.custodian_ledger import log_event


def generate_heartbeat(additional_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate a standard heartbeat payload."""
    payload: Dict[str, Any] = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "host": socket.gethostname(),
        "status": "ok",
    }

    if additional_payload:
        payload.update(additional_payload)

    return payload


def emit_heartbeat(status: str = "ok", meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate and record a heartbeat payload to the local ledger."""
    payload = generate_heartbeat({"status": status, **(meta or {})})
    log_event("HEARTBEAT", payload)
    return payload


__all__ = ["generate_heartbeat", "emit_heartbeat"]
