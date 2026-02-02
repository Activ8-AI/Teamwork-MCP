"""Pytest fixtures for test isolation."""
import os
import sqlite3
import tempfile
from pathlib import Path
from typing import Generator
import pytest


@pytest.fixture
def isolated_ledger_db(monkeypatch) -> Generator[Path, None, None]:
    """Provide an isolated ledger database for each test.
    
    This fixture creates a temporary database file for each test,
    preventing race conditions from shared state between tests.
    """
    # Create a temporary file and close it immediately so SQLite can use it
    fd, tmp_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)  # Close the file descriptor immediately
    tmp_db_path = Path(tmp_path)
    
    # Monkey-patch the DB_PATH in the custodian_ledger module
    import custody.custodian_ledger
    monkeypatch.setattr(custody.custodian_ledger, "DB_PATH", tmp_db_path)
    
    yield tmp_db_path
    
    # Cleanup: remove the temp file
    tmp_db_path.unlink(missing_ok=True)
