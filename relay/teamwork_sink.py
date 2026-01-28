from custody.custodian_ledger import log_event

def record_evidence(event):
    log_event("TEAMWORK_EVIDENCE", event)
    return {"logged": True}
from __future__ import annotations

from typing import Dict

from custody.custodian_ledger import log_event


def forward_to_teamwork(payload: Dict[str, str]) -> Dict[str, str]:
    """Pretend to forward data to the Teamwork sink and record an audit event."""
    log_event("TEAMWORK_SINK", payload)
    return {"status": "accepted", "destination": "teamwork", **payload}


__all__ = ["forward_to_teamwork"]
