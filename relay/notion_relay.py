from __future__ import annotations

from typing import Dict

from custody.custodian_ledger import log_event


def send_to_notion(payload: Dict[str, str]) -> Dict[str, str]:
    """Pretend to send a payload to Notion and record an audit event."""
    log_event("NOTION_RELAY", payload)
    return {"status": "queued", "destination": "notion", **payload}


__all__ = ["send_to_notion"]
