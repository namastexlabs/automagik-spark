from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from sqlalchemy import func
from datetime import datetime

Base = declarative_base()

class Flow(Base):
    """Flow model."""

    __tablename__ = "flows"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    folder_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    input_component = Column(String, nullable=False)
    output_component = Column(String, nullable=False)

    def __repr__(self):
        return f"<Flow {self.name}>"

class FlowComponent(Base):
    """Model representing a component in a flow."""
    
    __tablename__ = 'flow_components'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(String, ForeignKey('flows.id'), nullable=False)
    component_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    template = Column(JSON)
    tweakable_params = Column(JSON)
    is_input = Column(Boolean, default=False)
    is_output = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<FlowComponent(id='{self.id}', flow_id='{self.flow_id}', type='{self.type}')>"

class Task(Base):
    """Model representing a task execution of a flow."""
    
    __tablename__ = 'tasks'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(String, ForeignKey('flows.id'), nullable=False)
    status = Column(String, nullable=False)
    result = Column(JSON)
    error = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Task(id='{self.id}', flow_id='{self.flow_id}', status='{self.status}')>"

class Schedule(Base):
    """Model representing a scheduled execution of a flow."""
    
    __tablename__ = 'schedules'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(String, ForeignKey('flows.id'), nullable=False)
    cron_expression = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Schedule(id='{self.id}', flow_id='{self.flow_id}', cron='{self.cron_expression}')>"

class Log(Base):
    """Model representing a log entry for a task execution."""
    
    __tablename__ = 'logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Log(id='{self.id}', task_id='{self.task_id}', level='{self.level}')>"
