"""Tests for the AutoMagik API."""
import os
from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    """Test the root endpoint returns correct status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "AutoMagik API"
    assert "version" in data

def test_docs_endpoint(client: TestClient):
    """Test the OpenAPI docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_redoc_endpoint(client: TestClient):
    """Test the ReDoc endpoint is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

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
    response = client.options("/", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == test_origin
    
    # Test actual request
    response = client.get("/", headers={"Origin": test_origin})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == test_origin
