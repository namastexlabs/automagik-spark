"""Tests for sources API endpoints."""
import os
import uuid
import pytest
import httpx
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from automagik_spark.api.app import app
from automagik_spark.api.dependencies import verify_api_key
from automagik_spark.core.database.models import WorkflowSource
from automagik_spark.core.schemas.source import SourceType, SourceStatus
from tests.conftest import TEST_API_KEY

# Mark all tests to use session-scoped event loop
pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
def client():
    """Create a test client with sources router included."""
    return TestClient(app)


@pytest.fixture
def clean_env():
    """Clean up environment variables before and after each test."""
    env_vars = ["AUTOMAGIK_SPARK_API_KEY", "AUTOMAGIK_SPARK_ENCRYPTION_KEY"]
    original_values = {}
    for var in env_vars:
        if var in os.environ:
            original_values[var] = os.environ[var]
            del os.environ[var]
    
    yield
    
    for var, value in original_values.items():
        os.environ[var] = value


@pytest.fixture
def auth_headers():
    """Headers with valid API key."""
    return {"X-API-Key": TEST_API_KEY}


@pytest.fixture
def mock_langflow_response():
    """Mock response for LangFlow health check."""
    return {
        "status": "ok",
        "version": "1.0.0"
    }


@pytest.fixture
def mock_automagik_agents_response():
    """Mock response for AutoMagik Agents health and version."""
    health_response = {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "environment": "production"
    }
    root_response = {
        "name": "AutoMagik Agents",
        "version": "1.2.0",
        "description": "AutoMagik Agents API"
    }
    return health_response, root_response


@pytest.fixture
def mock_automagik_hive_response():
    """Mock response for AutoMagik Hive health and status."""
    health_response = {
        "status": "success",
        "utc": "2024-01-01T00:00:00Z",
        "service": "Automagik Hive Multi-Agent System"
    }
    status_response = {
        "agents_loaded": 5,
        "teams_loaded": 2,
        "workflows_loaded": 10
    }
    return health_response, status_response


@pytest.fixture
def sample_source_data():
    """Sample source data for tests."""
    return {
        "name": "Test LangFlow",
        "source_type": "langflow",
        "url": "http://localhost:7860",
        "api_key": "test-api-key"
    }


@pytest.fixture
async def created_source(client, clean_env, auth_headers, sample_source_data):
    """Create a source for testing update/delete operations."""
    os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
    
    with patch("httpx.AsyncClient.get") as mock_get:
        # Mock health check
        health_mock = AsyncMock()
        health_mock.json.return_value = {"status": "ok"}
        health_mock.raise_for_status = AsyncMock()
        
        # Mock version check  
        version_mock = AsyncMock()
        version_mock.json.return_value = {"version": "1.0.0", "status": "ok"}
        version_mock.raise_for_status = AsyncMock()
        
        mock_get.side_effect = [health_mock, version_mock]
        
        response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
        assert response.status_code == 201
        return response.json()


