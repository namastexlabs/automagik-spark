"""Pydantic models for workflow sources."""

from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, HttpUrl, ConfigDict

class SourceType(str, Enum):
    """Enum for workflow source types."""
    LANGFLOW = "langflow"
    AUTOMAGIK_AGENTS = "automagik-agents"

class WorkflowSourceBase(BaseModel):
    """Base model for workflow sources."""
    name: Optional[str] = None
    source_type: SourceType
    url: HttpUrl

class WorkflowSourceCreate(WorkflowSourceBase):
    """Model for creating a workflow source."""
    api_key: str = ""  # Allow empty string by default

class WorkflowSourceUpdate(BaseModel):
    """Model for updating a workflow source."""
    name: Optional[str] = None
    source_type: Optional[SourceType] = None
    url: Optional[HttpUrl] = None
    api_key: Optional[str] = None
    status: Optional[str] = None

class WorkflowSourceResponse(WorkflowSourceBase):
    """Model for workflow source responses."""
    id: UUID
    status: str
    version_info: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
