"""Pytest fixtures for test isolation."""
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
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        tmp_db_path = Path(tmp_file.name)
    
    # Monkey-patch the DB_PATH in the custodian_ledger module
    import custody.custodian_ledger
    monkeypatch.setattr(custody.custodian_ledger, "DB_PATH", tmp_db_path)
    
    yield tmp_db_path
    
    # Cleanup: close any open connections and remove the temp file
    try:
        tmp_db_path.unlink()
    except Exception:
        pass  # File might already be deleted
