import os
import sqlite3
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
    temp_db_fd, temp_db_path = tempfile.mkstemp(suffix=".db")
    temp_db_path_obj = Path(temp_db_path)
    
    # Patch the DB_PATH in custodian_ledger module
    with patch("custody.custodian_ledger.DB_PATH", temp_db_path_obj):
        yield temp_db_path_obj
    
    # Cleanup: close file descriptor and remove temporary database
    os.close(temp_db_fd)
    if temp_db_path_obj.exists():
        temp_db_path_obj.unlink()
