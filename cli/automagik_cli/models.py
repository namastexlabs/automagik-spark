from datetime import datetime
import uuid
import os
from sqlalchemy import Column, String, JSON, DateTime, Integer, ForeignKey, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from .shared.base import Base

def get_db_session():
    """Get a database session"""
    db_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(db_dir, 'automagik.db')
    
    # Ensure database directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Create database URL with absolute path
    db_url = f'sqlite:///{os.path.abspath(db_path)}'
    
    # Create engine with echo for debugging
    engine = create_engine(db_url, echo=os.getenv('AUTOMAGIK_DEBUG') == '1')
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    return Session()

class FlowComponent(Base):
    __tablename__ = "flow_components"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    component_id = Column(String, nullable=False)  # e.g., "CustomComponent-88JDQ"
    type = Column(String, nullable=False)  # e.g., "genericNode"
    template = Column(JSON)  # Component parameters
    tweakable_params = Column(ARRAY(String))  # List of parameters that can be tweaked
    is_input = Column(Boolean, default=False)
    is_output = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    flow = relationship("FlowDB", back_populates="components")

class FlowDB(Base):
    __tablename__ = "flows"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    data = Column(JSON)
    source = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    flow_version = Column(Integer, default=1)
    input_component = Column(String)  # ID of the input component
    output_component = Column(String)  # ID of the output component
    is_component = Column(Boolean, default=False)
    folder_id = Column(String)  # ID of the folder in Langflow
    folder_name = Column(String)  # Name of the folder in Langflow
    icon = Column(String)
    icon_bg_color = Column(String)
    gradient = Column(String)
    liked = Column(Boolean, default=False)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    components = relationship("FlowComponent", back_populates="flow", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="flow", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="flow", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    status = Column(String, nullable=False, default='pending')
    input_data = Column(JSON, default={})
    output_data = Column(JSON, default={})
    tries = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    flow = relationship("FlowDB", back_populates="tasks")
    logs = relationship("Log", back_populates="task", cascade="all, delete-orphan")

class Log(Base):
    __tablename__ = "logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    task = relationship("Task", back_populates="logs")

class Schedule(Base):
    __tablename__ = "schedules"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    schedule_type = Column(String, nullable=False)  # 'interval' or 'cron'
    schedule_expr = Column(String, nullable=False)  # '30m' for interval, '0 * * * *' for cron
    flow_params = Column(JSON, default={})  # Parameters to pass to the flow
    status = Column(String, default='active')
    next_run_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    flow = relationship("FlowDB", back_populates="schedules")