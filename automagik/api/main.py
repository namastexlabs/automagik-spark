"""
API Module for AutoMagik
"""

from fastapi import FastAPI, HTTPException, Depends, Query, Security, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List, Optional
import logging
import sys
import traceback
import uvicorn
from sqlalchemy import text
from uuid import UUID

from automagik.core.database.session import get_db_session
from automagik.core.database.models import FlowDB, Schedule, Task, Log
from automagik.core.services.flow_manager import FlowManager
from automagik.api.security import get_api_key
from automagik.core.services.langflow_client import LangflowClient
from automagik.api import schemas
from automagik.core.scheduler import SchedulerService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for all unhandled exceptions"""
    error_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    error_detail = {
        'error_id': error_id,
        'type': exc.__class__.__name__,
        'detail': str(exc)
    }
    
    # Log the full error with stack trace
    logger.error(f"Error ID: {error_id}")
    logger.error(f"Request: {request.method} {request.url}")
    logger.error("Exception occurred:", exc_info=True)
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_detail
        )
    elif isinstance(exc, SQLAlchemyError):
        logger.error("Database error:", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                **error_detail,
                'detail': 'Database error occurred. Please try again later.'
            }
        )
    
    return JSONResponse(
        status_code=500,
        content=error_detail
    )

# Health check endpoint
@app.get("/health")
def health_check():
    """Check service health including database connection."""
    try:
        # Test database connection
        with get_db_session() as db:
            # Try a simple query
            db.execute(text("SELECT 1"))
            
        # Test Redis connection if used
        # redis_client.ping()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("Health check failed:", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

# Flow endpoints
@app.get("/flows", response_model=schemas.FlowList)
async def list_flows(
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List all flows"""
    try:
        logger.info("Fetching all flows")
        flows = db.query(FlowDB).all()
        flow_responses = [schemas.FlowResponse.from_db(flow) for flow in flows]
        logger.info(f"Successfully fetched {len(flow_responses)} flows")
        return {"flows": flow_responses}
        
    except SQLAlchemyError as e:
        logger.error("Database error while fetching flows:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching flows"
        )
    except Exception as e:
        logger.error("Unexpected error while fetching flows:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/flows/{flow_id}", response_model=schemas.FlowResponse)
async def get_flow(
    flow_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get flow details"""
    try:
        logger.info(f"Fetching flow {flow_id}")
        try:
            flow_uuid = UUID(flow_id)
        except ValueError:
            logger.error(f"Invalid UUID format for flow_id: {flow_id}")
            raise HTTPException(status_code=422, detail="Invalid UUID format")
            
        flow = db.query(FlowDB).filter(FlowDB.id == flow_uuid).first()
        if not flow:
            logger.error(f"Flow {flow_id} not found")
            raise HTTPException(status_code=404, detail="Flow not found")
        
        logger.info(f"Successfully fetched flow {flow_id}")
        return schemas.FlowResponse.from_db(flow)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching flow {flow_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching flow"
        )
    except Exception as e:
        logger.error(f"Unexpected error while fetching flow {flow_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

# Schedule endpoints
@app.get("/schedules", response_model=schemas.ScheduleList)
async def list_schedules(
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List all schedules"""
    try:
        logger.info("Fetching all schedules")
        schedules = db.query(Schedule).all()
        schedule_responses = [schemas.ScheduleResponse.from_db(schedule) for schedule in schedules]
        logger.info(f"Successfully fetched {len(schedule_responses)} schedules")
        return {"schedules": schedule_responses}
        
    except SQLAlchemyError as e:
        logger.error("Database error while fetching schedules:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching schedules"
        )
    except Exception as e:
        logger.error("Unexpected error while fetching schedules:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/schedules/{schedule_id}", response_model=schemas.ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get schedule details"""
    try:
        logger.info(f"Fetching schedule {schedule_id}")
        try:
            schedule_uuid = UUID(schedule_id)
        except ValueError:
            logger.error(f"Invalid UUID format for schedule_id: {schedule_id}")
            raise HTTPException(status_code=422, detail="Invalid UUID format")
            
        schedule = db.query(Schedule).filter(Schedule.id == schedule_uuid).first()
        if not schedule:
            logger.error(f"Schedule {schedule_id} not found")
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        logger.info(f"Successfully fetched schedule {schedule_id}")
        return schemas.ScheduleResponse.from_db(schedule)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching schedule {schedule_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching schedule"
        )
    except Exception as e:
        logger.error(f"Unexpected error while fetching schedule {schedule_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

# Task endpoints
@app.get("/tasks", response_model=schemas.TaskList)
async def list_tasks(
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List all tasks"""
    try:
        logger.info("Fetching all tasks")
        tasks = db.query(Task).all()
        task_responses = [schemas.TaskResponse.from_db(task) for task in tasks]
        logger.info(f"Successfully fetched {len(task_responses)} tasks")
        return {"tasks": task_responses}
        
    except SQLAlchemyError as e:
        logger.error("Database error while fetching tasks:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching tasks"
        )
    except Exception as e:
        logger.error("Unexpected error while fetching tasks:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task(
    task_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get task details"""
    try:
        logger.info(f"Fetching task {task_id}")
        try:
            task_uuid = UUID(task_id)
        except ValueError:
            logger.error(f"Invalid UUID format for task_id: {task_id}")
            raise HTTPException(status_code=422, detail="Invalid UUID format")
            
        task = db.query(Task).filter(Task.id == task_uuid).first()
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail="Task not found")
        
        logger.info(f"Successfully fetched task {task_id}")
        return schemas.TaskResponse.from_db(task)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching task {task_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching task"
        )
    except Exception as e:
        logger.error(f"Unexpected error while fetching task {task_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
