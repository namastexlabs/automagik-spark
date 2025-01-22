from fastapi import Depends
from sqlalchemy.orm import Session
import os

from core.database import get_db_session
from core.flows import FlowManager
from core.scheduler import SchedulerService

def get_flow_manager(db: Session = Depends(get_db_session)):
    """Dependency for FlowManager"""
    api_url = os.getenv('LANGFLOW_API_URL')
    api_key = os.getenv('LANGFLOW_API_KEY')
    return FlowManager(db, api_url, api_key)

def get_scheduler(db: Session = Depends(get_db_session)):
    """Dependency for SchedulerService"""
    return SchedulerService(db)
