from custody.custodian_ledger import log_event


def send_to_notion(message: str) -> None:
    """Record that a message would be sent to Notion."""
    log_event("NOTION_RELAY", {"message": message})
