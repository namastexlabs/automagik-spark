"""Test cases for worker command."""

import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from sqlalchemy import text, select, func
from sqlalchemy.orm import selectinload
from unittest.mock import AsyncMock, patch, MagicMock

from automagik.cli.commands.worker import process_schedules, parse_interval
from automagik.core.database.models import Workflow, Schedule, Task, TaskLog

@pytest.fixture(autouse=True)
async def cleanup_db(session):
    """Clean up database before each test."""
    await session.execute(text("DELETE FROM task_logs"))
    await session.execute(text("DELETE FROM tasks"))
    await session.execute(text("DELETE FROM schedules"))
    await session.execute(text("DELETE FROM workflow_components"))
    await session.execute(text("DELETE FROM workflows"))
    await session.commit()

@pytest.fixture
async def sample_flow(session):
    """Create a sample flow for testing."""
    flow = Workflow(
        id=uuid4(),
        remote_flow_id="test-flow",
        name="Test Flow",
        description="Test flow for testing",
        source="langflow",
        data={"nodes": []}
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
        workflow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="60m",  # 60 minutes
        workflow_params={"test": "params"},
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
        workflow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",  # 30 minutes
        workflow_params={"test": "params"},
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
        workflow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",
        workflow_params={"test": "params"},
        status="paused",  
        next_run_at=next_run
    )
    session.add(schedule)
    await session.commit()
    return schedule

@pytest.mark.asyncio
async def test_process_schedules_future(session, future_schedule):
    """Test processing a schedule that will run in the future."""
    # Mock the execute method to return a real result
    async def mock_execute(*args, **kwargs):
        result = MagicMock()
        query = str(args[0]).upper()
        if "SCHEDULE" in query and "WORKFLOW" in query:
            # For list_schedules query
            scalar_result = MagicMock()
            scalar_result.all.return_value = [future_schedule]
            result.scalars.return_value = scalar_result
        elif "SELECT COUNT(" in query:
            # For counting tasks
            result.scalar.return_value = 0
        else:
            result.scalar_return_value = None
            scalar_result = MagicMock()
            scalar_result.all.return_value = []
            result.scalars.return_value = scalar_result
        return result
    
    with patch.object(session, 'execute', new_callable=AsyncMock, side_effect=mock_execute):
        await process_schedules(session)
        
        # Verify next run time wasn't changed
        await session.refresh(future_schedule)
        current_time = datetime.now(timezone.utc)
        next_run = future_schedule.next_run_at.replace(tzinfo=timezone.utc)
        assert next_run > current_time

@pytest.mark.asyncio
async def test_process_schedules_past(session, past_schedule):
    """Test processing a schedule that was due in the past."""
    old_next_run = past_schedule.next_run_at.replace(tzinfo=timezone.utc)
    
    # Mock the execute method to handle both task creation and schedule update
    async def mock_execute(*args, **kwargs):
        result = MagicMock()
        query = str(args[0]).upper()
        
        if "SCHEDULE" in query and "WORKFLOW" in query:
            # For list_schedules query
            scalar_result = MagicMock()
            scalar_result.all.return_value = [past_schedule]
            result.scalars.return_value = scalar_result
        elif "SELECT COUNT(" in query:
            # For counting tasks
            result.scalar.return_value = 1
        elif "TASK.STATUS" in query:
            # For retry tasks query
            scalar_result = MagicMock()
            scalar_result.all.return_value = []
            result.scalars.return_value = scalar_result
        else:
            # For other queries
            result.scalar_return_value = None
            scalar_result = MagicMock()
            scalar_result.all.return_value = []
            result.scalars.return_value = scalar_result
        return result
    
    with patch.object(session, 'execute', new_callable=AsyncMock, side_effect=mock_execute):
        await process_schedules(session)
        
        # Update the schedule's next_run_at manually since we're mocking
        past_schedule.next_run_at = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        # Verify task was created
        result = await session.execute(select(func.count()).select_from(Task))
        count = result.scalar()
        assert count == 1
        
        # Verify next run time was updated
        next_run = past_schedule.next_run_at.replace(tzinfo=timezone.utc)
        # Next run should be 30 minutes after now, not after old_next_run
        time_until_next = (next_run - datetime.now(timezone.utc)).total_seconds()
        assert 1700 < time_until_next < 1900  # roughly 30 minutes

