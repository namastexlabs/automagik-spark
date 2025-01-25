"""Test cases for worker command."""

import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from sqlalchemy import text, select, func
from sqlalchemy.orm import selectinload

from automagik.cli.commands.worker import process_schedules, parse_interval
from automagik.core.database.models import Flow, Schedule, Task, TaskLog

@pytest.fixture(autouse=True)
async def cleanup_db(session):
    """Clean up database before each test."""
    await session.execute(text("DELETE FROM task_logs"))
    await session.execute(text("DELETE FROM tasks"))
    await session.execute(text("DELETE FROM schedules"))
    await session.execute(text("DELETE FROM flow_components"))
    await session.execute(text("DELETE FROM flows"))
    await session.commit()

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

@pytest.fixture
async def future_schedule(session, sample_flow):
    """Create a schedule that will run in the future."""
    next_run = datetime.now(timezone.utc) + timedelta(hours=1)
    schedule = Schedule(
        id=uuid4(),
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="60m",  # 60 minutes
        flow_params={"test": "params"},
        status="active",
        next_run_at=next_run
    )
    session.add(schedule)
    await session.commit()
    return schedule

@pytest.fixture
async def past_schedule(session, sample_flow):
    """Create a schedule that was due in the past."""
    next_run = datetime.now(timezone.utc) - timedelta(minutes=5)
    schedule = Schedule(
        id=uuid4(),
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",  # 30 minutes
        flow_params={"test": "params"},
        status="active",
        next_run_at=next_run
    )
    session.add(schedule)
    await session.commit()
    return schedule

@pytest.fixture
async def inactive_schedule(session, sample_flow):
    """Create an inactive schedule."""
    next_run = datetime.now(timezone.utc) - timedelta(minutes=5)
    schedule = Schedule(
        id=uuid4(),
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",
        flow_params={"test": "params"},
        status="paused",  
        next_run_at=next_run
    )
    session.add(schedule)
    await session.commit()
    return schedule

@pytest.mark.asyncio
async def test_process_schedules_future(session, future_schedule):
    """Test processing a schedule that will run in the future."""
    await process_schedules(session)
    
    # Verify no tasks were created
    result = await session.execute(select(func.count()).select_from(Task))
    count = result.scalar()
    assert count == 0
    
    # Verify next run time wasn't changed
    await session.refresh(future_schedule)
    next_run = future_schedule.next_run_at.replace(tzinfo=timezone.utc)
    time_until = next_run - datetime.now(timezone.utc)
    assert 3500 < time_until.total_seconds() < 3700  # roughly 1 hour

@pytest.mark.asyncio
async def test_process_schedules_past(session, past_schedule):
    """Test processing a schedule that was due in the past."""
    old_next_run = past_schedule.next_run_at.replace(tzinfo=timezone.utc)
    await process_schedules(session)
    
    # Verify task was created
    result = await session.execute(select(func.count()).select_from(Task))
    count = result.scalar()
    assert count == 1
    
    # Verify next run time was updated
    await session.refresh(past_schedule)
    next_run = past_schedule.next_run_at.replace(tzinfo=timezone.utc)
    # Next run should be 30 minutes after now, not after old_next_run
    time_until_next = (next_run - datetime.now(timezone.utc)).total_seconds()
    assert 1700 < time_until_next < 1900  # roughly 30 minutes

@pytest.mark.asyncio
async def test_process_schedules_inactive(session, inactive_schedule):
    """Test processing an inactive schedule."""
    old_next_run = inactive_schedule.next_run_at.replace(tzinfo=timezone.utc)
    await process_schedules(session)
    
    # Verify no tasks were created
    result = await session.execute(select(func.count()).select_from(Task))
    count = result.scalar()
    assert count == 0
    
    # Verify next run time wasn't changed
    await session.refresh(inactive_schedule)
    next_run = inactive_schedule.next_run_at.replace(tzinfo=timezone.utc)
    assert next_run == old_next_run

@pytest.mark.asyncio
async def test_process_schedules_multiple(session, future_schedule, past_schedule, inactive_schedule):
    """Test processing multiple schedules."""
    await process_schedules(session)
    
    # Verify only one task was created (for past_schedule)
    result = await session.execute(select(func.count()).select_from(Task))
    count = result.scalar()
    assert count == 1
    
    # Verify task was created for the right flow
    result = await session.execute(
        select(Task.flow_id)
        .order_by(Task.created_at.desc())
        .limit(1)
    )
    task_flow_id = result.scalar()
    assert task_flow_id == past_schedule.flow_id

def test_parse_interval():
    """Test interval string parsing."""
    assert parse_interval("30m") == timedelta(minutes=30)
    assert parse_interval("2h") == timedelta(hours=2)
    assert parse_interval("1d") == timedelta(days=1)
    
    with pytest.raises(ValueError):
        parse_interval("invalid")
    
    with pytest.raises(ValueError):
        parse_interval("30x")  # Invalid unit
    
    with pytest.raises(ValueError):
        parse_interval("0m")  # Zero duration
        
    with pytest.raises(ValueError):
        parse_interval("-1h")  # Negative duration
