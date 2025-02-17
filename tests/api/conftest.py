
"""Test configuration for API tests."""
import pytest
from fastapi.testclient import TestClient
from automagik.api.app import app

@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


