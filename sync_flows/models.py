from sqlalchemy import Column, String, JSON, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from shared.base import Base

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

    def __repr__(self):
        return f"<FlowDB(id='{self.id}', name='{self.name}')>"
