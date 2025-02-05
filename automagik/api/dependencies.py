"""API dependencies."""
from typing import Optional
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from .config import get_api_key
from ..core.database.session import get_async_session

X_API_KEY = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(X_API_KEY)) -> str:
    """
    Verify the API key from the X-API-Key header.
    If AUTOMAGIK_API_KEY is not set, all requests are allowed.
    """
    configured_api_key = get_api_key()
    
    # If no API key is configured, allow all requests
    if not configured_api_key:
        # If a key is provided, return it; otherwise return "anonymous"
        return api_key if api_key else "anonymous"
    
    # If API key is configured but not provided in request
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # If API key is configured and provided but doesn't match
    if api_key != configured_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return api_key

# Use the FastAPI-compatible session dependency
get_session = get_async_session
