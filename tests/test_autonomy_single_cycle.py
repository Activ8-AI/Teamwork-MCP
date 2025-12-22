from telemetry.emit_heartbeat import generate_heartbeat
from custody.custodian_ledger import log_event, get_last_events


def test_single_cycle():
    """Test that logging an autonomy loop event writes exactly one event to the ledger."""
    hb = generate_heartbeat()
    log_event("AUTONOMY_LOOP", hb)
    events = get_last_events(100)
    assert len(events) == 1
    assert events[0]["event"] == "AUTONOMY_LOOP"
