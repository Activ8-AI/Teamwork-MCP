from custody.custodian_ledger import log_event


def send_to_notion(message: str) -> None:
    """Record that a message would be sent to Notion."""
    log_event("NOTION_RELAY", {"message": message})
from __future__ import annotations

from typing import Dict


def send_to_notion(payload: Dict[str, str]) -> Dict[str, str]:
    """Pretend to send a payload to Notion."""
    return {"status": "queued", "destination": "notion", **payload}


__all__ = ["send_to_notion"]
