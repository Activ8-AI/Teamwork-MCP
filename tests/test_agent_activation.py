from agent_hub.activate import activate
from custody.custodian_ledger import get_last_events


def test_agent_activation(isolated_ledger):
    """Test that agent activation logs exactly one event to the ledger."""
    before = len(get_last_events(100))
    activate()
    after = len(get_last_events(100))
    assert after == before + 1
