from custody.custodian_ledger import get_last_events, log_event
from telemetry.emit_heartbeat import generate_heartbeat


def test_heartbeat_write(isolated_ledger_db):
    """Test that heartbeat events are written to the ledger.
    
    Uses isolated_ledger_db fixture to prevent race conditions
    from parallel test execution or shared ledger state.
    """
    before = len(get_last_events(100))
    hb = generate_heartbeat()
    log_event("HEARTBEAT_EMIT", hb)
    after = len(get_last_events(100))
    assert after == before + 1
