
"""Main FastAPI application module."""

import datetime
from fastapi import FastAPI, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader

from automagik.version import __version__
from .config import get_cors_origins, get_api_key
from .dependencies import verify_api_key
from .routers import tasks, workflows, schedules, sources

app = FastAPI(
    title="AutoMagik API",
    description="AutoMagik - Automated workflow management with LangFlow integration",
    version=__version__,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

# Configure CORS with environment variables
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key security scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@app.get("/health")
async def health():
    """Health check endpoint"""
    current_time = datetime.datetime.now()
    return {
        "status": "healthy",
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/")
async def root(api_key: str = Security(verify_api_key)):
    """Root endpoint returning API status"""
    current_time = datetime.datetime.now()
    return {
        "status": "online",
        "service": "AutoMagik API",
        "version": __version__,
        "server_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "docs_url": "/api/v1/docs",
        "redoc_url": "/api/v1/redoc",
    }


# Add routers with /api/v1 prefix
app.include_router(workflows.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(schedules.router, prefix="/api/v1")
app.include_router(sources.router, prefix="/api/v1")


