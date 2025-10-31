"""API configuration."""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


def get_cors_origins() -> List[str]:
    """Get CORS origins from environment variable."""
    cors_origins = os.getenv("AUTOMAGIK_SPARK_API_CORS", "http://localhost:3000,http://localhost:8883")
    return [origin.strip() for origin in cors_origins.split(",") if origin.strip()]


def get_api_host() -> str:
    """Get the Spark API host from environment variable or default."""
    return os.environ.get("AUTOMAGIK_SPARK_API_HOST", "0.0.0.0")


def get_api_port() -> int:
    """Get Spark API port from environment variable."""
    port_str = os.getenv("AUTOMAGIK_SPARK_API_PORT", "8883")
    try:
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError(f"Port {port} is out of valid range (1-65535)")
        return port
    except ValueError:
        raise ValueError(f"Invalid port number: {port_str}")


def get_api_key() -> str | None:
    """Get API key from environment variable."""
    return os.getenv("AUTOMAGIK_SPARK_API_KEY")


def get_langflow_api_url() -> str:
    """Get LangFlow API URL."""
    return os.getenv("LANGFLOW_API_URL", "http://localhost:7860")


def get_langflow_api_key() -> str | None:
    """Get LangFlow API key."""
    return os.getenv("LANGFLOW_API_KEY")


def get_database_url() -> str:
    """Get database URL from environment variable."""
    database_url = os.getenv("AUTOMAGIK_SPARK_DATABASE_URL")
    if not database_url:
        raise ValueError("AUTOMAGIK_SPARK_DATABASE_URL environment variable is not set")
    return database_url


def get_agents_api_port() -> int:
    """Get AutoMagik Agents API port from environment variable."""
    port_str = os.getenv("AUTOMAGIK_API_PORT", "8881")
    try:
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError(f"Port {port} is out of valid range (1-65535)")
        return port
    except ValueError:
        raise ValueError(f"Invalid port number: {port_str}")


def get_agents_api_host() -> str:
    """Get AutoMagik Agents API host from environment variable or default."""
    return os.environ.get("AUTOMAGIK_API_HOST", "localhost")


def get_http_timeout() -> float:
    """Get HTTP client timeout in seconds from environment variable.

    This timeout applies to all HTTP requests made to external workflow sources
    (AutoMagik Agents, AutoMagik Hive, LangFlow).

    Default: 600 seconds (10 minutes) for long-running workflow executions.
    Minimum: 30 seconds to prevent premature timeouts.
    Maximum: 3600 seconds (1 hour) to prevent indefinite hangs.

    Returns:
        float: Timeout in seconds

    Environment Variable:
        AUTOMAGIK_SPARK_HTTP_TIMEOUT: Timeout in seconds (default: 600)
    """
    timeout_str = os.getenv("AUTOMAGIK_SPARK_HTTP_TIMEOUT", "600")
    try:
        timeout = float(timeout_str)
        if timeout < 30:
            raise ValueError(f"Timeout {timeout} is below minimum (30 seconds)")
        if timeout > 3600:
            raise ValueError(f"Timeout {timeout} exceeds maximum (3600 seconds)")
        return timeout
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError(f"Invalid timeout value: {timeout_str}")
        raise
