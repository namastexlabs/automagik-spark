from pydantic import BaseModel, Field, UUID4, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    
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
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime

class FlowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(..., description="Unique identifier of the flow")
    name: str = Field(..., description="Name of the flow")
    description: Optional[str] = Field(None, description="Description of the flow")
    source: str = Field(..., description="Source of the flow (e.g., langflow)")
    source_id: str = Field(..., description="ID of the flow in the source system")
    data: Dict[str, Any] = Field(..., description="Flow configuration data")
    created_at: datetime = Field(..., description="Flow creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Flow last update timestamp")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the flow")

    @classmethod
    def from_db(cls, flow):
        return cls(
            id=str(flow.id),
            name=flow.name,
            description=flow.description,
            source=flow.source,
            source_id=str(flow.source_id) if flow.source_id else None,
            data=flow.data,
            created_at=flow.created_at,
            updated_at=flow.updated_at,
            tags=flow.tags or []
        )

class FlowList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    flows: List[FlowResponse]

class ScheduleBase(BaseModel):
    flow_id: UUID
    schedule_type: str = Field(..., description="Type of schedule (e.g., cron, interval)")
    schedule_expr: str = Field(..., description="Schedule expression (e.g., cron expression or interval)")
    flow_params: Dict[str, Any] = Field(default_factory=dict, description="Parameters to pass to the flow")
    status: str = Field(..., description="Schedule status (e.g., active, paused)")
    next_run_at: Optional[datetime] = Field(None, description="Next scheduled run time")

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None

    @classmethod
    def from_db(cls, db_schedule):
        """Convert database model to API model."""
        return cls(
            id=db_schedule.id,
            flow_id=db_schedule.flow_id,
            schedule_type=db_schedule.schedule_type,
            schedule_expr=db_schedule.schedule_expr,
            flow_params=db_schedule.flow_params,
            status=db_schedule.status,
            next_run_at=db_schedule.next_run_at,
            created_at=db_schedule.created_at,
            updated_at=db_schedule.updated_at
        )

class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    flow_id: str
    schedule_type: str
    schedule_expr: str
    flow_params: Optional[Dict[str, Any]] = None
    status: str
    next_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_db(cls, schedule):
        return cls(
            id=str(schedule.id),
            flow_id=str(schedule.flow_id),
            schedule_type=schedule.schedule_type,
            schedule_expr=schedule.schedule_expr,
            flow_params=schedule.flow_params,
            status=schedule.status,
            next_run_at=schedule.next_run_at,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at
        )

class ScheduleList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    schedules: List[ScheduleResponse]

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
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    logs: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    flow_id: str
    status: str
    input_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tries: int = Field(default=0)
    max_retries: int = Field(default=3)
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_db(cls, task):
        return cls(
            id=str(task.id),
            flow_id=str(task.flow_id),
            status=task.status,
            input_data=task.input_data,
            output_data=task.output_data,
            tries=task.tries,
            max_retries=task.max_retries,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

class TaskList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    tasks: List[TaskResponse]
