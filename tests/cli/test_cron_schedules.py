"""Tests for cron schedule commands"""
import pytest
from datetime import datetime, timedelta
import uuid
from click.testing import CliRunner
from unittest.mock import MagicMock
from automagik.cli.commands.schedules import schedules
from automagik.core.scheduler.exceptions import InvalidScheduleError
from automagik.core.database.models import Schedule

class TestCronSchedules:
    """Test cron schedule commands"""

    def test_cron_schedule_create(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a cron schedule"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'cron':
                    # Basic cron validation (simplified for testing)
                    parts = schedule_expr.split()
                    if len(parts) != 5:
                        raise InvalidScheduleError("Invalid cron format. Must have 5 parts: minute hour day month weekday")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=datetime.now()
                    )
                raise InvalidScheduleError("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test creating a cron schedule
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'cron',
            '--expr', '0 8 * * 1-5',  # Every weekday at 8 AM
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 0
        assert "Created schedule successfully" in result.output

    def test_cron_schedule_invalid_format(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a cron schedule with invalid format"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'cron':
                    # Basic cron validation (simplified for testing)
                    parts = schedule_expr.split()
                    if len(parts) != 5:
                        raise InvalidScheduleError("Invalid cron format. Must have 5 parts: minute hour day month weekday")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=datetime.now()
                    )
                raise InvalidScheduleError("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test invalid cron format (wrong number of parts)
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'cron',
            '--expr', '* * *',  # Missing parts
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 1
        assert "Invalid cron format" in result.output

    def test_cron_schedule_common_patterns(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating cron schedules with common patterns"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'cron':
                    # Basic cron validation (simplified for testing)
                    parts = schedule_expr.split()
                    if len(parts) != 5:
                        raise InvalidScheduleError("Invalid cron format. Must have 5 parts: minute hour day month weekday")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=datetime.now()
                    )
                raise InvalidScheduleError("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test common cron patterns
        patterns = [
            '*/30 * * * *',  # Every 30 minutes
            '0 * * * *',     # Every hour
            '0 8 * * *',     # Every day at 8 AM
            '0 8 * * 1-5'    # Every weekday at 8 AM
        ]

        for pattern in patterns:
            result = runner.invoke(schedules, [
                'create',
                sample_flow.name,
                '--type', 'cron',
                '--expr', pattern,
                '--input', '{"key": "value"}'
            ])

            assert result.exit_code == 0
            assert "Created schedule successfully" in result.output
