"""API configuration."""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

def get_cors_origins() -> List[str]:
    """Get CORS origins from environment variable."""
    cors_origins = os.getenv("AUTOMAGIK_API_CORS", "http://localhost:3000,http://localhost:8000")
    return [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

def get_api_host() -> str:
    """Get the API host from environment variable or default."""
    return os.environ.get("AUTOMAGIK_API_HOST", "0.0.0.0")

def get_api_port() -> int:
    """Get API port from environment variable."""
    port_str = os.getenv("AUTOMAGIK_API_PORT", "8888")
    try:
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError(f"Port {port} is out of valid range (1-65535)")
        return port
    except ValueError:
        raise ValueError(f"Invalid port number: {port_str}")

def get_api_key() -> str | None:
    """Get API key from environment variable."""
    return os.getenv("AUTOMAGIK_API_KEY")

# LangFlow API configuration
LANGFLOW_API_URL = os.getenv("LANGFLOW_API_URL", "http://localhost:7860")
LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY")

def get_langflow_api_url() -> str:
    """Get LangFlow API URL."""
    return LANGFLOW_API_URL

def get_langflow_api_key() -> str:
    """Get LangFlow API key."""
    return LANGFLOW_API_KEY
