"""API configuration module."""
import os
from typing import List

def get_cors_origins() -> List[str]:
    """Get CORS origins from environment variable."""
    cors_str = os.getenv("AUTOMAGIK_API_CORS", "http://localhost:3000,http://localhost:8000")
    return [origin.strip() for origin in cors_str.split(",") if origin.strip()]

def get_api_host() -> str:
    """Get API host from environment variable."""
    return os.getenv("AUTOMAGIK_API_HOST", "0.0.0.0")

def get_api_port() -> int:
    """Get API port from environment variable."""
    return int(os.getenv("AUTOMAGIK_API_PORT", "8000"))

def get_api_key() -> str | None:
    """Get API key from environment variable."""
    return os.getenv("AUTOMAGIK_API_KEY")
