from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_cors_origins

app = FastAPI(
    title="AutoMagik API",
    description="AutoMagik - Automated workflow management with LangFlow integration",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS with environment variables
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint returning API status"""
    return {
        "status": "online",
        "service": "AutoMagik API",
        "version": "0.1.0"
    }

# Import and include your API routers here
# Example:
# from .routers import tasks, workflows
# app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
# app.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
