import socket
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def generate_heartbeat(additional_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate a standard heartbeat payload."""
    payload = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "host": socket.gethostname(),
        "status": "ok",
    }

    if additional_payload:
        payload.update(additional_payload)

    return payload
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from custody.custodian_ledger import CustodianLedger


def emit_heartbeat(status: str = "ok", meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Record and return the most recent heartbeat payload."""
    ledger = CustodianLedger()
    payload: Dict[str, Any] = {
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if meta:
        payload.update(meta)

    ledger.record_heartbeat(status=status, meta=payload)
    return payload


__all__ = ["emit_heartbeat"]
