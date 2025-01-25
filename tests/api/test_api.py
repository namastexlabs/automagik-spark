"""Tests for the API endpoints."""
import os
import pytest
from fastapi.testclient import TestClient
from automagik.api.app import app
from tests.conftest import TEST_API_KEY

def test_root_endpoint(client: TestClient):
    """Test the root endpoint returns correct status."""
    headers = {"X-API-Key": TEST_API_KEY}
    response = client.get("/api/v1/", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert response.json()["service"] == "AutoMagik API"
    assert response.json()["version"] == "0.1.0"

def test_docs_endpoint(client: TestClient):
    """Test the OpenAPI docs endpoint is accessible."""
    response = client.get("/api/v1/docs")
    assert response.status_code == 200

def test_redoc_endpoint(client: TestClient):
    """Test the ReDoc endpoint is accessible."""
    response = client.get("/api/v1/redoc")
    assert response.status_code == 200

def test_cors_configuration(client: TestClient):
    """Test CORS configuration is working."""
    # Get CORS origins from environment
    cors_origins = os.getenv("AUTOMAGIK_API_CORS", "http://localhost:3000,http://localhost:8000")
    test_origin = cors_origins.split(",")[0].strip()

    headers = {
        "Origin": test_origin,
        "Access-Control-Request-Method": "GET",
        "X-API-Key": TEST_API_KEY
    }

    # Test preflight request
    response = client.options("/api/v1/", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == test_origin

    # Test actual request
    response = client.get("/api/v1/", headers={"Origin": test_origin, "X-API-Key": TEST_API_KEY})
    assert response.status_code == 200
