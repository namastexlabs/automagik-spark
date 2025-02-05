"""Test cases for task manager."""

import pytest
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from sqlalchemy import select

from automagik.core.workflows import TaskManager
from automagik.core.database.models import Task, Workflow, TaskLog
from unittest.mock import MagicMock, AsyncMock


@pytest.fixture
async def task_manager(session):
    """Create a task manager for testing."""
    return TaskManager(session)


@pytest.fixture
async def test_flow(session):
    """Create a test flow."""
    flow = Workflow(
        id=uuid4(),
        remote_flow_id=str(uuid4()),
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
        workflow_id=test_flow.id,
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
    """Test successful task retry."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    await task_manager.session.commit()

    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.tries == 1


@pytest.mark.asyncio
async def test_retry_task_exponential_backoff(task_manager, failed_task):
    """Test task retry with exponential backoff."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    failed_task.tries = 2
    await task_manager.session.commit()

    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.tries == 3
    assert retried_task.next_retry_at > datetime.utcnow()


@pytest.mark.asyncio
async def test_retry_task_max_retries(task_manager, failed_task):
    """Test task retry with max retries reached."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    failed_task.tries = failed_task.max_retries
    await task_manager.session.commit()

    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is None


@pytest.mark.asyncio
async def test_retry_task_non_failed(task_manager, failed_task):
    """Test that only failed tasks can be retried."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "running"
    await task_manager.session.commit()

    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is None


@pytest.mark.asyncio
async def test_retry_task_logs(task_manager, failed_task, session):
    """Test that task logs are preserved when retrying."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    await session.commit()

    # Add a test log
    test_log = TaskLog(
        id=uuid4(),
        task_id=task_id,
        level="error",
        message="Test error log",
        created_at=datetime.now(timezone.utc)
    )
    session.add(test_log)
    await session.commit()

    # Retry the task
    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is not None
    assert retried_task.status == "pending"

    # Check that logs are preserved
    result = await session.execute(select(TaskLog).where(TaskLog.task_id == task_id))
    logs = result.scalars().all()
    assert len(logs) == 2  # Original log + new retry log
    assert any(log.message == "Test error log" for log in logs)
    assert any(log.message == failed_task.error for log in logs)


@pytest.mark.asyncio
async def test_retry_task_success_without_session():
    """Test successfully retrying a failed task."""
    session = AsyncMock()
    task = Task(
        id=uuid.uuid4(),
        status="failed",
        tries=0,
        max_retries=3,
        error="Previous error"
    )
    
    # Mock task retrieval
    result = AsyncMock()
    result.scalars.return_value.first.return_value = task
    session.execute.return_value = result
    
    task_manager = TaskManager(session)
    retried_task = await task_manager.retry_task(str(task.id))
    
    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.error is None
    assert retried_task.tries == 1


@pytest.mark.asyncio
async def test_retry_task_exponential_backoff_without_session():
    """Test exponential backoff for retried tasks."""
    session = AsyncMock()
    task = Task(
        id=uuid.uuid4(),
        status="failed",
        tries=2,
        max_retries=3,
        error="Previous error"
    )
    
    # Mock task retrieval
    result = AsyncMock()
    result.scalars.return_value.first.return_value = task
    session.execute.return_value = result
    
    task_manager = TaskManager(session)
    retried_task = await task_manager.retry_task(str(task.id))
    
    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.tries == 3
    assert retried_task.next_retry_at > datetime.utcnow()


@pytest.mark.asyncio
async def test_retry_task_max_retries_without_session():
    """Test task retry when max retries reached."""
    session = AsyncMock()
    task = Task(
        id=uuid.uuid4(),
        status="failed",
        tries=3,
        max_retries=3,
        error="Previous error"
    )
    
    # Mock task retrieval
    result = AsyncMock()
    result.scalars.return_value.first.return_value = task
    session.execute.return_value = result
    
    task_manager = TaskManager(session)
    with pytest.raises(ValueError, match="Task has reached maximum retries"):
        await task_manager.retry_task(str(task.id))


@pytest.mark.asyncio
async def test_retry_task_non_failed_without_session():
    """Test retrying a non-failed task."""
    session = AsyncMock()
    task = Task(
        id=uuid.uuid4(),
        status="pending",
        tries=0,
        max_retries=3
    )
    
    # Mock task retrieval
    result = AsyncMock()
    result.scalars.return_value.first.return_value = task
    session.execute.return_value = result
    
    task_manager = TaskManager(session)
    with pytest.raises(ValueError, match="Task is not in failed state"):
        await task_manager.retry_task(str(task.id))


@pytest.mark.asyncio
async def test_retry_task_logs_without_session():
    """Test task logs are created when retrying tasks."""
    session = AsyncMock()
    task = Task(
        id=uuid.uuid4(),
        status="failed",
        tries=1,
        max_retries=3,
        error="Previous error"
    )
    
    # Mock task retrieval
    result = AsyncMock()
    result.scalars.return_value.first.return_value = task
    session.execute.return_value = result
    
    task_manager = TaskManager(session)
    retried_task = await task_manager.retry_task(str(task.id))
    
    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.tries == 2
    
    # Verify task log was created
    session.add.assert_called_once()
    task_log = session.add.call_args[0][0]
    assert isinstance(task_log, TaskLog)
    assert task_log.task_id == task.id
    assert task_log.error == "Previous error"
    assert task_log.tries == 1


@pytest.mark.asyncio
async def test_retry_task_max_retries_with_session(task_manager, failed_task):
    """Test that tasks cannot be retried beyond max_retries."""
    # Set tries to max
    failed_task.tries = failed_task.max_retries
    await task_manager.session.commit()
    
    # Try to retry
    retried_task = await task_manager.retry_task(str(failed_task.id))
    assert retried_task is None  # Should not allow retry


@pytest.mark.asyncio
async def test_retry_task_non_failed_with_session(task_manager, failed_task):
    """Test that only failed tasks can be retried."""
    # Set task to running
    failed_task.status = "running"
    await task_manager.session.commit()
    
    # Try to retry
    retried_task = await task_manager.retry_task(str(failed_task.id))
    assert retried_task is None  # Should not allow retry


@pytest.mark.asyncio
async def test_retry_task_logs_with_session(task_manager, failed_task, session):
    """Test that task logs are preserved when retrying."""
    # Add a test log
    test_log = TaskLog(
        id=uuid4(),
        task_id=failed_task.id,
        level="error",
        message="Test error log",
        created_at=datetime.now(timezone.utc)
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
    assert len(logs) == 2  # Original log + new retry log
    assert any(log.message == "Test error log" for log in logs)
    assert any(log.message == failed_task.error for log in logs)
