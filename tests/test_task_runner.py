import pytest
from datetime import datetime
from cli.models import Task, Log
from cli.task_runner import TaskRunner
from cli.db import engine
from sqlalchemy.orm import Session

@pytest.fixture
def session():
    # Create a new session for each test
    session = Session(engine)
    yield session
    session.close()

@pytest.fixture
def task_runner():
    return TaskRunner()

@pytest.fixture
def sample_task(session):
    # Create a test task
    task = Task(
        agent_id=1,
        status='pending',
        input_data={'action': 'test'},
        output_data={},
        tries=0,
        max_retries=3,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    return task

def test_get_pending_tasks(task_runner, sample_task):
    """Test fetching pending tasks"""
    tasks = task_runner.get_pending_tasks()
    assert len(tasks) > 0
    assert tasks[0].id == sample_task.id
    assert tasks[0].status == 'pending'

def test_execute_task_success(task_runner, sample_task, session):
    """Test successful task execution"""
    # Override _run_agent_task to simulate success
    task_runner._run_agent_task = lambda task: True
    
    success = task_runner.execute_task(sample_task)
    
    # Refresh the task from database
    session.refresh(sample_task)
    
    assert success is True
    assert sample_task.status == 'completed'
    assert sample_task.tries == 0
    
    # Check logs
    logs = session.query(Log).filter_by(task_id=sample_task.id).all()
    assert len(logs) == 2  # Should have start and completion logs
    assert any('Starting task execution' in log.message for log in logs)
    assert any('completed successfully' in log.message for log in logs)

def test_execute_task_failure(task_runner, sample_task, session):
    """Test task execution failure and retry mechanism"""
    # Override _run_agent_task to simulate failure
    task_runner._run_agent_task = lambda task: False
    
    success = task_runner.execute_task(sample_task)
    
    # Refresh the task from database
    session.refresh(sample_task)
    
    assert success is False
    assert sample_task.status == 'pending'  # Should be pending for retry
    assert sample_task.tries == 1
    
    # Check logs
    logs = session.query(Log).filter_by(task_id=sample_task.id).all()
    assert len(logs) == 2  # Should have start and failure logs
    assert any('Will retry' in log.message for log in logs)

def test_max_retries_exceeded(task_runner, sample_task, session):
    """Test task failing after max retries"""
    # Override _run_agent_task to simulate failure
    task_runner._run_agent_task = lambda task: False
    
    # Execute task multiple times until max retries is exceeded
    for _ in range(sample_task.max_retries):
        task_runner.execute_task(sample_task)
        session.refresh(sample_task)
    
    assert sample_task.status == 'failed'
    assert sample_task.tries == sample_task.max_retries
    
    # Check logs
    logs = session.query(Log).filter_by(task_id=sample_task.id).all()
    assert any('Max retries exceeded' in log.message for log in logs)

def test_exception_handling(task_runner, sample_task, session):
    """Test handling of exceptions during task execution"""
    # Override _run_agent_task to raise an exception
    def raise_error(task):
        raise ValueError("Test error")
    task_runner._run_agent_task = raise_error
    
    success = task_runner.execute_task(sample_task)
    
    # Refresh the task from database
    session.refresh(sample_task)
    
    assert success is False
    assert sample_task.tries == 1
    
    # Check logs
    logs = session.query(Log).filter_by(task_id=sample_task.id).all()
    assert any('Test error' in log.message for log in logs) 