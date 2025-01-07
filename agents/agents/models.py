from sqlalchemy import Column, String, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from shared.base import Base
from sqlalchemy.orm import relationship

class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    flow_id = Column(UUID, ForeignKey('flows.id'), nullable=False)
    input_component = Column(String, nullable=False)  # Component ID that receives input
    output_component = Column(String, nullable=False)  # Component ID that produces output
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationship to schedules
    schedules = relationship("Schedule", back_populates="agent", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Agent(id='{self.id}', name='{self.name}', flow_id='{self.flow_id}')>"
