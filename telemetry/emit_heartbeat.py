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
