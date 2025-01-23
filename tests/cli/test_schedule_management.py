"""Tests for schedule management commands"""
import pytest
from datetime import datetime, timedelta
import uuid
from click.testing import CliRunner
from unittest.mock import MagicMock
from automagik.cli.commands.schedules import schedules
from automagik.core.scheduler.exceptions import ScheduleNotFoundError
from automagik.core.database.models import Schedule

class TestScheduleManagement:
    """Test schedule management commands"""

    def test_delete_schedule(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test deleting a schedule"""
        schedule_id = uuid.uuid4()

        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def delete_schedule(self, schedule_id):
                # Simulate schedule deletion
                try:
                    uuid.UUID(str(schedule_id))
                except ValueError:
                    raise ScheduleNotFoundError("Invalid schedule ID format")
                if str(schedule_id) == "00000000-0000-0000-0000-000000000000":
                    raise ScheduleNotFoundError(f"Schedule not found: {schedule_id}")
                return True

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Test successful deletion
        result = runner.invoke(schedules, ['delete', str(schedule_id)])
        assert result.exit_code == 0
        assert "Schedule deleted successfully" in result.output

        # Test deleting non-existent schedule
        result = runner.invoke(schedules, ['delete', '00000000-0000-0000-0000-000000000000'])
        assert result.exit_code == 1
        assert "Schedule not found" in result.output

    def test_list_schedules_filtering(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test listing schedules with various filters"""
        # Create sample schedules
        interval_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="interval",
            schedule_expr="5m",
            next_run_at=datetime.now() + timedelta(minutes=5),
            status="active"
        )

        cron_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="cron",
            schedule_expr="0 * * * *",
            next_run_at=datetime.now() + timedelta(hours=1),
            status="active"
        )

        oneshot_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="oneshot",
            schedule_expr=(datetime.now() + timedelta(days=1)).isoformat(),
            next_run_at=datetime.now() + timedelta(days=1),
            status="active"
        )

        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def list_schedules(self, flow_name=None, status=None):
                schedules = [interval_schedule, cron_schedule, oneshot_schedule]
                if status:
                    schedules = [s for s in schedules if s.status == status]
                return schedules

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Test listing all schedules
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert str(interval_schedule.id) in result.output
        assert str(cron_schedule.id) in result.output
        assert str(oneshot_schedule.id) in result.output

        # Test filtering by type
        result = runner.invoke(schedules, ['list', '--type', 'interval'])
        assert result.exit_code == 0
        assert str(interval_schedule.id) in result.output
        assert str(cron_schedule.id) not in result.output
        assert str(oneshot_schedule.id) not in result.output

        # Test filtering by status
        result = runner.invoke(schedules, ['list', '--status', 'active'])
        assert result.exit_code == 0
        assert str(interval_schedule.id) in result.output
        assert str(cron_schedule.id) in result.output
        assert str(oneshot_schedule.id) in result.output

    def test_list_schedules_empty(self, runner, mock_db_session, monkeypatch):
        """Test listing schedules when none exist"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def list_schedules(self, flow_name=None, status=None):
                return []

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Test listing with no schedules
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert "No schedules found" in result.output
