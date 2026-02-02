from __future__ import annotations

from typing import Dict

from custody.custodian_ledger import log_event


def send_slack_signal(channel: str, message: str) -> Dict[str, str]:
    """Pretend to dispatch a Slack signal and record an audit event."""
    payload = {"channel": channel, "message": message}
    log_event("SLACK_SIGNAL", payload)
    return {"status": "sent", **payload}


__all__ = ["send_slack_signal"]
