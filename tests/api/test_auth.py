
"""Tests for API authentication."""
import os
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from automagik_spark.api.app import app
from automagik_spark.api.dependencies import verify_api_key

TEST_API_KEY = "test-key"

# Mark all tests to use session-scoped event loop
pytestmark = pytest.mark.asyncio(loop_scope="session")

@pytest.fixture
def clean_env():
    """Clean up environment variables before and after each test."""
    # Store original value
    original_key = os.environ.get("SPARK_API_KEY")
    if "SPARK_API_KEY" in os.environ:
        del os.environ["SPARK_API_KEY"]
    
    yield
    
    # Restore original value
    if original_key is not None:
        os.environ["SPARK_API_KEY"] = original_key
    elif "SPARK_API_KEY" in os.environ:
        del os.environ["SPARK_API_KEY"]

@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)

async def test_api_no_key_configured(client, clean_env):
    """Test API when no API key is configured."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

async def test_api_key_required(client, clean_env):
    """Test API key is required when configured."""
    os.environ["SPARK_API_KEY"] = TEST_API_KEY
    response = client.get("/")
    assert response.status_code == 401
    error = response.json()
    assert "detail" in error
    assert "X-API-Key header is missing" in error["detail"]

async def test_api_key_valid(client, clean_env):
    """Test API key authentication works."""
    os.environ["SPARK_API_KEY"] = TEST_API_KEY
    headers = {"X-API-Key": TEST_API_KEY}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "online"

async def test_api_key_invalid(client, clean_env):
    """Test invalid API key is rejected."""
    os.environ["SPARK_API_KEY"] = TEST_API_KEY
    headers = {"X-API-Key": "wrong-key"}
    response = client.get("/", headers=headers)
    assert response.status_code == 401
    error = response.json()
    assert "detail" in error
    assert "Invalid API key" in error["detail"]

async def test_verify_api_key_no_key_configured(clean_env):
    """Test verify_api_key when no key is configured."""
    # When no key is configured, any key should be accepted
    result = await verify_api_key("some-key")
    assert result == "some-key"
    
    # Missing key should return anonymous
    result = await verify_api_key(None)
    assert result == "anonymous"

async def test_verify_api_key_with_key_configured(clean_env):
    """Test verify_api_key with configured key."""
    os.environ["SPARK_API_KEY"] = TEST_API_KEY
    
    # Valid key should be accepted
    result = await verify_api_key(TEST_API_KEY)
    assert result == TEST_API_KEY
    
    # Invalid key should raise HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await verify_api_key("wrong-key")
    assert exc_info.value.status_code == 401
    assert "Invalid API key" in exc_info.value.detail
    
    # Missing key should raise HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await verify_api_key(None)
    assert exc_info.value.status_code == 401
    assert "X-API-Key header is missing" in exc_info.value.detail

async def test_api_key_case_sensitive(client, clean_env):
    """Test API key validation is case-sensitive."""
    os.environ["SPARK_API_KEY"] = TEST_API_KEY
    headers = {"X-API-Key": TEST_API_KEY.upper()}
    response = client.get("/", headers=headers)
    assert response.status_code == 401
    error = response.json()
    assert "detail" in error
    assert "Invalid API key" in error["detail"]

async def test_api_key_whitespace(client, clean_env):
    """Test API key validation with whitespace."""
    os.environ["SPARK_API_KEY"] = TEST_API_KEY
    headers = {"X-API-Key": f" {TEST_API_KEY} "}
    response = client.get("/", headers=headers)
    assert response.status_code == 401
    error = response.json()
    assert "detail" in error
    assert "Invalid API key" in error["detail"]


