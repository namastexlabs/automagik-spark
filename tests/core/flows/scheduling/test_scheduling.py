"""Tests for flow scheduling functionality."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone

from automagik.core.flows.manager import FlowManager
from automagik.core.database.models import Flow, Schedule

@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return FlowManager(session)

@pytest.fixture
async def sample_flow(session):
    """Create a sample flow in the database."""
    flow = Flow(
        id=uuid4(),
        name="Test Flow",
        description="A test flow",
        data={"nodes": []},
        source="langflow",
        source_id="test-flow-1",
        flow_version=1,
        input_component="input-1",
        output_component="output-1"
    )
    session.add(flow)
    await session.commit()
    await session.refresh(flow)
    return flow

@pytest.mark.asyncio
async def test_create_schedule(flow_manager, sample_flow):
    """Test creating a schedule for a flow."""
    schedule = await flow_manager.create_schedule(
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
async def test_delete_schedule(flow_manager, sample_flow):
    """Test deleting a schedule."""
    # Create a schedule first
    schedule = Schedule(
        id=uuid4(),
        flow_id=sample_flow.id,
        schedule_type="cron",
        schedule_expr="0 0 * * *",
        flow_params={"input": "test"}
    )
    flow_manager.session.add(schedule)
    await flow_manager.session.commit()
    
    # Now delete it
    result = await flow_manager.delete_schedule(schedule.id)
    assert result is True
    
    # Verify it's gone
    deleted_schedule = await flow_manager.get_schedule(schedule.id)
    assert deleted_schedule is None

@pytest.mark.asyncio
async def test_delete_nonexistent_schedule(flow_manager):
    """Test deleting a schedule that doesn't exist."""
    result = await flow_manager.delete_schedule(uuid4())
    assert result is False
