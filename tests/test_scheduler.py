import uuid
import pytest
from datetime import datetime, timedelta
import pytz
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session
from automagik.core.scheduler.scheduler import SchedulerService
from automagik.core.scheduler.exceptions import InvalidScheduleError, FlowNotFoundError
from automagik.core.database.models import Schedule, FlowDB

@pytest.fixture
def mock_session():
    session = Mock(spec=Session)
    session.commit = Mock()
    session.rollback = Mock()
    return session

@pytest.fixture
def scheduler_service(mock_session):
    service = SchedulerService(mock_session)
    service.timezone = pytz.UTC
    return service

@pytest.fixture
def sample_flow():
    return FlowDB(
        id=uuid.uuid4(),
        name="test_flow",
        input_component="input_node",
        output_component="output_node"
    )

@pytest.fixture
def sample_schedule(sample_flow):
    return Schedule(
        id=uuid.uuid4(),
        flow_id=sample_flow.id,
        flow=sample_flow,
        schedule_type="cron",
        schedule_expr="* * * * *",
        flow_params={},
        next_run_at=datetime.now(pytz.UTC),
        status="active"
    )

def test_create_oneshot_schedule_success(scheduler_service, mock_session, sample_flow):
    # Setup
    future_time = datetime.now(pytz.UTC) + timedelta(days=1)
    schedule_expr = future_time.isoformat()
    mock_session.query.return_value.filter.return_value.first.return_value = sample_flow

    # Execute
    schedule = scheduler_service.create_schedule(
        flow_name="test_flow",
        schedule_type="oneshot",
        schedule_expr=schedule_expr
    )

    # Verify
    assert schedule.schedule_type == "oneshot"
    assert schedule.schedule_expr == schedule_expr
    assert schedule.next_run_at == future_time
    assert schedule.status == "active"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_oneshot_schedule_past_time(scheduler_service, mock_session, sample_flow):
    # Setup
    past_time = datetime.now(pytz.UTC) - timedelta(days=1)
    schedule_expr = past_time.isoformat()
    mock_session.query.return_value.filter.return_value.first.return_value = sample_flow

    # Execute and verify
    with pytest.raises(InvalidScheduleError, match="One-time schedule must be in the future"):
        scheduler_service.create_schedule(
            flow_name="test_flow",
            schedule_type="oneshot",
            schedule_expr=schedule_expr
        )

def test_create_oneshot_schedule_invalid_format(scheduler_service, mock_session, sample_flow):
    # Setup
    mock_session.query.return_value.filter.return_value.first.return_value = sample_flow

    # Execute and verify
    with pytest.raises(InvalidScheduleError, match="Invalid datetime format"):
        scheduler_service.create_schedule(
            flow_name="test_flow",
            schedule_type="oneshot",
            schedule_expr="invalid-date"
        )

def test_get_due_schedules_with_oneshot(scheduler_service, mock_session, sample_flow):
    # Setup
    current_time = datetime.now(pytz.UTC)
    past_time = current_time - timedelta(minutes=5)
    future_time = current_time + timedelta(minutes=5)
    
    past_schedule = Schedule(
        id=uuid.uuid4(),
        flow_id=sample_flow.id,
        flow=sample_flow,
        schedule_type="oneshot",
        schedule_expr=past_time.isoformat(),
        next_run_at=past_time,
        status="active"
    )
    
    future_schedule = Schedule(
        id=uuid.uuid4(),
        flow_id=sample_flow.id,
        flow=sample_flow,
        schedule_type="oneshot",
        schedule_expr=future_time.isoformat(),
        next_run_at=future_time,
        status="active"
    )
    
    # Mock query to only return past_schedule when filtering for due schedules
    mock_session.query.return_value.filter.return_value.all.return_value = [past_schedule]

    # Execute
    due_schedules = scheduler_service.get_due_schedules()

    # Verify
    assert len(due_schedules) == 1
    assert due_schedules[0].id == past_schedule.id
    assert due_schedules[0].status == "completed"  # Should be marked completed
    mock_session.commit.assert_called_once()  # Should commit the status change

def test_update_schedule_next_run_oneshot(scheduler_service, mock_session):
    # Setup
    current_time = datetime.now(pytz.UTC)
    schedule = Schedule(
        id=uuid.uuid4(),
        schedule_type="oneshot",
        schedule_expr=current_time.isoformat(),
        next_run_at=current_time,
        status="active"
    )

    # Execute
    scheduler_service.update_schedule_next_run(schedule)

    # Verify
    assert schedule.status == "completed"
    mock_session.commit.assert_called_once()
