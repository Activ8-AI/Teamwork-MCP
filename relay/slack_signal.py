from custody.custodian_ledger import log_event


def send_slack_signal(channel: str, message: str) -> None:
    log_event("SLACK_SIGNAL", {"channel": channel, "message": message})
