from custody.custodian_ledger import log_event


def send_slack_signal(channel: str, message: str) -> None:
    log_event("SLACK_SIGNAL", {"channel": channel, "message": message})
from __future__ import annotations

from typing import Dict


def send_slack_signal(channel: str, message: str) -> Dict[str, str]:
    """Pretend to dispatch a Slack signal."""
    return {"status": "sent", "channel": channel, "message": message}


__all__ = ["send_slack_signal"]
