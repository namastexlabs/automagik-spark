"""Tests for API authentication."""
import os
import pytest
from fastapi.testclient import TestClient
from automagik.api.app import app

@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)

def test_api_no_key_configured(client):
    """Test that endpoints are accessible when no API key is configured."""
    if "AUTOMAGIK_API_KEY" in os.environ:
        del os.environ["AUTOMAGIK_API_KEY"]

    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_api_key_required(client):
    """Test that endpoints require API key when configured."""
    os.environ["AUTOMAGIK_API_KEY"] = "test-key"
    
    # Test without key
    response = client.get("/api/v1/")
    assert response.status_code == 401
    assert "X-API-Key header is missing" in response.json()["detail"]
    
    # Test with wrong key
    response = client.get("/api/v1/", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]
    
    # Test with correct key
    response = client.get("/api/v1/", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_api_key_flows(client):
    """Test API key authentication for flows endpoints."""
    os.environ["AUTOMAGIK_API_KEY"] = "test-key"
    headers = {"X-API-Key": "test-key"}
    
    # Test list flows
    response = client.get("/api/v1/flows", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Test without key
    response = client.get("/api/v1/flows")
    assert response.status_code == 401

def test_api_key_tasks(client):
    """Test API key authentication for tasks endpoints."""
    os.environ["AUTOMAGIK_API_KEY"] = "test-key"
    headers = {"X-API-Key": "test-key"}
    
    # Test list tasks
    response = client.get("/api/v1/tasks", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Test without key
    response = client.get("/api/v1/tasks")
    assert response.status_code == 401

def test_api_key_schedules(client):
    """Test API key authentication for schedules endpoints."""
    os.environ["AUTOMAGIK_API_KEY"] = "test-key"
    headers = {"X-API-Key": "test-key"}
    
    # Test list schedules
    response = client.get("/api/v1/schedules", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Test without key
    response = client.get("/api/v1/schedules")
    assert response.status_code == 401

def test_api_key_workers(client):
    """Test API key authentication for workers endpoints."""
    os.environ["AUTOMAGIK_API_KEY"] = "test-key"
    headers = {"X-API-Key": "test-key"}
    
    # Test list workers
    response = client.get("/api/v1/workers", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Test without key
    response = client.get("/api/v1/workers")
    assert response.status_code == 401

@pytest.fixture(autouse=True)
def cleanup_env():
    """Clean up environment variables after each test."""
    yield
    if "AUTOMAGIK_API_KEY" in os.environ:
        del os.environ["AUTOMAGIK_API_KEY"]
