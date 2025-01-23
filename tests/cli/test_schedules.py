"""Tests for schedule creation and listing"""
import pytest
from datetime import datetime, timedelta
import uuid
from click.testing import CliRunner
from unittest.mock import MagicMock
from automagik.cli.commands.schedules import schedules
from automagik.core.scheduler.exceptions import InvalidScheduleError
from automagik.core.database.models import Schedule

class TestScheduleCreate:
    """Test schedule creation commands"""

    def test_oneshot_schedule_create(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    dt = datetime.fromisoformat(schedule_expr)
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=dt
                    )
                raise InvalidScheduleError("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test creating a one-time schedule
        future_time = datetime.now() + timedelta(days=1)
        schedule_time = future_time.strftime("%Y-%m-%dT%H:%M:%S")
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'oneshot',
            '--expr', schedule_time,
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 0
        assert "Created schedule successfully" in result.output

    def test_oneshot_schedule_past_time(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule with past time"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    dt = datetime.fromisoformat(schedule_expr)
                    if dt <= datetime.now():
                        raise InvalidScheduleError("One-time schedule must be in the future")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=dt
                    )
                raise InvalidScheduleError("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Try to create a schedule for yesterday
        past_time = datetime.now() - timedelta(days=1)
        schedule_time = past_time.strftime("%Y-%m-%dT%H:%M:%S")
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'oneshot',
            '--expr', schedule_time,
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 1
        assert "One-time schedule must be in the future" in result.output

    def test_oneshot_schedule_invalid_format(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule with invalid datetime format"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    try:
                        datetime.fromisoformat(schedule_expr)
                    except ValueError:
                        raise InvalidScheduleError("Invalid datetime format")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=datetime.now()
                    )
                raise InvalidScheduleError("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test invalid datetime format
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'oneshot',
            '--expr', 'invalid-date',
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 1
        assert "Invalid datetime format" in result.output

class TestScheduleList:
    """Test schedule listing commands"""

    def test_list_oneshot_schedules(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test listing one-time schedules with different statuses"""
        # Create sample one-time schedules
        future_time = datetime.now() + timedelta(days=1)
        past_time = datetime.now() - timedelta(hours=1)

        active_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="oneshot",
            schedule_expr=future_time.isoformat(),
            next_run_at=future_time,
            status="active"
        )

        completed_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="oneshot",
            schedule_expr=past_time.isoformat(),
            next_run_at=past_time,
            status="completed"
        )

        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def list_schedules(self, flow_name=None, status=None):
                schedules = [active_schedule, completed_schedule]
                if status:
                    schedules = [s for s in schedules if s.status == status]
                return schedules

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Test listing all schedules
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert str(active_schedule.id) in result.output
        assert str(completed_schedule.id) in result.output

        # Test filtering by type
        result = runner.invoke(schedules, ['list', '--type', 'oneshot'])
        assert result.exit_code == 0
        assert str(active_schedule.id) in result.output
        assert str(completed_schedule.id) in result.output

        # Test filtering by status
        result = runner.invoke(schedules, ['list', '--status', 'active'])
        assert result.exit_code == 0
        assert str(active_schedule.id) in result.output
        assert str(completed_schedule.id) not in result.output
