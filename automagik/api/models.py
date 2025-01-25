"""API models for request/response validation."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str = Field(..., description="Error detail message")

class TaskBase(BaseModel):
    """Base model for task operations."""
    name: str = Field(..., description="Task name")
    flow_id: str = Field(..., description="ID of the flow this task belongs to")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")

class TaskCreate(TaskBase):
    """Model for creating a new task."""
    schedule: Optional[str] = Field(None, description="Cron schedule expression")

class TaskResponse(TaskBase):
    """Model for task response."""
    id: str = Field(..., description="Task ID")
    status: str = Field(..., description="Task status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")

class FlowBase(BaseModel):
    """Base model for flow operations."""
    name: str = Field(..., description="Flow name")
    description: Optional[str] = Field(None, description="Flow description")
    config: Dict[str, Any] = Field(..., description="Flow configuration")

class FlowCreate(FlowBase):
    """Model for creating a new flow."""
    pass

class FlowResponse(FlowBase):
    """Model for flow response."""
    id: str = Field(..., description="Flow ID")
    created_at: datetime = Field(..., description="Flow creation timestamp")
    updated_at: datetime = Field(..., description="Flow last update timestamp")

class ScheduleBase(BaseModel):
    """Base model for schedule operations."""
    name: str = Field(..., description="Schedule name")
    cron_expression: str = Field(..., description="Cron expression for the schedule")
    task_id: str = Field(..., description="ID of the task to schedule")
    enabled: bool = Field(default=True, description="Whether the schedule is enabled")

class ScheduleCreate(ScheduleBase):
    """Model for creating a new schedule."""
    pass

class ScheduleResponse(ScheduleBase):
    """Model for schedule response."""
    id: str = Field(..., description="Schedule ID")
    created_at: datetime = Field(..., description="Schedule creation timestamp")
    updated_at: datetime = Field(..., description="Schedule last update timestamp")
    last_run: Optional[datetime] = Field(None, description="Last execution timestamp")
    next_run: Optional[datetime] = Field(None, description="Next scheduled execution timestamp")

class WorkerStatus(BaseModel):
    """Model for worker status."""
    id: str = Field(..., description="Worker ID")
    status: str = Field(..., description="Worker status")
    last_heartbeat: datetime = Field(..., description="Last heartbeat timestamp")
    current_task: Optional[str] = Field(None, description="Current task ID if any")
    stats: Dict[str, Any] = Field(default_factory=dict, description="Worker statistics")