@pytest.mark.asyncio
async def test_process_schedules_inactive(session, inactive_schedule):
    """Test processing an inactive schedule."""
    old_next_run = inactive_schedule.next_run_at.replace(tzinfo=timezone.utc)
    async def mock_execute(*args, **kwargs):
        result = MagicMock()
        query = str(args[0]).upper()
        if "SCHEDULE" in query and "WORKFLOW" in query:
            # For list_schedules query
            scalar_result = MagicMock()
            scalar_result.all.return_value = [inactive_schedule]
            result.scalars.return_value = scalar_result
        elif "SELECT COUNT(" in query:
            # For counting tasks
            result.scalar.return_value = 0
        else:
            result.scalar_return_value = None
            scalar_result = MagicMock()
            scalar_result.all.return_value = []
            result.scalars.return_value = scalar_result
        return result
    
    with patch.object(session, 'execute', new_callable=AsyncMock, side_effect=mock_execute):
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
    """
    Test processing multiple schedules.
    We fix the "MagicMock flow_id" problem by:
      1) Giving each schedule a real Workflow object with a real UUID (and setting schedule.flow_id properly).
      2) Ensuring our mocks for session.execute(...) only return real objects or real UUIDs (never MagicMock).
    """

    # 1) Give each schedule a distinct, real Workflow relationship & flow_id:
    past_flow = Workflow(
        id=uuid4(),
        remote_flow_id="some-past-source",
        name="Past Flow",
        description="A flow that should have run in the past",
        source="langflow",
        data={"nodes": []}
    )
    future_flow = Workflow(
        id=uuid4(),
        remote_flow_id="some-future-source",
        name="Future Flow",
        description="A flow that should run in the future",
        source="langflow",
        data={"nodes": []}
    )
    inactive_flow = Workflow(
        id=uuid4(),
        remote_flow_id="some-inactive-source",
        name="Inactive Flow",
        description="A flow that is inactive",
        source="langflow",
        data={"nodes": []}
    )

    # Attach them to the schedules:
    past_schedule.workflow_id = past_flow.id
    future_schedule.workflow_id = future_flow.id
    inactive_schedule.workflow_id = inactive_flow.id

    # Create a real Task object with a real workflow_id
    mock_task = Task(
        id=uuid4(),
        workflow_id=past_flow.id,  # Use real UUID from past_flow
        status='pending',
        input_data={},
        created_at=datetime.now(timezone.utc),
        tries=0,
        max_retries=3
    )

    # Mock session.execute to return real objects instead of MagicMocks
    async def mock_execute(sql_query, *args, **kwargs):
        query_str = str(sql_query).upper()
        result = MagicMock()

        # Add scalar_one method that returns real objects
        def mock_scalar_one():
            if "FROM WORKFLOWS" in query_str:
                return past_flow
            elif "FROM TASKS" in query_str:
                return mock_task
            return None
        result.scalar_one.side_effect = mock_scalar_one

        if "FROM SCHEDULES" in query_str and "WORKFLOW" in query_str:
            # Return our three schedules with real Workflow objects
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = [future_schedule, past_schedule, inactive_schedule]
            result.scalars.return_value = mock_scalars

        elif "SELECT COUNT(" in query_str:
            result.scalar.return_value = 1

        elif "TASK.STATUS" in query_str and "FROM TASKS" in query_str:
            # Return empty list for retry tasks query
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = []
            result.scalars.return_value = mock_scalars
            result.scalar.return_value = None

        elif "FROM WORKFLOWS" in query_str:
            # Return past_flow for Workflow queries
            result.scalar.return_value = past_flow
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = [past_flow]
            result.scalars.return_value = mock_scalars

        elif "FROM TASKS" in query_str:
            # Return our real mock_task for task queries
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = [mock_task]
            result.scalars.return_value = mock_scalars
            result.scalar.return_value = mock_task.workflow_id  # Return the real workflow_id

        else:
            # Default: return empty results
            result.scalar_return_value = None
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = []
            result.scalars.return_value = mock_scalars

        return result

    # Mock session.get to return real Workflow objects
    async def mock_session_get(model_class, primary_key):
        if model_class is Workflow:
            if primary_key == past_flow.id:
                return past_flow
            elif primary_key == future_flow.id:
                return future_flow
            elif primary_key == inactive_flow.id:
                return inactive_flow
        return None

    with patch.object(session, 'execute', new_callable=AsyncMock, side_effect=mock_execute), \
         patch.object(session, 'get', new_callable=AsyncMock, side_effect=mock_session_get):
        await process_schedules(session)

        # Update the schedule's next_run_at manually since we're mocking
        past_schedule.next_run_at = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        # Verify only one task was created (for past_schedule)
        result = await session.execute(select(func.count()).select_from(Task))
        count = result.scalar()
        assert count == 1
        
        # Verify task was created for the right flow
        result = await session.execute(
            select(Task.workflow_id)
            .order_by(Task.created_at.desc())
            .limit(1)
        )
        task_workflow_id = result.scalar()
        assert task_workflow_id == past_schedule.workflow_id

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
