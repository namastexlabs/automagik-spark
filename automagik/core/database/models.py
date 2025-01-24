"""
Database Models Module

This module defines all database models used in the application.
"""

from datetime import datetime
import uuid
from sqlalchemy import Column, String, JSON, DateTime, Integer, ForeignKey, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class FlowComponent(Base):
    """
    Represents a component within a flow, such as input/output nodes or processing steps.
    """
    __tablename__ = "flow_components"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(String, ForeignKey('flows.id'), nullable=False)
    component_id = Column(String, nullable=False)  # e.g., "CustomComponent-88JDQ"
    type = Column(String, nullable=False)  # e.g., "genericNode"
    template = Column(JSON)  # Component parameters
    tweakable_params = Column(JSON)  # List of parameters that can be tweaked
    is_input = Column(Boolean, default=False)
    is_output = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flow = relationship("FlowDB", back_populates="components")


class FlowDB(Base):
    """Flow model."""
    __tablename__ = 'flows'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    input_component = Column(String, nullable=False)
    output_component = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    schedules = relationship("Schedule", back_populates="flow", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="flow", cascade="all, delete-orphan")
    components = relationship("FlowComponent", back_populates="flow", cascade="all, delete-orphan")


class Schedule(Base):
    """Schedule model."""
    __tablename__ = 'schedules'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(String, ForeignKey('flows.id'), nullable=False)
    schedule_type = Column(String, nullable=False)  # interval, cron, oneshot
    schedule_expr = Column(String, nullable=False)  # e.g., "5m", "* * * * *", "2025-01-01T00:00:00"
    flow_params = Column(JSON)  # Optional parameters to pass to the flow
    status = Column(String, default='active')  # active, paused, completed
    next_run_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    flow = relationship("FlowDB", back_populates="schedules")


class Task(Base):
    """Task model."""
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(String, ForeignKey('flows.id'), nullable=False)
    status = Column(String, nullable=False)  # pending, running, completed, failed
    input_data = Column(JSON)
    result = Column(JSON)
    error = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    flow = relationship("FlowDB", back_populates="tasks")
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete-orphan")


class TaskLog(Base):
    """Task log model."""
    __tablename__ = 'logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
    level = Column(String, nullable=False)  # info, warning, error
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    task = relationship("Task", back_populates="logs")
