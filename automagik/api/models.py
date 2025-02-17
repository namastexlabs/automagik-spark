
"""API models for request/response validation."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str = Field(..., description="Error detail message")

    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    """Base model for task operations."""
    workflow_id: str = Field(..., description="ID of the workflow this task belongs to")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Task input data")
    output_data: Optional[Dict[str, Any]] = Field(None, description="Task output data")
    error: Optional[str] = Field(None, description="Task error message")
    tries: Optional[int] = Field(0, description="Number of tries")
    max_retries: Optional[int] = Field(3, description="Maximum number of retries")
    next_retry_at: Optional[datetime] = Field(None, description="Next retry timestamp")
    started_at: Optional[datetime] = Field(None, description="Task start timestamp")
    finished_at: Optional[datetime] = Field(None, description="Task finish timestamp")

    model_config = ConfigDict(from_attributes=True)

class TaskCreate(TaskBase):
    """Model for creating a new task."""
    schedule: Optional[str] = Field(None, description="Cron schedule expression")

    model_config = ConfigDict(from_attributes=True)

class TaskResponse(TaskBase):
    """Model for task response."""
    id: str = Field(..., description="Task ID")
    status: str = Field(..., description="Task status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")

    @classmethod
    def model_validate(cls, obj: Any) -> "TaskResponse":
        """Convert a Task object to TaskResponse."""
        if hasattr(obj, "__dict__"):
            data = {
                "id": str(obj.id) if isinstance(obj.id, UUID) else obj.id,
                "workflow_id": str(obj.workflow_id) if isinstance(obj.workflow_id, UUID) else obj.workflow_id,
                "status": obj.status,
                "input_data": obj.input_data,
                "output_data": obj.output_data,
                "error": obj.error,
                "tries": obj.tries,
                "max_retries": obj.max_retries,
                "next_retry_at": obj.next_retry_at,
                "started_at": obj.started_at,
                "finished_at": obj.finished_at,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at
            }
            return super().model_validate(data)
        return super().model_validate(obj)

    model_config = ConfigDict(from_attributes=True)

class WorkflowBase(BaseModel):
    """Base model for workflow operations."""
    name: str = Field(..., description="Workflow name")
    description: Optional[str] = Field(None, description="Workflow description")
    source: str = Field(..., description="Source system name")
    remote_flow_id: str = Field(..., description="ID of the remote flow")
    flow_version: Optional[int] = Field(1, description="Flow version")
    input_component: Optional[str] = Field(None, description="Input component ID")
    output_component: Optional[str] = Field(None, description="Output component ID")
    is_component: Optional[bool] = Field(False, description="Whether the workflow is a component")
    folder_id: Optional[str] = Field(None, description="Folder ID")
    folder_name: Optional[str] = Field(None, description="Folder name")
    icon: Optional[str] = Field(None, description="Icon name")
    icon_bg_color: Optional[str] = Field(None, description="Icon background color")
    gradient: Optional[bool] = Field(False, description="Whether to use gradient")
    liked: Optional[bool] = Field(False, description="Whether the workflow is liked")
    tags: Optional[List[str]] = Field(default_factory=list, description="Workflow tags")
    data: Dict[str, Any] = Field(default_factory=dict, description="Workflow data")

    model_config = ConfigDict(from_attributes=True)

class WorkflowCreate(WorkflowBase):
    """Model for creating a new workflow."""
    pass

    model_config = ConfigDict(from_attributes=True)

class WorkflowResponse(WorkflowBase):
    """Model for workflow response."""
    id: str = Field(..., description="Workflow ID")
    created_at: datetime = Field(..., description="Workflow creation timestamp")
    updated_at: datetime = Field(..., description="Workflow last update timestamp")

    @classmethod
    def model_validate(cls, obj: Any) -> "WorkflowResponse":
        """Convert a Workflow object to WorkflowResponse."""
        if hasattr(obj, "__dict__"):
            data = {
                "id": str(obj.id) if isinstance(obj.id, UUID) else obj.id,
                "name": obj.name,
                "description": obj.description,
                "source": obj.source,
                "remote_flow_id": obj.remote_flow_id,
                "flow_version": obj.flow_version,
                "input_component": obj.input_component,
                "output_component": obj.output_component,
                "is_component": obj.is_component,
                "folder_id": obj.folder_id,
                "folder_name": obj.folder_name,
                "icon": obj.icon,
                "icon_bg_color": obj.icon_bg_color,
                "gradient": obj.gradient,
                "liked": obj.liked,
                "tags": obj.tags,
                "data": obj.data,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at
            }
            return super().model_validate(data)
        return super().model_validate(obj)

    model_config = ConfigDict(from_attributes=True)

class ScheduleBase(BaseModel):
    """Base model for schedule operations."""
    workflow_id: str = Field(..., description="ID of the workflow this schedule belongs to")
    schedule_type: str = Field(..., description="Type of schedule (cron, interval, or one-time)")
    schedule_expr: str = Field(..., description="Schedule expression (cron expression, interval like '1h', or datetime/now for one-time)")
    input_value: Optional[str] = Field(None, description="Input string to be passed to the workflow's input component")
    status: str = Field("active", description="Schedule status")
    next_run_at: Optional[datetime] = Field(None, description="Next run timestamp")

    model_config = ConfigDict(from_attributes=True)

class ScheduleCreate(ScheduleBase):
    """Model for creating a new schedule."""
    pass

    model_config = ConfigDict(from_attributes=True)

class ScheduleResponse(ScheduleBase):
    """Model for schedule response."""
    id: str = Field(..., description="Schedule ID")
    created_at: datetime = Field(..., description="Schedule creation timestamp")
    updated_at: datetime = Field(..., description="Schedule last update timestamp")

    @classmethod
    def model_validate(cls, obj: Any) -> "ScheduleResponse":
        """Convert a Schedule object to ScheduleResponse."""
        if hasattr(obj, "__dict__"):
            data = {
                "id": str(obj.id) if isinstance(obj.id, UUID) else obj.id,
                "workflow_id": str(obj.workflow_id) if isinstance(obj.workflow_id, UUID) else obj.workflow_id,
                "schedule_type": obj.schedule_type,
                "schedule_expr": obj.schedule_expr,
                "input_value": obj.input_data,
                "status": obj.status,
                "next_run_at": obj.next_run_at,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at
            }
            return super().model_validate(data)
        return super().model_validate(obj)

    model_config = ConfigDict(from_attributes=True)

class WorkerStatus(BaseModel):
    """Model for worker status."""
    id: str = Field(..., description="Worker ID")
    status: str = Field(..., description="Worker status")
    last_heartbeat: datetime = Field(..., description="Last heartbeat timestamp")
    current_task: Optional[str] = Field(None, description="Current task ID if any")
    stats: Dict[str, Any] = Field(default_factory=dict, description="Worker statistics")

    model_config = ConfigDict(from_attributes=True)


