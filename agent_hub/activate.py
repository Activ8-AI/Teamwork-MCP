from custody.custodian_ledger import log_event
from telemetry.emit_heartbeat import generate_heartbeat


def activate():
    """Trigger a lightweight activation heartbeat and persist it to the ledger."""
    heartbeat = generate_heartbeat()
    log_event("AGENT_ACTIVATION", heartbeat)
    return heartbeat
