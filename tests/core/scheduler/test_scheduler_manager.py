"""Test cases for SchedulerManager."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone
from croniter import croniter

from automagik.core.flows import FlowManager
from automagik.core.scheduler import SchedulerManager
from automagik.core.database.models import Flow, Schedule


@pytest.fixture
async def scheduler_manager(session):
    """Create a scheduler manager for testing."""
    flow_manager = FlowManager(session)
    return SchedulerManager(session, flow_manager)


@pytest.fixture
async def sample_flow(session):
    """Create a sample flow for testing."""
    flow = Flow(
        id=uuid4(),
        name="Test Flow",
        description="Test Flow Description",
        input_component="input",
        output_component="output",
        source="test",
        source_id="test-flow",
        data={"test": "data"}
    )
    session.add(flow)
    await session.commit()
    return flow


@pytest.mark.asyncio
async def test_create_schedule_with_valid_interval(scheduler_manager, sample_flow):
    """Test creating a schedule with a valid interval."""
    schedule = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",  # 30 minutes
        flow_params={"input": "test"}
    )

    assert schedule is not None
    assert schedule.flow_id == sample_flow.id
    assert schedule.schedule_type == "interval"
    assert schedule.schedule_expr == "30m"
    assert schedule.flow_params == {"input": "test"}
    assert schedule.next_run_at is not None


@pytest.mark.asyncio
async def test_create_schedule_with_valid_cron(scheduler_manager, sample_flow):
    """Test creating a schedule with a valid cron expression."""
    cron_expr = "0 8 * * *"  # Every day at 8 AM
    schedule = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="cron",
        schedule_expr=cron_expr,
        flow_params={"input": "test"}
    )

    assert schedule is not None
    assert schedule.flow_id == sample_flow.id
    assert schedule.schedule_type == "cron"
    assert schedule.schedule_expr == cron_expr
    assert schedule.flow_params == {"input": "test"}
    
    # Verify next_run_at is calculated correctly
    # Note: We need to use a timezone-aware datetime for both values
    now = datetime.now(timezone.utc)
    cron = croniter(cron_expr, now)
    next_run = cron.get_next(datetime)
    expected_next_run = next_run.replace(tzinfo=timezone.utc)
    actual_next_run = schedule.next_run_at.replace(tzinfo=timezone.utc)
    assert abs((actual_next_run - expected_next_run).total_seconds()) < 5


@pytest.mark.asyncio
async def test_create_schedule_with_invalid_interval(scheduler_manager, sample_flow):
    """Test creating a schedule with an invalid interval."""
    schedule = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="invalid",
        flow_params={"input": "test"}
    )

    assert schedule is None


@pytest.mark.asyncio
async def test_create_schedule_with_invalid_cron(scheduler_manager, sample_flow):
    """Test creating a schedule with an invalid cron expression."""
    schedule = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="cron",
        schedule_expr="invalid",
        flow_params={"input": "test"}
    )

    assert schedule is None


@pytest.mark.asyncio
async def test_create_schedule_with_nonexistent_flow(scheduler_manager):
    """Test creating a schedule for a flow that doesn't exist."""
    schedule = await scheduler_manager.create_schedule(
        flow_id=uuid4(),
        schedule_type="interval",
        schedule_expr="30m",
        flow_params={"input": "test"}
    )

    assert schedule is None


@pytest.mark.asyncio
async def test_create_schedule_with_invalid_interval_formats(scheduler_manager, sample_flow):
    """Test creating schedules with various invalid interval formats."""
    invalid_intervals = [
        "30",       # Missing unit
        "1x",       # Invalid unit
        "0m",       # Zero value
        "-1m",      # Negative value
        "1.5m",     # Non-integer value
        "m",        # Missing value
        "",         # Empty string
        "1mm",      # Double unit
        "m1",       # Unit before value
        "one m",    # Non-numeric value
    ]
    
    for interval in invalid_intervals:
        schedule = await scheduler_manager.create_schedule(
            flow_id=sample_flow.id,
            schedule_type="interval",
            schedule_expr=interval,
            flow_params={"input": "test"}
        )
        assert schedule is None, f"Schedule with invalid interval '{interval}' should not be created"


