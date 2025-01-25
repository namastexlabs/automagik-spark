"""
Flow Manager Module

Provides the main interface for managing flows, combining functionality
from flow_analyzer and flow_sync.
"""

import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
from dateutil import tz

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .analyzer import FlowAnalyzer
from .sync import FlowSync
from ..database.models import Flow, FlowComponent, Schedule, Task

logger = logging.getLogger(__name__)

class FlowManager:
    """Flow manager class for handling LangFlow integration and scheduling."""
    
    def __init__(self, session: AsyncSession, langflow_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize FlowManager.
        
        Args:
            session: SQLAlchemy async session
            langflow_url: Optional LangFlow API URL (defaults to env var)
            api_key: Optional API key (defaults to env var)
        """
        self.session = session
        self.langflow_url = langflow_url or os.getenv("LANGFLOW_API_URL")
        api_key = api_key or os.getenv("LANGFLOW_API_KEY")
        
        if not self.langflow_url:
            raise ValueError("LangFlow API URL not provided")
            
        self.flow_sync = FlowSync(self.langflow_url, api_key)
        self.analyzer = FlowAnalyzer()
        
    async def list_remote_flows(self, include_examples: bool = False) -> List[Dict[str, Any]]:
        """
        List all available flows from LangFlow.
        
        Args:
            include_examples: Whether to include example flows
            
        Returns:
            List of flow dictionaries
        """
        return await self.flow_sync.get_remote_flows(remove_examples=not include_examples)
        
    async def list_flows(self) -> List[Flow]:
        """
        List all flows from the local database.
        
        Returns:
            List of Flow objects
        """
        result = await self.session.execute(
            select(Flow)
            .options(selectinload(Flow.schedules))
            .order_by(Flow.name)
        )
        return list(result.scalars().all())
        
    async def get_flow_components(self, flow_id: str) -> List[Dict[str, Any]]:
        """
        Get components from a specific flow.
        
        Args:
            flow_id: ID of the flow to analyze
            
        Returns:
            List of components with their details
        """
        flow_data = await self.flow_sync.get_flow_data(flow_id)
        if not flow_data:
            return []
            
        return self.analyzer.get_flow_components(flow_data)
        
    async def sync_flow(
        self,
        flow_id: str,
        input_component: str,
        output_component: str
    ) -> Optional[uuid.UUID]:
        """
        Sync a flow from LangFlow to local database.
        
        Args:
            flow_id: ID of the flow to sync
            input_component: ID of the input component
            output_component: ID of the output component
            
        Returns:
            UUID of the synced flow or None if failed
        """
        try:
            # Get flow data
            flow_data = await self.flow_sync.get_flow_data(flow_id)
            if not flow_data:
                return None
                
            # Create or update flow
            flow = Flow(
                id=uuid.uuid4(),
                name=flow_data["name"],
                data=flow_data,
                created_at=datetime.utcnow()
            )
            
            # Get components
            components = []
            for node in flow_data.get("data", {}).get("nodes", []):
                params = self.analyzer.analyze_component(node)
                component = FlowComponent(
                    id=uuid.uuid4(),
                    flow_id=flow.id,
                    component_id=node["id"],
                    type=node.get("type", "unknown"),
                    template=node.get("data", {}).get("node", {}).get("template"),
                    tweakable_params=params,
                    is_input=node["id"] == input_component,
                    is_output=node["id"] == output_component
                )
                components.append(component)
            
            # Save to database
            self.session.add(flow)
            for component in components:
                self.session.add(component)
            await self.session.commit()
            
            return flow.id
            
        except Exception as e:
            logger.error(f"Error syncing flow {flow_id}: {str(e)}")
            await self.session.rollback()
            return None
            
    async def list_schedules(self) -> List[Schedule]:
        """
        List all schedules from database.
        
        Returns:
            List of Schedule objects
        """
        result = await self.session.execute(
            select(Schedule)
            .options(selectinload(Schedule.flow))
            .order_by(Schedule.created_at)
        )
        return list(result.scalars().all())
        
    async def create_schedule(
        self,
        flow_id: str,
        schedule_type: str,
        schedule_expr: str,
        flow_params: Optional[Dict[str, str]] = None
    ) -> Optional[Schedule]:
        """
        Create a new schedule for a flow.
        
        Args:
            flow_id: ID of the flow to schedule
            schedule_type: Type of schedule (cron/interval)
            schedule_expr: Schedule expression
            flow_params: Optional parameters for the flow
            
        Returns:
            Created Schedule object or None if failed
        """
        try:
            # Get flow
            result = await self.session.execute(select(Flow).where(Flow.id == flow_id))
            flow = result.scalar_one_or_none()
            if not flow:
                logger.error(f"Flow {flow_id} not found")
                return None
            
            # Create schedule
            now = datetime.now(tz=tz.tzutc())
            next_run = now + timedelta(minutes=1)  # Start in 1 minute
            
            schedule = Schedule(
                id=uuid.uuid4(),
                flow_id=flow_id,
                schedule_type=schedule_type,
                schedule_expr=schedule_expr,
                flow_params={'input_value': flow_params.get('input_value', '')} if flow_params else {},
                status='active',
                created_at=now,
                next_run_at=next_run
            )
            
            self.session.add(schedule)
            await self.session.commit()
            await self.session.refresh(schedule)
            
            return schedule
            
        except Exception as e:
            logger.error(f"Error creating schedule: {str(e)}")
            await self.session.rollback()
            return None
            
    async def update_schedule_status(self, schedule_id: str, action: str) -> bool:
        """
        Update schedule status.
        
        Args:
            schedule_id: ID of schedule to update
            action: Action to perform (pause/resume/stop)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            status_map = {
                'pause': 'paused',
                'resume': 'active',
                'stop': 'stopped'
            }
            
            new_status = status_map.get(action)
            if not new_status:
                logger.error(f"Invalid action: {action}")
                return False
            
            result = await self.session.execute(
                update(Schedule)
                .where(Schedule.id == schedule_id)
                .values(status=new_status)
            )
            
            if result.rowcount == 0:
                logger.error(f"Schedule {schedule_id} not found")
                return False
            
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating schedule status: {str(e)}")
            await self.session.rollback()
            return False
            
    async def update_schedule_next_run(self, schedule_id: str, next_run: datetime) -> bool:
        """
        Update schedule next run time.
        
        Args:
            schedule_id: ID of schedule to update
            next_run: Next run time
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self.session.execute(
                select(Schedule)
                .where(Schedule.id == schedule_id)
            )
            schedule = result.scalar_one_or_none()
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return False
            
            # Ensure next_run is timezone-aware
            if next_run.tzinfo is None:
                next_run = next_run.replace(tzinfo=tz.tzutc())
            
            schedule.next_run_at = next_run
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating schedule next run: {str(e)}")
            await self.session.rollback()
            return False
            
    async def list_tasks(
        self,
        flow_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """
        List tasks from database.
        
        Args:
            flow_id: Optional flow ID to filter by
            status: Optional status to filter by
            limit: Maximum number of tasks to return
            
        Returns:
            List of Task objects
        """
        query = select(Task).options(
            selectinload(Task.flow)
        ).order_by(Task.created_at.desc())
        
        if flow_id:
            query = query.where(Task.flow_id == flow_id)
        if status:
            query = query.where(Task.status == status)
            
        query = query.limit(limit)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
        
    async def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: ID of task to get
            
        Returns:
            Task object if found, None otherwise
        """
        result = await self.session.execute(
            select(Task)
            .options(
                selectinload(Task.flow)
            )
            .where(Task.id == task_id)
        )
        return result.scalar_one_or_none()
        
    async def retry_task(self, task_id: str) -> Optional[Task]:
        """
        Retry a failed task.
        
        Args:
            task_id: ID of task to retry
            
        Returns:
            New Task object if successful, None otherwise
        """
        try:
            # Get original task
            original_task = await self.get_task(task_id)
            if not original_task:
                logger.error(f"Task {task_id} not found")
                return None
                
            if original_task.status != 'failed':
                logger.error(f"Can only retry failed tasks")
                return None
                
            # Create new task
            new_task = Task(
                id=uuid.uuid4(),
                flow_id=original_task.flow_id,
                schedule_id=original_task.schedule_id,
                status='pending',
                input_data=original_task.input_data,
                created_at=datetime.utcnow(),
                max_retries=original_task.max_retries,
                tries=0  # Reset tries count for the new task
            )
            
            self.session.add(new_task)
            await self.session.commit()
            await self.session.refresh(new_task)
            
            return new_task
            
        except Exception as e:
            logger.error(f"Error retrying task: {str(e)}")
            await self.session.rollback()
            return None

    async def get_flow(self, flow_id: str) -> Optional[Flow]:
        """Get a flow by ID."""
        try:
            flow = await self.session.get(Flow, flow_id)
            return flow
        except Exception as e:
            logger.error(f"Failed to get flow: {str(e)}")
            return None

    async def run_flow(self, flow_id: str, flow_params: dict = None) -> Optional[dict]:
        """Run a flow with given parameters."""
        try:
            # Get flow
            flow = await self.get_flow(flow_id)
            if not flow:
                logger.error(f"Flow {flow_id} not found")
                return None
            
            # Execute flow
            result = await self.flow_sync.execute_flow(flow.id, flow_params or {})
            if not result:
                return None
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to run flow: {str(e)}")
            return None
