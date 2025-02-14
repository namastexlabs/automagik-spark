"""
Database models for the application.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from uuid import uuid4
import os
import base64
from cryptography.fernet import Fernet
import logging
from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UUID, func
from sqlalchemy.orm import relationship

from automagik.core.database.base import Base

logger = logging.getLogger(__name__)

def utcnow():
    """Return current UTC datetime with timezone."""
    return datetime.now(timezone.utc)


class Workflow(Base):
    """Workflow model."""
    __tablename__ = "workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    data = Column(JSON)  # Additional workflow data
    flow_raw_data = Column(JSON)  # Raw flow data from source
    
    # Source system info
    source = Column(String(50), nullable=False)  # e.g., "langflow"
    remote_flow_id = Column(String(255), nullable=False)  # ID of the remote flow (UUID)
    flow_version = Column(Integer, default=1)
    workflow_source_id = Column(UUID(as_uuid=True), ForeignKey("workflow_sources.id"))
    workflow_source = relationship("WorkflowSource", back_populates="workflows")
    
    # Component info
    input_component = Column(String(255))  # Component ID in source system
    output_component = Column(String(255))  # Component ID in source system
    is_component = Column(Boolean, default=False)
    
    # Metadata
    folder_id = Column(String(255))
    folder_name = Column(String(255))
    icon = Column(String(255))
    icon_bg_color = Column(String(50))
    gradient = Column(Boolean, default=False)
    liked = Column(Boolean, default=False)
    tags = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    tasks = relationship("Task", back_populates="workflow")
    schedules = relationship("Schedule", back_populates="workflow")
    components = relationship("WorkflowComponent", back_populates="workflow")

    def __str__(self):
        """Return a string representation of the workflow."""
        return f"{self.name} ({self.id})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'data': self.data,
            'flow_raw_data': self.flow_raw_data,
            'source': self.source,
            'remote_flow_id': self.remote_flow_id,
            'flow_version': self.flow_version,
            'input_component': self.input_component,
            'output_component': self.output_component,
            'is_component': self.is_component,
            'folder_id': self.folder_id,
            'folder_name': self.folder_name,
            'icon': self.icon,
            'icon_bg_color': self.icon_bg_color,
            'gradient': self.gradient,
            'liked': self.liked,
            'tags': self.tags,
            'workflow_source_id': str(self.workflow_source_id) if self.workflow_source_id else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'schedules': [s.to_dict() for s in self.schedules] if self.schedules else []
        }


class WorkflowSource(Base):
    """Workflow source model."""
    __tablename__ = "workflow_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    source_type = Column(String(50), nullable=False)  # e.g., "langflow"
    url = Column(String(255), nullable=False, unique=True)
    encrypted_api_key = Column(String, nullable=False)
    version_info = Column(JSON)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    workflows = relationship("Workflow", back_populates="workflow_source")

    @staticmethod
    def _get_encryption_key():
        """Get encryption key from environment or generate a default one."""
        key = os.environ.get('AUTOMAGIK_ENCRYPTION_KEY')
        
        if not key:
            # Log a warning that we're using a testing key
            logger.warning("No AUTOMAGIK_ENCRYPTION_KEY found in environment, using testing key. This is unsafe for production!")
            # Use a fixed testing key that's URL-safe base64 encoded
            return b'S1JwNXY2Z1hrY1NhcUxXR3VZM3pNMHh3cU1mWWVEejVQYk09'
            
        # Key is provided in environment
        try:
            # First try to decode as URL-safe base64
            decoded = base64.urlsafe_b64decode(key.encode())
            if len(decoded) == 32:
                return key.encode()
        except Exception:
            pass
            
        try:
            # If not base64, try to encode the raw key
            if len(key.encode()) == 32:
                return base64.urlsafe_b64encode(key.encode())
            elif len(key) == 44:  # Standard base64 encoded length for 32 bytes
                return key.encode()
        except Exception as e:
            logger.error(f"Invalid encryption key format: {str(e)}")
            raise ValueError("Invalid encryption key format. Key must be either 32 bytes of raw data or base64 encoded.")

    @staticmethod
    def encrypt_api_key(api_key: str) -> str:
        """Encrypt an API key."""
        key = WorkflowSource._get_encryption_key()
        f = Fernet(key)
        return f.encrypt(api_key.encode()).decode()

    @staticmethod
    def decrypt_api_key(encrypted_key: str) -> str:
        """Decrypt an API key."""
        key = WorkflowSource._get_encryption_key()
        f = Fernet(key)
        return f.decrypt(encrypted_key.encode()).decode()

    def __str__(self):
        """Return a string representation of the source."""
        return f"{self.source_type} source at {self.url}"

    def __init__(self, **kwargs):
        """Initialize a workflow source."""
        # Ensure URL doesn't end with /
        if 'url' in kwargs:
            kwargs['url'] = kwargs['url'].rstrip('/')
        super().__init__(**kwargs)


class WorkflowComponent(Base):
    """Workflow component model."""
    __tablename__ = "workflow_components"

    id = Column(UUID(as_uuid=True), primary_key=True)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"), nullable=False)
    
    # Component info
    component_id = Column(String(255), nullable=False)  # ID in source system (e.g., "ChatOutput-WHzRB")
    type = Column(String(50), nullable=False)
    template = Column(JSON)  # Component template/configuration
    tweakable_params = Column(JSON)  # Parameters that can be modified
    
    # Input/Output flags
    is_input = Column(Boolean, default=False)
    is_output = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    workflow = relationship("Workflow", back_populates="components")


class Task(Base):
    """Task model."""
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('workflows.id'), nullable=False)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey('schedules.id'), nullable=True)
    status = Column(String, nullable=False, default='pending')
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    tries = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=3)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    workflow = relationship("Workflow", back_populates="tasks")
    logs = relationship("TaskLog", back_populates="task", order_by="TaskLog.created_at")
    schedule = relationship("Schedule", back_populates="tasks")

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        # Don't try to access relationships if we're detached
        return {
            'id': str(self.id),
            'workflow_id': str(self.workflow_id),
            'schedule_id': str(self.schedule_id) if self.schedule_id else None,
            'status': self.status,
            'input_data': self.input_data,
            'output_data': self.output_data,
            'error': self.error,
            'next_retry_at': self.next_retry_at.isoformat() if self.next_retry_at else None,
            'tries': self.tries,
            'max_retries': self.max_retries,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TaskLog(Base):
    """Task log entry."""

    __tablename__ = "task_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)
    component_id = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    task = relationship("Task", back_populates="logs")


class Schedule(Base):
    """Schedule model."""
    __tablename__ = 'schedules'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('workflows.id'), nullable=False)
    schedule_type = Column(String, nullable=False)
    schedule_expr = Column(String, nullable=False)
    workflow_params = Column(String, nullable=True)
    params = Column(JSON, nullable=True)
    status = Column(String, nullable=False, default="active")
    next_run_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    input_data = Column(String, nullable=True)

    # Relationships
    workflow = relationship("Workflow", back_populates="schedules")
    tasks = relationship("Task", back_populates="schedule")

    def to_dict(self) -> Dict[str, Any]:
        """Convert schedule to dictionary."""
        return {
            'id': str(self.id),
            'workflow_id': str(self.workflow_id),
            'schedule_type': self.schedule_type,
            'schedule_expr': self.schedule_expr,
            'workflow_params': self.workflow_params,
            'params': self.params,
            'status': self.status,
            'next_run_at': self.next_run_at.isoformat() if self.next_run_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'input_data': self.input_data
        }


class Worker(Base):
    """Worker model."""
    __tablename__ = "workers"

    id = Column(UUID(as_uuid=True), primary_key=True)
    hostname = Column(String(255), nullable=False)
    pid = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="active")  # active, paused, stopped
    current_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    stats = Column(JSON)  # Worker statistics
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    last_heartbeat = Column(DateTime(timezone=True))

    # Relationships
    current_task = relationship("Task")
