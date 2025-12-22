import pytest
from custody.custodian_ledger import clear_ledger


@pytest.fixture(autouse=True)
def isolate_ledger():
    """Clear the ledger before each test to ensure test isolation."""
    clear_ledger()
    yield
