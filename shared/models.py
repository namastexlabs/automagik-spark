from sqlalchemy import Column, String, JSON, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class FlowDB(Base):
    __tablename__ = "flows"
    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    data = Column(JSON)
    source = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    flow_version = Column(Integer, default=1)
    user_id = Column(String)
    folder_id = Column(String)
    is_component = Column(Boolean, default=False)
    icon = Column(String)
    icon_bg_color = Column(String)
    gradient = Column(String)
    liked = Column(Boolean, default=False)
    tags = Column(JSON)
    folder_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationship to agents
    agents = relationship("Agent", back_populates="flow")

class Agent(Base):
    __tablename__ = "agents"
    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    flow_id = Column(UUID, ForeignKey('flows.id'), nullable=False)
    input_component = Column(String, nullable=False)
    output_component = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Add relationships
    flow = relationship("FlowDB", back_populates="agents")
    schedules = relationship("Schedule", back_populates="agent")

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(UUID, primary_key=True)
    agent_id = Column(UUID, ForeignKey('agents.id'), nullable=False)
    schedule_type = Column(String, nullable=False)  # 'interval' or 'cron'
    schedule_expr = Column(String, nullable=False)
    status = Column(String, default='active')  # 'active' or 'paused'
    next_run_at = Column(DateTime)
    last_run_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationship
    agent = relationship("Agent", back_populates="schedules") 