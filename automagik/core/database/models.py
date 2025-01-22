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
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
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
    """
    Represents a flow, which is a collection of components and their connections.
    """
    __tablename__ = "flows"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    data = Column(JSON)  # Full flow data including connections
    source = Column(String, nullable=False)  # e.g., 'langflow'
    source_id = Column(String, nullable=False)  # Original ID in the source system
    flow_version = Column(Integer, default=1)
    input_component = Column(String)  # ID of the input component
    output_component = Column(String)  # ID of the output component
    is_component = Column(Boolean, default=False)
    folder_id = Column(String)  # ID of the folder in source system
    folder_name = Column(String)  # Name of the folder in source system
    icon = Column(String)
    icon_bg_color = Column(String)
    gradient = Column(String)
    liked = Column(Boolean, default=False)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    components = relationship("FlowComponent", back_populates="flow", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="flow", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="flow", cascade="all, delete-orphan")


class Task(Base):
    """
    Represents a task, which is an execution instance of a flow.
    """
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    status = Column(String, nullable=False, default='pending')  # pending, running, completed, failed
    input_data = Column(JSON, default={})
    output_data = Column(JSON, default={})
    tries = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flow = relationship("FlowDB", back_populates="tasks")
    logs = relationship("Log", back_populates="task", cascade="all, delete-orphan")


class Log(Base):
    """
    Represents a log entry associated with a task execution.
    """
    __tablename__ = "logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
    level = Column(String, nullable=False)  # debug, info, warning, error
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    task = relationship("Task", back_populates="logs")


class Schedule(Base):
    """
    Represents a schedule for automated flow execution.
    """
    __tablename__ = "schedules"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    schedule_type = Column(String, nullable=False)  # 'interval' or 'cron'
    schedule_expr = Column(String, nullable=False)  # '30m' for interval, '0 * * * *' for cron
    flow_params = Column(JSON, default={})  # Parameters to pass to the flow
    status = Column(String, default='active')  # active, paused, deleted
    next_run_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flow = relationship("FlowDB", back_populates="schedules")
