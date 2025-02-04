"""Tests for the API configuration module."""
import os
import pytest
from unittest.mock import patch
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
    """Test getting the default API host."""
    host = get_api_host()
    assert host == "0.0.0.0"

def test_get_api_host_custom():
    """Test getting a custom API host."""
    with patch.dict(os.environ, {"AUTOMAGIK_API_HOST": "0.0.0.0"}):
        host = get_api_host()
        assert host == "0.0.0.0"

def test_get_api_port_default():
    """Test getting the default API port."""
    port = get_api_port()
    assert port == 8888

def test_get_api_port_custom():
    """Test getting a custom API port."""
    with patch.dict(os.environ, {"AUTOMAGIK_API_PORT": "8888"}):
        port = get_api_port()
        assert port == 8888

def test_get_api_port_invalid():
    """Test getting an invalid API port."""
    with patch.dict(os.environ, {"AUTOMAGIK_API_PORT": "invalid"}):
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
