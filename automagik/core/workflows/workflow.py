"""
Local workflow management module.

Provides functionality for managing workflows in the local database.
"""

import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database.models import Workflow

logger = logging.getLogger(__name__)

class LocalWorkflowManager:
    """Local workflow management class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize local workflow manager."""
        self.session = session

    async def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID or source_id."""
        try:
            # Try getting by ID first
            workflow = await self.session.get(Workflow, workflow_id)
            if workflow:
                return workflow
                
            # If not found, try by source_id
            result = await self.session.execute(
                select(Workflow).where(Workflow.source_id == workflow_id)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get workflow: {str(e)}")
            return None

    async def list_workflows(self) -> List[Workflow]:
        """List all workflows from the local database."""
        result = await self.session.execute(
            select(Workflow)
            .options(joinedload(Workflow.schedules))
            .order_by(Workflow.name)
        )
        return list(result.scalars().unique().all())

    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow from local database."""
        try:
            # Try exact match first (for full UUID)
            try:
                uuid_obj = UUID(workflow_id)
                exact_match = True
            except ValueError:
                exact_match = False
            
            # Build query based on match type
            query = select(Workflow).options(
                joinedload(Workflow.components),
                joinedload(Workflow.schedules),
                joinedload(Workflow.tasks)
            )
            
            if exact_match:
                query = query.where(Workflow.id == uuid_obj)
            else:
                query = query.where(cast(Workflow.id, String).like(f"{workflow_id}%"))
            
            # Execute query
            result = await self.session.execute(query)
            workflow = result.unique().scalar_one_or_none()
            
            if not workflow:
                logger.error(f"Workflow {workflow_id} not found in local database")
                return False
            
            # Delete all related objects first
            for component in workflow.components:
                await self.session.delete(component)
            for schedule in workflow.schedules:
                await self.session.delete(schedule)
            for task in workflow.tasks:
                await self.session.delete(task)
            
            # Now delete the workflow
            await self.session.delete(workflow)
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting workflow: {e}")
            await self.session.rollback()
            return False
