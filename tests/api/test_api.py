
"""Tests for the API endpoints."""
import os
import datetime
import pytest
from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from fastapi.testclient import TestClient

import tomllib
from pathlib import Path

def _get_version():
    """Get version from pyproject.toml"""
    try:
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    except Exception:
        return "unknown"

__version__ = _get_version()
from automagik_spark.api.config import get_cors_origins
from automagik_spark.api.dependencies import verify_api_key
from automagik_spark.api.routers import tasks, workflows, schedules
from tests.conftest import TEST_API_KEY

# Mark all tests to use session-scoped event loop
pytestmark = pytest.mark.asyncio(loop_scope="session")

def create_test_client():
    """Create a new test client with fresh CORS configuration."""
    app = FastAPI(
        title="Spark API",
        description="Spark - Automated workflow management with LangFlow integration",
        version=__version__,
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        openapi_url="/api/v1/openapi.json",
    )
    
    # Configure CORS with environment variables
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # API Key security scheme
    api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "timestamp": datetime.datetime.now().isoformat(),
        }
    
    @app.get("/")
    async def root(api_key: str = Security(verify_api_key)):
        """Root endpoint returning API status."""
        return {
            "status": "online",
            "service": "Spark API",
            "version": __version__,
            "api_key": api_key,
        }
    
    # Add routers with /api/v1 prefix
    app.include_router(workflows.router, prefix="/api/v1")
    app.include_router(tasks.router, prefix="/api/v1")
    app.include_router(schedules.router, prefix="/api/v1")
    
    return TestClient(app)

@pytest.fixture
def client():
    """Create a test client for the API."""
    return create_test_client()

@pytest.fixture
def clean_env():
    """Clean up environment variables before and after each test."""
    env_vars = ["AUTOMAGIK_SPARK_API_KEY", "AUTOMAGIK_SPARK_API_CORS"]
    original_values = {}
    for var in env_vars:
        if var in os.environ:
            original_values[var] = os.environ[var]
            del os.environ[var]
    
    yield
    
    for var, value in original_values.items():
        os.environ[var] = value

async def test_root_endpoint(client: TestClient, clean_env):
    """Test the root endpoint returns correct status."""
    os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
    headers = {"X-API-Key": TEST_API_KEY}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "Spark API"
    assert "version" in data
    assert isinstance(data["version"], str)

async def test_docs_endpoint(client: TestClient, clean_env):
    """Test the OpenAPI docs endpoint is accessible."""
    response = client.get("/api/v1/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

async def test_openapi_json_endpoint(client: TestClient, clean_env):
    """Test the OpenAPI JSON endpoint is accessible."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
    assert "components" in schema

async def test_redoc_endpoint(client: TestClient, clean_env):
    """Test the ReDoc endpoint is accessible."""
    response = client.get("/api/v1/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

async def test_cors_configuration_default(client: TestClient, clean_env):
    """Test default CORS configuration."""
    test_origin = "http://localhost:3000"
    headers = {
        "Origin": test_origin,
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "x-api-key",
    }
    
    # Test preflight request
    response = client.options("/", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == test_origin
    assert "GET" in response.headers["access-control-allow-methods"]
    assert "x-api-key" in response.headers["access-control-allow-headers"].lower()
    
    # Test actual request
    headers = {
        "Origin": test_origin,
        "X-API-Key": TEST_API_KEY
    }
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == test_origin

async def test_cors_configuration_custom(client: TestClient, clean_env):
    """Test custom CORS configuration."""
    test_origin = "http://example.com"
    os.environ["AUTOMAGIK_SPARK_API_CORS"] = test_origin
    
    # Create a new client with fresh CORS configuration
    client = create_test_client()
    
    headers = {
        "Origin": test_origin,
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "x-api-key",
    }
    
    # Test preflight request
    response = client.options("/", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == test_origin
    assert "GET" in response.headers["access-control-allow-methods"]
    assert "x-api-key" in response.headers["access-control-allow-headers"].lower()
    
    # Test actual request
    headers = {
        "Origin": test_origin,
        "X-API-Key": TEST_API_KEY
    }
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == test_origin

async def test_cors_configuration_invalid_origin(client: TestClient, clean_env):
    """Test CORS with invalid origin."""
    test_origin = "http://invalid.com"
    
    # Test actual request
    headers = {
        "Origin": test_origin,
        "X-API-Key": TEST_API_KEY
    }
    response = client.get("/", headers=headers)
    assert response.status_code == 200  # Request succeeds but without CORS headers
    assert "access-control-allow-origin" not in response.headers

async def test_health_check(client: TestClient, clean_env):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert isinstance(data["timestamp"], str)


