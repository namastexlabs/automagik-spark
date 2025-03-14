"""Main FastAPI application module."""

import datetime
from fastapi import FastAPI, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from automagik.version import __version__
from .config import get_cors_origins, get_api_key
from ..core.config import get_settings
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

# Custom OpenAPI schema to include security components
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add API Key security scheme
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key authentication"
        },
        "APIKeyQuery": {
            "type": "apiKey",
            "in": "query",
            "name": "api_key",
            "description": "API key authentication via query parameter"
        }
    }
    
    # Apply security to all endpoints except those that don't need auth
    security_requirement = [{"APIKeyHeader": []}, {"APIKeyQuery": []}]
    
    # These endpoints don't require authentication
    no_auth_paths = ["/health", "/", "/api/v1/docs", "/api/v1/redoc", "/api/v1/openapi.json"]
    
    # Update security for each path
    for path, path_item in openapi_schema["paths"].items():
        if path not in no_auth_paths:
            for operation in path_item.values():
                operation["security"] = security_requirement
                
                # Add authentication description to each endpoint
                if "description" in operation:
                    operation["description"] += "\n\n**Requires Authentication**: This endpoint requires an API key."
                else:
                    operation["description"] = "**Requires Authentication**: This endpoint requires an API key."
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Set the custom OpenAPI schema
app.openapi = custom_openapi

@app.get("/health")
async def health():
    """Health check endpoint"""
    current_time = datetime.datetime.now()
    return {
        "status": "healthy",
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/")
async def root():
    """Root endpoint returning API status"""
    current_time = datetime.datetime.now()
    settings = get_settings()
    base_url = settings.remote_url
    return {
        "status": 200,
        "service": "AutoMagik API",
        "message": "Welcome to AutoMagik API, it's up and running!",
        "version": __version__,
        "server_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "docs_url": f"{base_url}/api/v1/docs",
        "redoc_url": f"{base_url}/api/v1/redoc",
        "openapi_url": f"{base_url}/api/v1/openapi.json",
    }


# Add routers with /api/v1 prefix
app.include_router(workflows.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(schedules.router, prefix="/api/v1")
app.include_router(sources.router, prefix="/api/v1")
