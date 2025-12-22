from custody.custodian_ledger import log_event


def create_teamwork_task(title: str, description: str) -> None:
    log_event("TEAMWORK_TASK", {"title": title, "description": description})
from __future__ import annotations

from typing import Dict


def forward_to_teamwork(payload: Dict[str, str]) -> Dict[str, str]:
    """Pretend to forward data to the Teamwork sink."""
    return {"status": "accepted", "destination": "teamwork", **payload}


__all__ = ["forward_to_teamwork"]
