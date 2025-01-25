"""Test cases for task manager."""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import select

from automagik.core.flows import TaskManager
from automagik.core.database.models import Task, Flow, TaskLog

@pytest.fixture
async def task_manager(session):
    """Create a task manager for testing."""
    return TaskManager(session)

@pytest.fixture
async def test_flow(session):
    """Create a test flow."""
    flow = Flow(
        id=uuid4(),
        source_id=str(uuid4()),
        name="Test Flow",
        description="A test flow",
        source="langflow",  # Required field
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(flow)
    await session.commit()
    return flow

@pytest.fixture
async def failed_task(session, test_flow):
    """Create a failed task."""
    task = Task(
        id=uuid4(),
        flow_id=test_flow.id,
        status="failed",
        error="Test error",
        input_data={"test": "data"},
        tries=0,
        max_retries=3,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        started_at=datetime.utcnow(),
        finished_at=datetime.utcnow()
    )
    session.add(task)
    await session.commit()
    return task

@pytest.mark.asyncio
async def test_retry_task_success(task_manager, failed_task):
    """Test retrying a failed task successfully."""
    # Retry the task
    retried_task = await task_manager.retry_task(str(failed_task.id))
    
    assert retried_task is not None
    assert retried_task.id == failed_task.id  # Same task ID
    assert retried_task.status == "pending"
    assert retried_task.tries == 1
    assert retried_task.error is None
    assert retried_task.started_at is None
    assert retried_task.finished_at is None
    
    # Check next retry time (should be 5 minutes for first retry)
    assert retried_task.next_retry_at is not None
    retry_delay = retried_task.next_retry_at - datetime.utcnow()
    assert abs(retry_delay.total_seconds() - 300) < 5  # Within 5 seconds of 5 minutes

@pytest.mark.asyncio
async def test_retry_task_exponential_backoff(task_manager, failed_task):
    """Test that retry delays follow exponential backoff."""
    # First retry (5 minutes)
    task1 = await task_manager.retry_task(str(failed_task.id))
    delay1 = task1.next_retry_at - datetime.utcnow()
    assert abs(delay1.total_seconds() - 300) < 5  # ~5 minutes
    
    # Fail the task again
    task1.status = "failed"
    await task_manager.session.commit()
    
    # Second retry (10 minutes)
    task2 = await task_manager.retry_task(str(task1.id))
    delay2 = task2.next_retry_at - datetime.utcnow()
    assert abs(delay2.total_seconds() - 600) < 5  # ~10 minutes
    
    # Fail the task again
    task2.status = "failed"
    await task_manager.session.commit()
    
    # Third retry (20 minutes)
    task3 = await task_manager.retry_task(str(task2.id))
    delay3 = task3.next_retry_at - datetime.utcnow()
    assert abs(delay3.total_seconds() - 1200) < 5  # ~20 minutes

@pytest.mark.asyncio
async def test_retry_task_max_retries(task_manager, failed_task):
    """Test that tasks cannot be retried beyond max_retries."""
    # Set tries to max
    failed_task.tries = failed_task.max_retries
    await task_manager.session.commit()
    
    # Try to retry
    retried_task = await task_manager.retry_task(str(failed_task.id))
    assert retried_task is None  # Should not allow retry

@pytest.mark.asyncio
async def test_retry_task_non_failed(task_manager, failed_task):
    """Test that only failed tasks can be retried."""
    # Set task to running
    failed_task.status = "running"
    await task_manager.session.commit()
    
    # Try to retry
    retried_task = await task_manager.retry_task(str(failed_task.id))
    assert retried_task is None  # Should not allow retry

@pytest.mark.asyncio
async def test_retry_task_logs(task_manager, failed_task, session):
    """Test that task logs are preserved when retrying."""
    # Add a test log
    test_log = TaskLog(
        id=uuid4(),
        task_id=failed_task.id,
        level="error",
        message="Test error log",
        created_at=datetime.utcnow()
    )
    session.add(test_log)
    await session.commit()
    
    # Retry the task
    retried_task = await task_manager.retry_task(str(failed_task.id))
    
    # Check that the log still exists
    result = await session.execute(
        select(TaskLog).where(TaskLog.task_id == retried_task.id)
    )
    logs = result.scalars().all()
    assert len(logs) == 1
    assert logs[0].message == "Test error log"
