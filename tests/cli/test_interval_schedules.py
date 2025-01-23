"""Tests for interval schedule commands"""
import pytest
from datetime import datetime, timedelta
import uuid
from click.testing import CliRunner
from unittest.mock import MagicMock
from automagik.cli.commands.schedules import schedules
from automagik.core.scheduler.exceptions import InvalidScheduleError
from automagik.core.database.models import Schedule

class TestIntervalSchedules:
    """Test interval schedule commands"""

    def test_interval_schedule_create(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating an interval schedule"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'interval':
                    # Basic interval validation (simplified for testing)
                    if not any(schedule_expr.endswith(unit) for unit in ['m', 'h', 'd']):
                        raise InvalidScheduleError("Invalid interval format. Use m (minutes), h (hours), or d (days)")
                    try:
                        int(schedule_expr[:-1])
                    except ValueError:
                        raise InvalidScheduleError("Invalid interval format. Must be a number followed by m, h, or d")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=datetime.now(),
                        status='active',
                        schedule_type='interval',
                        schedule_expr=schedule_expr,
                        flow=sample_flow,
                        flow_id=sample_flow.id
                    )
                raise InvalidScheduleError("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test creating an interval schedule
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'interval',
            '--expr', '30m',  # Every 30 minutes
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 0
        assert "Created schedule successfully" in result.output

    def test_interval_schedule_invalid_format(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating an interval schedule with invalid format"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'interval':
                    if not any(schedule_expr.endswith(unit) for unit in ['m', 'h', 'd']):
                        raise InvalidScheduleError("Invalid interval format. Use m (minutes), h (hours), or d (days)")
                    try:
                        int(schedule_expr[:-1])
                    except ValueError:
                        raise InvalidScheduleError("Invalid interval format. Must be a number followed by m, h, or d")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=datetime.now(),
                        status='active',
                        schedule_type='interval',
                        schedule_expr=schedule_expr,
                        flow=sample_flow,
                        flow_id=sample_flow.id
                    )
                raise InvalidScheduleError("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test invalid interval format
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'interval',
            '--expr', 'invalid',
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 1
        assert "Invalid interval format" in result.output
