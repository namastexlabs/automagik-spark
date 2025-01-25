"""API dependencies."""
from typing import Optional
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from .config import get_api_key

X_API_KEY = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(X_API_KEY)) -> str:
    """
    Verify the API key from the X-API-Key header.
    If AUTOMAGIK_API_KEY is not set, all requests are allowed.
    """
    configured_api_key = get_api_key()
    
    if not configured_api_key:
        # If no API key is configured, allow all requests
        return "anonymous"
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if api_key != configured_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return api_key
