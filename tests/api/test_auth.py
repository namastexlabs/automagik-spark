"""Tests for API authentication."""
import os
import pytest
from fastapi.testclient import TestClient
from automagik.api.app import app

TEST_API_KEY = "test-key"

@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)

@pytest.mark.asyncio
async def test_api_no_key_configured(client):
    """Test API when no API key is configured."""
    os.environ.pop("AUTOMAGIK_API_KEY", None)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_api_key_required(client):
    """Test API key is required when configured."""
    os.environ["AUTOMAGIK_API_KEY"] = TEST_API_KEY
    response = client.get("/")
    assert response.status_code == 401
    assert "X-API-Key header is missing" in response.json()["detail"]

@pytest.mark.asyncio
async def test_api_key_valid(client):
    """Test API key authentication works."""
    os.environ["AUTOMAGIK_API_KEY"] = TEST_API_KEY
    headers = {"X-API-Key": TEST_API_KEY}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.fixture(autouse=True)
def cleanup_env():
    """Clean up environment variables after each test."""
    yield
    os.environ.pop("AUTOMAGIK_API_KEY", None)
