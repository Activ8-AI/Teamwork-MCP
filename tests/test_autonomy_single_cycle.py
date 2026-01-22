from telemetry.emit_heartbeat import generate_heartbeat
from custody.custodian_ledger import log_event, get_last_events


def test_single_cycle():
    before = len(get_last_events(100))
    hb = generate_heartbeat()
    log_event("AUTONOMY_LOOP", hb)
    after = len(get_last_events(100))
    assert after == before + 1
