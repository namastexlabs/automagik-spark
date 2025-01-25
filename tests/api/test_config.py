"""Tests for the API configuration module."""
import os
import pytest
from automagik.api.config import get_cors_origins, get_api_host, get_api_port, get_api_key

def test_get_cors_origins_default():
    """Test get_cors_origins returns default values when env var is not set."""
    if "AUTOMAGIK_API_CORS" in os.environ:
        del os.environ["AUTOMAGIK_API_CORS"]
    
    origins = get_cors_origins()
    assert isinstance(origins, list)
    assert len(origins) == 2
    assert "http://localhost:3000" in origins
    assert "http://localhost:8000" in origins

def test_get_cors_origins_custom():
    """Test get_cors_origins returns custom values from env var."""
    os.environ["AUTOMAGIK_API_CORS"] = "http://example.com,http://test.com"
    
    origins = get_cors_origins()
    assert isinstance(origins, list)
    assert len(origins) == 2
    assert "http://example.com" in origins
    assert "http://test.com" in origins

def test_get_api_host_default():
    """Test get_api_host returns default value when env var is not set."""
    if "AUTOMAGIK_API_HOST" in os.environ:
        del os.environ["AUTOMAGIK_API_HOST"]
    
    host = get_api_host()
    assert host == "0.0.0.0"

def test_get_api_host_custom():
    """Test get_api_host returns custom value from env var."""
    os.environ["AUTOMAGIK_API_HOST"] = "127.0.0.1"
    assert get_api_host() == "127.0.0.1"

def test_get_api_port_default():
    """Test get_api_port returns default value when env var is not set."""
    if "AUTOMAGIK_API_PORT" in os.environ:
        del os.environ["AUTOMAGIK_API_PORT"]
    
    port = get_api_port()
    assert isinstance(port, int)
    assert port == 8000

def test_get_api_port_custom():
    """Test get_api_port returns custom value from env var."""
    os.environ["AUTOMAGIK_API_PORT"] = "9000"
    assert get_api_port() == 9000

def test_get_api_port_invalid():
    """Test get_api_port raises ValueError for invalid port."""
    os.environ["AUTOMAGIK_API_PORT"] = "invalid"
    with pytest.raises(ValueError):
        get_api_port()

def test_get_api_key():
    """Test get_api_key returns None when not set."""
    if "AUTOMAGIK_API_KEY" in os.environ:
        del os.environ["AUTOMAGIK_API_KEY"]
    assert get_api_key() is None

def test_get_api_key_custom():
    """Test get_api_key returns value from env var."""
    test_key = "test-api-key"
    os.environ["AUTOMAGIK_API_KEY"] = test_key
    assert get_api_key() == test_key
