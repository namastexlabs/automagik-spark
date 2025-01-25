"""Local flow management module."""

import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database.models import Flow

logger = logging.getLogger(__name__)

class LocalFlowManager:
    """Local flow management class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize local flow manager."""
        self.session = session

    async def get_flow(self, flow_id: str) -> Optional[Flow]:
        """Get a flow by ID or source_id."""
        try:
            # Try getting by ID first
            flow = await self.session.get(Flow, flow_id)
            if flow:
                return flow
                
            # If not found, try by source_id
            result = await self.session.execute(
                select(Flow).where(Flow.source_id == flow_id)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get flow: {str(e)}")
            return None

    async def list_flows(self) -> List[Flow]:
        """List all flows from the local database."""
        result = await self.session.execute(
            select(Flow)
            .options(joinedload(Flow.schedules))
            .order_by(Flow.name)
        )
        return list(result.scalars().unique().all())

    async def delete_flow(self, flow_id: str) -> bool:
        """Delete a flow from local database."""
        try:
            # Try exact match first (for full UUID)
            try:
                uuid_obj = UUID(flow_id)
                exact_match = True
            except ValueError:
                exact_match = False
            
            # Build query based on match type
            query = select(Flow).options(
                joinedload(Flow.components),
                joinedload(Flow.schedules),
                joinedload(Flow.tasks)
            )
            
            if exact_match:
                query = query.where(Flow.id == uuid_obj)
            else:
                query = query.where(cast(Flow.id, String).like(f"{flow_id}%"))
            
            # Execute query
            result = await self.session.execute(query)
            flow = result.unique().scalar_one_or_none()
            
            if not flow:
                logger.error(f"Flow {flow_id} not found in local database")
                return False
            
            # Delete all related objects first
            for component in flow.components:
                await self.session.delete(component)
            for schedule in flow.schedules:
                await self.session.delete(schedule)
            for task in flow.tasks:
                await self.session.delete(task)
            
            # Now delete the flow
            await self.session.delete(flow)
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting flow: {e}")
            await self.session.rollback()
            return False
