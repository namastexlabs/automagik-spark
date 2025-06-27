
"""Tests for the API configuration module."""
import os
import pytest
from automagik_spark.api.config import (
    get_cors_origins,
    get_api_host,
    get_api_port,
    get_api_key,
    get_langflow_api_url,
    get_langflow_api_key
)

@pytest.fixture
def clean_env():
    """Fixture to clean environment variables before tests."""
    env_vars = [
        "AUTOMAGIK_API_CORS",
        "AUTOMAGIK_API_HOST",
        "AUTOMAGIK_API_PORT",
        "SPARK_API_KEY",
        "LANGFLOW_API_URL",
        "LANGFLOW_API_KEY"
    ]
    # Store original values
    original_values = {}
    for var in env_vars:
        if var in os.environ:
            original_values[var] = os.environ[var]
            del os.environ[var]
    
    yield
    
    # Restore original values
    for var, value in original_values.items():
        os.environ[var] = value

def test_get_cors_origins_default(clean_env):
    """Test get_cors_origins returns default values when env var is not set."""
    origins = get_cors_origins()
    assert isinstance(origins, list)
    assert len(origins) == 2
    assert "http://localhost:3000" in origins
    assert "http://localhost:8000" in origins

def test_get_cors_origins_custom(clean_env):
    """Test get_cors_origins returns custom values from env var."""
    test_origins = ["http://example.com", "http://test.com"]
    os.environ["AUTOMAGIK_API_CORS"] = ",".join(test_origins)
    
    origins = get_cors_origins()
    assert isinstance(origins, list)
    assert len(origins) == len(test_origins)
    for origin in test_origins:
        assert origin in origins

def test_get_cors_origins_empty(clean_env):
    """Test get_cors_origins with empty string."""
    os.environ["AUTOMAGIK_API_CORS"] = ""
    origins = get_cors_origins()
    assert isinstance(origins, list)
    assert len(origins) == 0

def test_get_api_host_default(clean_env):
    """Test getting the default API host."""
    host = get_api_host()
    assert host == "0.0.0.0"

def test_get_api_host_custom(clean_env):
    """Test getting a custom API host."""
    test_host = "127.0.0.1"
    os.environ["AUTOMAGIK_API_HOST"] = test_host
    host = get_api_host()
    assert host == test_host

def test_get_api_port_default(clean_env):
    """Test getting the default API port."""
    port = get_api_port()
    assert port == 8888
    assert isinstance(port, int)

def test_get_api_port_custom(clean_env):
    """Test getting a custom API port."""
    test_port = "9999"
    os.environ["AUTOMAGIK_API_PORT"] = test_port
    port = get_api_port()
    assert port == int(test_port)
    assert isinstance(port, int)

def test_get_api_port_invalid(clean_env):
    """Test getting an invalid API port."""
    os.environ["AUTOMAGIK_API_PORT"] = "invalid"
    with pytest.raises(ValueError):
        get_api_port()

def test_get_api_key_default(clean_env):
    """Test get_api_key returns None when not set."""
    api_key = get_api_key()
    assert api_key is None

def test_get_api_key_custom(clean_env):
    """Test get_api_key returns value from env var."""
    test_key = "test-api-key"
    os.environ["SPARK_API_KEY"] = test_key
    api_key = get_api_key()
    assert api_key == test_key

def test_get_langflow_api_url_default(clean_env):
    """Test get_langflow_api_url returns default when not set."""
    url = get_langflow_api_url()
    assert url == "http://localhost:7860"

def test_get_langflow_api_url_custom(clean_env):
    """Test get_langflow_api_url returns custom value."""
    test_url = "http://example.com:7860"
    os.environ["LANGFLOW_API_URL"] = test_url
    url = get_langflow_api_url()
    assert url == test_url

def test_get_langflow_api_key_default(clean_env):
    """Test get_langflow_api_key returns None when not set."""
    api_key = get_langflow_api_key()
    assert api_key is None

def test_get_langflow_api_key_custom(clean_env):
    """Test get_langflow_api_key returns custom value."""
    test_key = "test-langflow-key"
    os.environ["LANGFLOW_API_KEY"] = test_key
    api_key = get_langflow_api_key()
    assert api_key == test_key


