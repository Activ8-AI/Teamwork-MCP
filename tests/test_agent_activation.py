from agent_hub.activate import activate
from custody.custodian_ledger import get_last_events


def test_agent_activation():
    """Test that agent activation logs exactly one event to the ledger."""
    activate()
    events = get_last_events(100)
    assert len(events) == 1
    assert events[0]["event"] == "AGENT_ACTIVATION"