class TestSourcesCreate:
    """Test cases for POST /sources/."""
    
    async def test_create_langflow_source_success(self, client, clean_env, auth_headers, mock_langflow_response):
        """Test successful creation of LangFlow source."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check
            health_mock = AsyncMock()
            health_mock.json.return_value = mock_langflow_response
            health_mock.raise_for_status = AsyncMock()
            
            # Mock version check
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "1.0.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            source_data = {
                "name": "Test LangFlow",
                "source_type": "langflow", 
                "url": "http://localhost:7860",
                "api_key": "test-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            
            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "Test LangFlow"
            assert data["source_type"] == "langflow"
            assert data["url"] == "http://localhost:7860"
            assert data["status"] == "active"
            assert "id" in data
            assert "created_at" in data
            assert "updated_at" in data
            assert "version_info" in data

    async def test_create_automagik_agents_source_success(self, client, clean_env, auth_headers, mock_automagik_agents_response):
        """Test successful creation of AutoMagik Agents source."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        health_response, root_response = mock_automagik_agents_response
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check
            health_mock = AsyncMock()
            health_mock.json.return_value = health_response
            health_mock.raise_for_status = AsyncMock()
            
            # Mock root endpoint
            root_mock = AsyncMock() 
            root_mock.json.return_value = root_response
            root_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, root_mock]
            
            source_data = {
                "name": "Test AutoMagik Agents",
                "source_type": "automagik-agents",
                "url": "http://localhost:8000",
                "api_key": "agents-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            
            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "Test AutoMagik Agents"
            assert data["source_type"] == "automagik-agents"
            assert data["status"] == "active"

    async def test_create_automagik_hive_source_success(self, client, clean_env, auth_headers, mock_automagik_hive_response):
        """Test successful creation of AutoMagik Hive source."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        health_response, status_response = mock_automagik_hive_response
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check
            health_mock = AsyncMock()
            health_mock.json.return_value = health_response
            health_mock.raise_for_status = AsyncMock()
            
            # Mock status endpoint
            status_mock = AsyncMock()
            status_mock.json.return_value = status_response
            status_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, status_mock]
            
            source_data = {
                "name": "Test AutoMagik Hive", 
                "source_type": "automagik-hive",
                "url": "http://localhost:9000",
                "api_key": "hive-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            
            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "Test AutoMagik Hive"
            assert data["source_type"] == "automagik-hive"
            assert data["status"] == "active"
            assert data["version_info"]["agents_loaded"] == 5

    async def test_create_source_duplicate_url(self, client, created_source, clean_env, auth_headers):
        """Test creating source with duplicate URL fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        source_data = {
            "name": "Duplicate Source",
            "source_type": "langflow",
            "url": created_source["url"], 
            "api_key": "test-key"
        }
        
        response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    async def test_create_source_invalid_url(self, client, clean_env, auth_headers):
        """Test creating source with invalid URL fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        source_data = {
            "name": "Invalid URL Source",
            "source_type": "langflow",
            "url": "not-a-url",
            "api_key": "test-key"
        }
        
        response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error

    async def test_create_source_health_check_fails(self, client, clean_env, auth_headers):
        """Test creating source when health check fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock failed health check
            mock_get.side_effect = httpx.RequestError("Connection failed")
            
            source_data = {
                "name": "Unreachable Source",
                "source_type": "langflow",
                "url": "http://localhost:9999",
                "api_key": "test-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            assert response.status_code == 400
            assert "Failed to validate source" in response.json()["detail"]

    async def test_create_source_unauthorized(self, client, clean_env):
        """Test creating source without API key fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        source_data = {
            "name": "Test Source",
            "source_type": "langflow", 
            "url": "http://localhost:7860",
            "api_key": "test-key"
        }
        
        response = client.post("/api/v1/sources/", json=source_data)
        assert response.status_code == 401

    async def test_create_source_empty_api_key(self, client, clean_env, auth_headers, mock_langflow_response):
        """Test creating source with empty API key succeeds."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check
            health_mock = AsyncMock()
            health_mock.json.return_value = mock_langflow_response
            health_mock.raise_for_status = AsyncMock()
            
            # Mock version check
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "1.0.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            source_data = {
                "name": "No API Key Source",
                "source_type": "langflow",
                "url": "http://localhost:7860",
                "api_key": ""
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            
            assert response.status_code == 201


class TestSourcesList:
    """Test cases for GET /sources/."""
    
    async def test_list_sources_success(self, client, created_source, clean_env, auth_headers):
        """Test successful listing of sources."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.get("/api/v1/sources/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(source["id"] == created_source["id"] for source in data)

    async def test_list_sources_with_status_filter(self, client, created_source, clean_env, auth_headers):
        """Test listing sources with status filter."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.get("/api/v1/sources/?status=active", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for source in data:
            assert source["status"] == "active"

    async def test_list_sources_unauthorized(self, client, clean_env):
        """Test listing sources without API key fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.get("/api/v1/sources/")
        assert response.status_code == 401


class TestSourcesGet:
    """Test cases for GET /sources/{source_id}."""
    
    async def test_get_source_success(self, client, created_source, clean_env, auth_headers):
        """Test successful retrieval of specific source."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.get(f"/api/v1/sources/{created_source['id']}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_source["id"]
        assert data["name"] == created_source["name"]

    async def test_get_source_not_found(self, client, clean_env, auth_headers):
        """Test getting non-existent source returns 404."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/sources/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    async def test_get_source_invalid_id(self, client, clean_env, auth_headers):
        """Test getting source with invalid UUID format."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.get("/api/v1/sources/invalid-uuid", headers=auth_headers)
        assert response.status_code == 422

    async def test_get_source_unauthorized(self, client, created_source, clean_env):
        """Test getting source without API key fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.get(f"/api/v1/sources/{created_source['id']}")
        assert response.status_code == 401


class TestSourcesUpdate:
    """Test cases for PATCH /sources/{source_id}."""
    
    async def test_update_source_name(self, client, created_source, clean_env, auth_headers):
        """Test updating source name."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        update_data = {"name": "Updated Source Name"}
        
        response = client.patch(
            f"/api/v1/sources/{created_source['id']}", 
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Source Name"
        assert data["id"] == created_source["id"]

    async def test_update_source_url(self, client, created_source, clean_env, auth_headers, mock_langflow_response):
        """Test updating source URL."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check for new URL
            health_mock = AsyncMock()
            health_mock.json.return_value = mock_langflow_response
            health_mock.raise_for_status = AsyncMock()
            
            # Mock version check
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "1.0.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            update_data = {"url": "http://localhost:8860"}
            
            response = client.patch(
                f"/api/v1/sources/{created_source['id']}", 
                json=update_data,
                headers=auth_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["url"] == "http://localhost:8860"

    async def test_update_source_api_key(self, client, created_source, clean_env, auth_headers, mock_langflow_response):
        """Test updating source API key validates source."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check with new API key
            health_mock = AsyncMock()
            health_mock.json.return_value = mock_langflow_response
            health_mock.raise_for_status = AsyncMock()
            
            # Mock version check
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "1.1.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            update_data = {"api_key": "new-api-key"}
            
            response = client.patch(
                f"/api/v1/sources/{created_source['id']}", 
                json=update_data,
                headers=auth_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["version_info"]["version"] == "1.1.0"

    async def test_update_source_status(self, client, created_source, clean_env, auth_headers):
        """Test updating source status."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        update_data = {"status": "inactive"}
        
        response = client.patch(
            f"/api/v1/sources/{created_source['id']}", 
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "inactive"

    async def test_update_source_type(self, client, created_source, clean_env, auth_headers):
        """Test updating source type."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        update_data = {"source_type": "automagik-agents"}
        
        response = client.patch(
            f"/api/v1/sources/{created_source['id']}", 
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["source_type"] == "automagik-agents"

    async def test_update_source_url_conflict(self, client, created_source, clean_env, auth_headers, sample_source_data):
        """Test updating URL to existing URL fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        # Create another source first
        with patch("httpx.AsyncClient.get") as mock_get:
            health_mock = AsyncMock()
            health_mock.json.return_value = {"status": "ok"}
            health_mock.raise_for_status = AsyncMock()
            
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "1.0.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            another_source_data = {
                **sample_source_data,
                "url": "http://localhost:9860"
            }
            
            response = client.post("/api/v1/sources/", json=another_source_data, headers=auth_headers)
            assert response.status_code == 201
            another_source = response.json()
            
        # Now try to update first source to second source's URL
        update_data = {"url": another_source["url"]}
        
        response = client.patch(
            f"/api/v1/sources/{created_source['id']}", 
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    async def test_update_source_not_found(self, client, clean_env, auth_headers):
        """Test updating non-existent source returns 404."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        fake_id = str(uuid.uuid4())
        update_data = {"name": "Updated Name"}
        
        response = client.patch(
            f"/api/v1/sources/{fake_id}", 
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_source_unauthorized(self, client, created_source, clean_env):
        """Test updating source without API key fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        update_data = {"name": "Updated Name"}
        
        response = client.patch(
            f"/api/v1/sources/{created_source['id']}", 
            json=update_data
        )
        assert response.status_code == 401

    async def test_update_source_multiple_fields(self, client, created_source, clean_env, auth_headers, mock_langflow_response):
        """Test updating multiple fields at once."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check
            health_mock = AsyncMock()
            health_mock.json.return_value = mock_langflow_response
            health_mock.raise_for_status = AsyncMock()
            
            # Mock version check
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "2.0.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            update_data = {
                "name": "Updated Multi-Field Source",
                "url": "http://localhost:9860", 
                "status": "inactive",
                "api_key": "updated-key"
            }
            
            response = client.patch(
                f"/api/v1/sources/{created_source['id']}", 
                json=update_data,
                headers=auth_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Updated Multi-Field Source"
            assert data["url"] == "http://localhost:9860"
            assert data["status"] == "inactive"
            assert data["version_info"]["version"] == "2.0.0"


class TestSourcesDelete:
    """Test cases for DELETE /sources/{source_id}."""
    
    async def test_delete_source_success(self, client, created_source, clean_env, auth_headers):
        """Test successful deletion of source."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.delete(f"/api/v1/sources/{created_source['id']}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "deleted successfully" in data["message"]
        
        # Verify source is actually deleted
        get_response = client.get(f"/api/v1/sources/{created_source['id']}", headers=auth_headers)
        assert get_response.status_code == 404

    async def test_delete_source_not_found(self, client, clean_env, auth_headers):
        """Test deleting non-existent source returns 404."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/api/v1/sources/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    async def test_delete_source_unauthorized(self, client, created_source, clean_env):
        """Test deleting source without API key fails.""" 
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.delete(f"/api/v1/sources/{created_source['id']}")
        assert response.status_code == 401


class TestSourceValidation:
    """Test cases for source validation logic."""
    
    async def test_wrong_health_status(self, client, clean_env, auth_headers):
        """Test source validation fails when health status is wrong."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check with wrong status for langflow
            health_mock = AsyncMock()
            health_mock.json.return_value = {"status": "error"}
            health_mock.raise_for_status = AsyncMock()
            
            mock_get.return_value = health_mock
            
            source_data = {
                "name": "Wrong Status Source",
                "source_type": "langflow",
                "url": "http://localhost:7860",
                "api_key": "test-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            assert response.status_code == 400
            assert "health check failed" in response.json()["detail"]

    async def test_automagik_hive_fallback_status(self, client, clean_env, auth_headers):
        """Test AutoMagik Hive fallback when status endpoint fails."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check success
            health_mock = AsyncMock()
            health_mock.json.return_value = {
                "status": "success",
                "utc": "2024-01-01T00:00:00Z",
                "service": "Automagik Hive Multi-Agent System"
            }
            health_mock.raise_for_status = AsyncMock()
            
            # Mock status endpoint failure (raises exception)
            status_mock = AsyncMock()
            status_mock.raise_for_status.side_effect = httpx.RequestError("Status endpoint failed")
            
            mock_get.side_effect = [health_mock, status_mock]
            
            source_data = {
                "name": "Fallback Hive Source",
                "source_type": "automagik-hive",
                "url": "http://localhost:9000", 
                "api_key": "hive-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            
            # Should still succeed with fallback data
            assert response.status_code == 201
            data = response.json()
            assert data["version_info"]["name"] == "Automagik Hive Multi-Agent System"


class TestEncryption:
    """Test cases for API key encryption/decryption."""
    
    async def test_api_key_encryption(self, client, clean_env, auth_headers, mock_langflow_response):
        """Test that API keys are properly encrypted in database."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health and version checks
            health_mock = AsyncMock()
            health_mock.json.return_value = mock_langflow_response
            health_mock.raise_for_status = AsyncMock()
            
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "1.0.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            source_data = {
                "name": "Encryption Test Source",
                "source_type": "langflow",
                "url": "http://localhost:7860",
                "api_key": "secret-api-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            assert response.status_code == 201
            
            # Test encryption and decryption work correctly
            test_key = "test-secret-key"
            encrypted = WorkflowSource.encrypt_api_key(test_key)
            assert encrypted != test_key  # Should be encrypted
            
            decrypted = WorkflowSource.decrypt_api_key(encrypted)
            assert decrypted == test_key  # Should decrypt correctly

    async def test_encryption_key_from_environment(self):
        """Test encryption key handling from environment."""
        # Test with custom key
        custom_key = "S1JwNXY2Z1hrY1NhcUxXR3VZM3pNMHh3cU1mWWVEejVQYk09"
        os.environ["AUTOMAGIK_SPARK_ENCRYPTION_KEY"] = custom_key
        
        retrieved_key = WorkflowSource._get_encryption_key()
        assert retrieved_key == custom_key
        
        # Clean up
        del os.environ["AUTOMAGIK_SPARK_ENCRYPTION_KEY"]


class TestURLHandling:
    """Test cases for URL handling and normalization."""
    
    async def test_url_trailing_slash_removed(self, client, clean_env, auth_headers, mock_langflow_response):
        """Test that trailing slashes are removed from URLs."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health and version checks
            health_mock = AsyncMock()
            health_mock.json.return_value = mock_langflow_response
            health_mock.raise_for_status = AsyncMock()
            
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "1.0.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            source_data = {
                "name": "Trailing Slash Test",
                "source_type": "langflow",
                "url": "http://localhost:7860/",  # Note trailing slash
                "api_key": "test-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            assert response.status_code == 201
            
            data = response.json()
            assert data["url"] == "http://localhost:7860"  # No trailing slash

    async def test_url_validation_with_ports(self, client, clean_env, auth_headers, mock_langflow_response):
        """Test URL validation works with different ports."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health and version checks
            health_mock = AsyncMock()
            health_mock.json.return_value = mock_langflow_response
            health_mock.raise_for_status = AsyncMock()
            
            version_mock = AsyncMock()
            version_mock.json.return_value = {"version": "1.0.0", "status": "ok"}
            version_mock.raise_for_status = AsyncMock()
            
            mock_get.side_effect = [health_mock, version_mock]
            
            test_urls = [
                "http://localhost:7860",
                "https://example.com:443",
                "http://192.168.1.100:8080"
            ]
            
            for i, url in enumerate(test_urls):
                source_data = {
                    "name": f"URL Test {i}",
                    "source_type": "langflow",
                    "url": url,
                    "api_key": "test-key"
                }
                
                response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
                assert response.status_code == 201
                data = response.json()
                assert data["url"] == url


class TestErrorHandling:
    """Test cases for error handling and edge cases."""
    
    async def test_network_timeout(self, client, clean_env, auth_headers):
        """Test handling of network timeouts during validation."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock network timeout
            mock_get.side_effect = httpx.TimeoutException("Request timeout")
            
            source_data = {
                "name": "Timeout Test Source",
                "source_type": "langflow",
                "url": "http://localhost:7860",
                "api_key": "test-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            assert response.status_code == 400
            assert "Failed to validate source" in response.json()["detail"]

    async def test_invalid_json_response(self, client, clean_env, auth_headers):
        """Test handling of invalid JSON responses during validation."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock health check with invalid JSON
            health_mock = AsyncMock()
            health_mock.json.side_effect = ValueError("Invalid JSON")
            health_mock.raise_for_status = AsyncMock()
            
            mock_get.return_value = health_mock
            
            source_data = {
                "name": "Invalid JSON Source",
                "source_type": "langflow",
                "url": "http://localhost:7860", 
                "api_key": "test-key"
            }
            
            response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
            assert response.status_code == 400

    async def test_missing_required_fields(self, client, clean_env, auth_headers):
        """Test validation of required fields."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        # Missing source_type
        response = client.post("/api/v1/sources/", json={
            "name": "Missing Type",
            "url": "http://localhost:7860",
            "api_key": "test-key"
        }, headers=auth_headers)
        assert response.status_code == 422
        
        # Missing URL
        response = client.post("/api/v1/sources/", json={
            "name": "Missing URL",
            "source_type": "langflow",
            "api_key": "test-key"
        }, headers=auth_headers)
        assert response.status_code == 422

    async def test_invalid_source_type(self, client, clean_env, auth_headers):
        """Test validation of source type enum."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        response = client.post("/api/v1/sources/", json={
            "name": "Invalid Type",
            "source_type": "invalid-type",
            "url": "http://localhost:7860",
            "api_key": "test-key"
        }, headers=auth_headers)
        assert response.status_code == 422

    async def test_invalid_uuid_format(self, client, clean_env, auth_headers):
        """Test handling of invalid UUID formats in path parameters."""
        os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
        
        invalid_ids = ["not-a-uuid", "12345", "", "uuid-but-invalid-format"]
        
        for invalid_id in invalid_ids:
            # Test GET
            response = client.get(f"/api/v1/sources/{invalid_id}", headers=auth_headers)
            assert response.status_code == 422
            
            # Test PATCH
            response = client.patch(f"/api/v1/sources/{invalid_id}", json={"name": "test"}, headers=auth_headers)
            assert response.status_code == 422
            
            # Test DELETE
            response = client.delete(f"/api/v1/sources/{invalid_id}", headers=auth_headers)
            assert response.status_code == 422