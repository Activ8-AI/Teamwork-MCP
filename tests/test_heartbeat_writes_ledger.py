from custody.custodian_ledger import get_last_events, log_event
from telemetry.emit_heartbeat import generate_heartbeat


def test_heartbeat_write():
    """Test that logging a heartbeat event writes exactly one event to the ledger."""
    hb = generate_heartbeat()
    log_event("HEARTBEAT_EMIT", hb)
    events = get_last_events(100)
    assert len(events) == 1
    assert events[0]["event"] == "HEARTBEAT_EMIT"
