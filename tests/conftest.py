import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def isolated_ledger():
    """
    Provides an isolated ledger database for each test.
    
    This fixture creates a temporary database file that is automatically
    cleaned up after the test completes, ensuring test isolation and
    preventing race conditions when tests run in parallel.
    """
    # Create a temporary file for the test database
    temp_db = tempfile.NamedTemporaryFile(mode='w', suffix=".db", delete=False)
    temp_db_path = Path(temp_db.name)
    temp_db.close()
    
    # Patch the DB_PATH in custodian_ledger module
    with patch("custody.custodian_ledger.DB_PATH", temp_db_path):
        yield temp_db_path
    
    # Cleanup: remove temporary database
    if temp_db_path.exists():
        temp_db_path.unlink()