@pytest.mark.asyncio
async def test_create_schedule_with_valid_interval_formats(scheduler_manager, sample_flow):
    """Test creating schedules with various valid interval formats."""
    valid_intervals = [
        "1m",    # 1 minute
        "30m",   # 30 minutes
        "1h",    # 1 hour
        "24h",   # 24 hours
        "1d",    # 1 day
        "7d",    # 7 days
    ]
    
    for interval in valid_intervals:
        schedule = await scheduler_manager.create_schedule(
            flow_id=sample_flow.id,
            schedule_type="interval",
            schedule_expr=interval,
            flow_params={"input": "test"}
        )
        assert schedule is not None, f"Schedule with valid interval '{interval}' should be created"
        assert schedule.schedule_expr == interval
        assert schedule.next_run_at is not None


@pytest.mark.asyncio
async def test_update_schedule_status(scheduler_manager, sample_flow):
    """Test updating schedule status."""
    # Create a schedule
    schedule = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",
        flow_params={"input": "test"}
    )
    assert schedule is not None
    assert schedule.status == "active"

    # Update status to paused
    result = await scheduler_manager.update_schedule_status(str(schedule.id), "pause")
    assert result is True

    # Verify status was updated
    updated_schedule = await scheduler_manager.get_schedule(schedule.id)
    assert updated_schedule is not None
    assert updated_schedule.status == "paused"

    # Resume schedule
    result = await scheduler_manager.update_schedule_status(str(schedule.id), "resume")
    assert result is True

    # Verify status was updated
    updated_schedule = await scheduler_manager.get_schedule(schedule.id)
    assert updated_schedule is not None
    assert updated_schedule.status == "active"


@pytest.mark.asyncio
async def test_update_schedule_status_invalid_action(scheduler_manager, sample_flow):
    """Test updating schedule status with invalid action."""
    # Create a schedule
    schedule = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",
        flow_params={"input": "test"}
    )

    assert schedule is not None

    # Try to update with invalid action
    result = await scheduler_manager.update_schedule_status(str(schedule.id), "invalid")
    assert result is False


@pytest.mark.asyncio
async def test_update_schedule_status_nonexistent_schedule(scheduler_manager):
    """Test updating status of a schedule that doesn't exist."""
    result = await scheduler_manager.update_schedule_status(str(uuid4()), "pause")
    assert result is False


@pytest.mark.asyncio
async def test_list_schedules(scheduler_manager, sample_flow):
    """Test listing schedules."""
    # Create some schedules
    schedule1 = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",
        flow_params={"input": "test1"}
    )
    schedule2 = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="cron",
        schedule_expr="0 8 * * *",
        flow_params={"input": "test2"}
    )

    # List schedules
    schedules = await scheduler_manager.list_schedules()
    assert len(schedules) >= 2

    # Verify the schedules we created are in the list
    schedule_ids = [str(s.id) for s in schedules]
    assert str(schedule1.id) in schedule_ids
    assert str(schedule2.id) in schedule_ids


@pytest.mark.asyncio
async def test_delete_schedule(scheduler_manager, sample_flow):
    """Test deleting a schedule."""
    # Create a schedule
    schedule = await scheduler_manager.create_schedule(
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",
        flow_params={"input": "test"}
    )

    assert schedule is not None

    # Delete the schedule
    result = await scheduler_manager.delete_schedule(schedule.id)
    assert result is True

    # Verify schedule was deleted
    deleted_schedule = await scheduler_manager.get_schedule(schedule.id)
    assert deleted_schedule is None


@pytest.mark.asyncio
async def test_delete_nonexistent_schedule(scheduler_manager):
    """Test deleting a schedule that doesn't exist."""
    result = await scheduler_manager.delete_schedule(uuid4())
    assert result is False
