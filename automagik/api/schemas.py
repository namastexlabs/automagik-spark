from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class HealthResponse(BaseModel):
    status: str = Field(..., description="Current health status of the API")
    timestamp: datetime = Field(..., description="Current server timestamp")

class FlowBase(BaseModel):
    name: str
    description: Optional[str] = None
    folder_name: Optional[str] = None
    source: str = "local"
    source_id: Optional[str] = None
    flow_version: Optional[int] = 1
    input_component: Optional[str] = None
    output_component: Optional[str] = None
    data: Dict[str, Any]

class FlowCreate(FlowBase):
    pass

class Flow(FlowBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FlowResponse(BaseModel):
    id: str = Field(..., description="Unique identifier of the flow")
    name: str = Field(..., description="Name of the flow")
    description: Optional[str] = Field(None, description="Description of the flow")
    source: str = Field(..., description="Source of the flow (e.g., langflow)")
    source_id: str = Field(..., description="ID of the flow in the source system")
    data: Dict[str, Any] = Field(..., description="Flow configuration data")
    created_at: datetime = Field(..., description="Flow creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Flow last update timestamp")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the flow")

class ScheduleBase(BaseModel):
    flow_id: UUID
    name: str
    description: Optional[str] = None
    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None
    input_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    enabled: bool = True
    max_retries: int = 3
    retry_delay: int = 60

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None

    class Config:
        from_attributes = True

class ScheduleResponse(BaseModel):
    id: str = Field(..., description="Unique identifier of the schedule")
    flow_id: str = Field(..., description="ID of the associated flow")
    schedule_type: str = Field(..., description="Type of schedule (e.g., interval, cron)")
    schedule_expr: str = Field(..., description="Schedule expression (e.g., '1h' for interval)")
    flow_params: Dict[str, Any] = Field(..., description="Parameters to pass to the flow")
    status: str = Field(..., description="Current status of the schedule")
    next_run_at: datetime = Field(..., description="Next scheduled run time")
    created_at: datetime = Field(..., description="Schedule creation timestamp")
    updated_at: datetime = Field(..., description="Schedule last update timestamp")

class TaskBase(BaseModel):
    flow_id: UUID
    schedule_id: Optional[UUID] = None
    input_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    status: str = "pending"
    tries: int = 0
    max_tries: int = 3
    retry_delay: int = 60

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    logs: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

    class Config:
        from_attributes = True

class TaskResponse(BaseModel):
    id: str = Field(..., description="Unique identifier of the task")
    flow_id: str = Field(..., description="ID of the associated flow")
    status: TaskStatus = Field(..., description="Current status of the task")
    input_data: Dict[str, Any] = Field(..., description="Input data for the task")
    output_data: Optional[Dict[str, Any]] = Field(None, description="Output data from the task")
    tries: int = Field(..., description="Number of execution attempts")
    max_retries: int = Field(..., description="Maximum number of retry attempts")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")

class FlowList(BaseModel):
    flows: List[FlowResponse] = Field(..., description="List of flows")

class ScheduleList(BaseModel):
    schedules: List[ScheduleResponse] = Field(..., description="List of schedules")

class TaskList(BaseModel):
    tasks: List[TaskResponse] = Field(..., description="List of tasks")
