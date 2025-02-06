"""Pydantic models for workflow sources."""

from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl, constr, ConfigDict

class WorkflowSourceBase(BaseModel):
    """Base model for workflow sources."""
    source_type: constr(strip_whitespace=True, min_length=1)
    url: HttpUrl
    status: Optional[str] = "active"

class WorkflowSourceCreate(WorkflowSourceBase):
    """Model for creating a workflow source."""
    api_key: str

class WorkflowSourceUpdate(BaseModel):
    """Model for updating a workflow source."""
    source_type: Optional[str] = None
    url: Optional[HttpUrl] = None
    api_key: Optional[str] = None
    status: Optional[str] = None

class WorkflowSourceResponse(WorkflowSourceBase):
    """Model for workflow source responses."""
    id: UUID
    version_info: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
