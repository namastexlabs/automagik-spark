import pytest
from datetime import datetime, timedelta
import pytz
import uuid
from unittest.mock import patch, Mock
from automagik.cli.scheduler_service import SchedulerService
from automagik.core.database.models import Schedule, FlowDB, Task

@pytest.fixture
def scheduler(db_session):
    return SchedulerService(db_session)

def test_get_current_time(scheduler):
    current_time = scheduler._get_current_time()
    assert isinstance(current_time, datetime)
    assert current_time.tzinfo is not None

def test_calculate_next_run_interval(scheduler):
    # Test minutes
    next_run = scheduler._calculate_next_run('interval', '30m')
    assert next_run > scheduler._get_current_time()
    assert next_run < scheduler._get_current_time() + timedelta(minutes=31)

    # Test hours
    next_run = scheduler._calculate_next_run('interval', '2h')
    assert next_run > scheduler._get_current_time()
    assert next_run < scheduler._get_current_time() + timedelta(hours=3)

    # Test days
    next_run = scheduler._calculate_next_run('interval', '1d')
    assert next_run > scheduler._get_current_time()
    assert next_run < scheduler._get_current_time() + timedelta(days=2)

    # Test invalid interval
    with pytest.raises(ValueError):
        scheduler._calculate_next_run('interval', '30x')

def test_calculate_next_run_cron(scheduler):
    # Test every minute
    next_run = scheduler._calculate_next_run('cron', '* * * * *')
    assert next_run > scheduler._get_current_time()
    assert next_run < scheduler._get_current_time() + timedelta(minutes=2)

    # Test specific time
    next_run = scheduler._calculate_next_run('cron', '0 12 * * *')  # noon every day
    assert next_run.hour == 12
    assert next_run.minute == 0

def test_calculate_next_run_oneshot(scheduler):
    future_time = scheduler._get_current_time() + timedelta(hours=1)
    next_run = scheduler._calculate_next_run('oneshot', future_time.isoformat())
    assert abs((next_run - future_time).total_seconds()) < 1

    # Test past time
    past_time = scheduler._get_current_time() - timedelta(hours=1)
    with pytest.raises(ValueError):
        scheduler._calculate_next_run('oneshot', past_time.isoformat())

def test_create_schedule(scheduler, db_session):
    flow_id = uuid.uuid4()
    flow = FlowDB(
        id=flow_id,
        name='Test Flow',
        source='langflow',
        source_id='test-source-id'
    )
    db_session.add(flow)
    db_session.commit()

    # Test interval schedule
    schedule = scheduler.create_schedule(
        flow_id=flow_id,
        schedule_type='interval',
        schedule_expr='30m',
        flow_params={'test': 'value'}
    )
    assert schedule.flow_id == flow_id
    assert schedule.schedule_type == 'interval'
    assert schedule.schedule_expr == '30m'
    assert schedule.flow_params == {'test': 'value'}
    assert schedule.next_run_at > scheduler._get_current_time()

def test_get_due_schedules(scheduler, db_session):
    flow_id = uuid.uuid4()
    flow = FlowDB(
        id=flow_id,
        name='Test Flow',
        source='langflow',
        source_id='test-source-id'
    )
    db_session.add(flow)
    db_session.commit()
    
    # Add a due schedule
    past_time = scheduler._get_current_time() - timedelta(minutes=5)
    schedule_id = uuid.uuid4()
    due_schedule = Schedule(
        id=schedule_id,
        flow_id=flow_id,
        schedule_type='interval',
        schedule_expr='30m',
        next_run_at=past_time
    )
    
    # Add a future schedule
    future_time = scheduler._get_current_time() + timedelta(minutes=5)
    future_schedule = Schedule(
        id=uuid.uuid4(),
        flow_id=flow_id,
        schedule_type='interval',
        schedule_expr='30m',
        next_run_at=future_time
    )
    
    db_session.add_all([due_schedule, future_schedule])
    db_session.commit()
    
    due_schedules = scheduler.get_due_schedules()
    assert len(due_schedules) == 1
    assert due_schedules[0].id == schedule_id

def test_update_schedule_next_run(scheduler, db_session):
    flow_id = uuid.uuid4()
    flow = FlowDB(
        id=flow_id,
        name='Test Flow',
        source='langflow',
        source_id='test-source-id'
    )
    schedule = Schedule(
        id=uuid.uuid4(),
        flow_id=flow_id,
        schedule_type='interval',
        schedule_expr='30m'
    )
    db_session.add_all([flow, schedule])
    db_session.commit()
    
    old_next_run = schedule.next_run_at
    scheduler.update_schedule_next_run(schedule)
    assert schedule.next_run_at > old_next_run

def test_create_task(scheduler, db_session):
    flow_id = uuid.uuid4()
    flow = FlowDB(
        id=flow_id,
        name='Test Flow',
        source='langflow',
        source_id='test-source-id'
    )
    schedule_id = uuid.uuid4()
    schedule = Schedule(
        id=schedule_id,
        flow_id=flow_id,
        schedule_type='interval',
        schedule_expr='30m',
        flow_params={'test': 'value'}
    )
    db_session.add_all([flow, schedule])
    db_session.commit()
    
    task = scheduler.create_task(schedule)
    assert task.flow_id == flow_id
    assert task.status == 'pending'
    assert task.input_data == {'test': 'value'}

def test_log_task_start(scheduler, db_session):
    flow_id = uuid.uuid4()
    flow = FlowDB(
        id=flow_id,
        name='Test Flow',
        source='langflow',
        source_id='test-source-id'
    )
    task_id = uuid.uuid4()
    task = Task(
        id=task_id,
        flow_id=flow_id,
        status='pending'
    )
    db_session.add_all([flow, task])
    db_session.commit()
    
    scheduler.log_task_start(task)
    assert task.status == 'running'
    assert task.started_at is not None

def test_log_task_completion(scheduler, db_session):
    flow_id = uuid.uuid4()
    flow = FlowDB(
        id=flow_id,
        name='Test Flow',
        source='langflow',
        source_id='test-source-id'
    )
    task_id = uuid.uuid4()
    task = Task(
        id=task_id,
        flow_id=flow_id,
        status='running'
    )
    db_session.add_all([flow, task])
    db_session.commit()
    
    output_data = {'result': 'success'}
    scheduler.log_task_completion(task, output_data)
    assert task.status == 'completed'
    assert task.completed_at is not None
    assert task.output_data == output_data

def test_log_task_error(scheduler, db_session):
    flow_id = uuid.uuid4()
    flow = FlowDB(
        id=flow_id,
        name='Test Flow',
        source='langflow',
        source_id='test-source-id'
    )
    task_id = uuid.uuid4()
    task = Task(
        id=task_id,
        flow_id=flow_id,
        status='running'
    )
    db_session.add_all([flow, task])
    db_session.commit()
    
    error_message = 'Test error'
    scheduler.log_task_error(task, error_message)
    assert task.status == 'failed'
    assert task.error == error_message
