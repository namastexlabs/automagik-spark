from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
import os

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: Optional[str] = Security(api_key_header)) -> str:
    """Validate API key from header."""
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": API_KEY_NAME},
        )
    
    api_key = os.getenv("AUTOMAGIK_API_KEY")
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key is not configured",
        )
        
    if api_key_header != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": API_KEY_NAME},
        )
        
    return api_key_header
