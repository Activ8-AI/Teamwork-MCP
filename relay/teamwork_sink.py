from custody.custodian_ledger import log_event


def create_teamwork_task(title: str, description: str) -> None:
    log_event("TEAMWORK_TASK", {"title": title, "description": description})
