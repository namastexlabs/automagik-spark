from fastapi import FastAPI, HTTPException, Depends, Query, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import uvicorn

from core.database import get_db_session
from core.database.models import FlowDB, Schedule, Task
from core.flows import FlowManager
from core.scheduler import SchedulerService
from core.services.langflow_client import LangflowClient
from . import schemas
from .security import get_api_key

app = FastAPI(
    title="AutoMagik API",
    description="API for managing LangFlow workflows and schedules",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=schemas.HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

# Flow endpoints
@app.get("/flows", response_model=schemas.FlowList)
async def list_flows(
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List all flows"""
    flows = db.query(FlowDB).all()
    return {"flows": flows}

@app.get("/flows/{flow_id}", response_model=schemas.FlowResponse)
async def get_flow(
    flow_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get flow details"""
    flow = db.query(FlowDB).filter(FlowDB.id == flow_id).first()
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    return flow

# Schedule endpoints
@app.get("/schedules", response_model=schemas.ScheduleList)
async def list_schedules(
    flow_id: Optional[str] = None,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List all schedules, optionally filtered by flow"""
    query = db.query(Schedule)
    if flow_id:
        query = query.filter(Schedule.flow_id == flow_id)
    schedules = query.all()
    return {"schedules": schedules}

@app.get("/schedules/{schedule_id}", response_model=schemas.ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get schedule details"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

# Task endpoints
@app.get("/tasks", response_model=schemas.TaskList)
async def list_tasks(
    flow_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=100),
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List tasks with optional filters"""
    query = db.query(Task)
    if flow_id:
        query = query.filter(Task.flow_id == flow_id)
    if status:
        query = query.filter(Task.status == status)
    tasks = query.limit(limit).all()
    return {"tasks": tasks}

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task(
    task_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get task details including logs and output"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
