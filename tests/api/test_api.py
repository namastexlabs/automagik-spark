"""Tests for the API endpoints."""
import os
from fastapi.testclient import TestClient
from automagik.api.app import app

def test_root_endpoint(client: TestClient):
    """Test the root endpoint returns correct status."""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

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
    }

    # Test preflight request
    response = client.options("/api/v1/", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == test_origin

    # Test actual request
    response = client.get("/api/v1/", headers={"Origin": test_origin})
    assert response.status_code == 200
