from agent_hub.activate import activate
from custody.custodian_ledger import get_last_events


def test_agent_activation(isolated_ledger_db):
    """Test that agent activation logs an event to the ledger.
    
    Uses isolated_ledger_db fixture to prevent race conditions
    from parallel test execution or shared ledger state.
    """
    before = len(get_last_events(100))
    activate()
    after = len(get_last_events(100))
    assert after == before + 1
