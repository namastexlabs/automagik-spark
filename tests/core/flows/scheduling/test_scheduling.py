"""Tests for flow scheduling functionality."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone

from automagik.core.workflows import WorkflowManager
from automagik.core.scheduler import SchedulerManager
from automagik.core.database.models import Workflow, Schedule

@pytest.fixture
def flow_manager(session):
    """Create a WorkflowManager instance."""
    return WorkflowManager(session)

@pytest.fixture
async def scheduler_manager(flow_manager: WorkflowManager):
    """Create a scheduler manager for testing."""
    return SchedulerManager(flow_manager.session, flow_manager)

@pytest.fixture
async def sample_flow(session):
    """Create a sample flow in the database."""
    flow = Workflow(
        id=uuid4(),
        name="Test Flow",
        description="A test flow",
        data={"nodes": []},
        source="test",
        remote_flow_id="test_id",
        flow_version=1,
        input_component="input-1",
        output_component="output-1"
    )
    session.add(flow)
    await session.commit()
    await session.refresh(flow)
    return flow

@pytest.mark.asyncio
async def test_create_schedule(scheduler_manager, sample_flow):
    """Test creating a schedule for a flow."""
    schedule = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="cron",
        schedule_expr="0 0 * * *",
        flow_params={"input": "test"}
    )
    
    assert schedule is not None
    assert schedule.flow_id == sample_flow.id
    assert schedule.schedule_type == "cron"
    assert schedule.schedule_expr == "0 0 * * *"
    assert schedule.flow_params == {"input": "test"}

@pytest.mark.asyncio
async def test_delete_schedule(scheduler_manager, sample_flow):
    """Test deleting a schedule."""
    # Create a schedule first
    schedule = Schedule(
        id=uuid4(),
        flow_id=sample_flow.id,
        schedule_type="cron",
        schedule_expr="0 0 * * *",
        flow_params={"input": "test"}
    )
    scheduler_manager.session.add(schedule)
    await scheduler_manager.session.commit()
    
    # Now delete it
    result = await scheduler_manager.delete_schedule(schedule.id)
    assert result is True
    
    # Verify it's gone
    result = await scheduler_manager.get_schedule(schedule.id)
    assert result is None

@pytest.mark.asyncio
async def test_delete_nonexistent_schedule(scheduler_manager):
    """Test deleting a schedule that doesn't exist."""
    result = await scheduler_manager.delete_schedule(uuid4())
    assert result is False
