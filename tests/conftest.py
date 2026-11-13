import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

TEST_DB = Path(tempfile.gettempdir()) / "deepguard_test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"


@pytest.fixture
def client():
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
