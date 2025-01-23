import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock
import uuid
from datetime import datetime
from automagik.core.database.models import FlowDB, Schedule

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session

@pytest.fixture
def sample_flow():
    """Create a sample flow for testing"""
    return FlowDB(
        id=uuid.uuid4(),
        name="Test Flow",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        data={"nodes": [], "edges": []}
    )

@pytest.fixture
def sample_schedule(sample_flow):
    """Create a sample schedule for testing"""
    return Schedule(
        id=uuid.uuid4(),
        flow_id=sample_flow.id,
        flow=sample_flow,
        schedule_type="interval",
        schedule_expr="5m",
        next_run_at=datetime.now(),
        status="active"
    )
