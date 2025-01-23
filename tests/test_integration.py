import os
import uuid
import pytest
import tempfile
from sqlalchemy import create_engine
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
from datetime import datetime, timedelta

from automagik.cli.commands.flows import flows
from automagik.cli.commands.schedules import schedules
from automagik.core.database.models import FlowDB, Schedule
from automagik.core.database.session import get_db_session

@pytest.fixture
def temp_db(monkeypatch):
    """Create a temporary SQLite database for testing."""
    # Create a temporary file
    db_fd, db_path = tempfile.mkstemp()
    
    # Create the database engine
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create all tables
    FlowDB.metadata.create_all(engine)
    Schedule.metadata.create_all(engine)
    
    # Create a session factory
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Mock the get_db_session to return our test session
    monkeypatch.setattr('automagik.core.database.session.get_db_session', lambda: session)
    
    yield session
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def sample_flow(temp_db):
    """Create a sample flow in the database."""
    flow = FlowDB(
        id=uuid.uuid4(),
        name="Test Flow",
        description="A test flow",
        data={"nodes": [], "edges": []},
        source="langflow",
        source_id="test-flow-1",
        flow_version=1,
        input_component="test-input",
        output_component="test-output"
    )
    temp_db.add(flow)
    temp_db.commit()
    return flow

@pytest.fixture
def sample_schedule(temp_db, sample_flow):
    """Create a sample schedule in the database."""
    schedule = Schedule(
        id=uuid.uuid4(),
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="1m",
        next_run_at=datetime.utcnow() + timedelta(minutes=1),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    temp_db.add(schedule)
    temp_db.commit()
    return schedule

@pytest.fixture
def runner():
    """Create a Click CLI runner."""
    return CliRunner()

class TestIntegration:
    """Integration tests using a real SQLite database."""

    def test_flows_list(self, runner, temp_db, sample_flow, monkeypatch):
        """Test listing flows from the database."""
        # Clear existing flows
        temp_db.query(FlowDB).delete()
        temp_db.commit()

        # Create a test flow
        flow_id = uuid.uuid4()
        test_flow = FlowDB(
            id=flow_id,
            name="Test Flow",
            description="A test flow",
            data={"nodes": [], "edges": []},
            source="langflow",
            source_id="test-flow-1",
            flow_version=1,
            input_component="test-input",
            output_component="test-output"
        )
        temp_db.add(test_flow)
        temp_db.commit()
        temp_db.refresh(test_flow)

        # Mock the get_db_session to return our temp_db
        def mock_get_db_session():
            return temp_db
        monkeypatch.setattr('automagik.cli.commands.flows.get_db_session', mock_get_db_session)

        # Run the flows list command
        result = runner.invoke(flows, ['list'])
        assert result.exit_code == 0
        assert "Test Flow" in result.output
        
    def test_schedules_list(self, runner, temp_db, sample_schedule):
        """Test listing schedules from the database."""
        # Mock the get_db_session to return our temp_db
        with patch('automagik.cli.commands.schedules.get_db_session', return_value=temp_db):
            result = runner.invoke(schedules, ['list'])
            assert result.exit_code == 0
            assert "interval" in result.output
            assert "1m" in result.output
    
    def test_schedule_create(self, runner, temp_db, sample_flow, monkeypatch):
        """Test creating a schedule."""
        # Clear existing schedules and flows
        temp_db.query(Schedule).delete()
        temp_db.query(FlowDB).delete()
        temp_db.commit()

        # Create a test flow first
        flow_id = uuid.uuid4()
        test_flow = FlowDB(
            id=flow_id,
            name="Test Flow",
            description="A test flow",
            data={"nodes": [], "edges": []},
            source="langflow",
            source_id="test-flow-1",
            flow_version=1,
            input_component="test-input",
            output_component="test-output"
        )
        temp_db.add(test_flow)
        temp_db.commit()
        temp_db.refresh(test_flow)

        # Mock the get_db_session to return our temp_db
        def mock_get_db_session():
            return temp_db
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', mock_get_db_session)

        # Run the schedule create command
        result = runner.invoke(schedules, ['create', str(flow_id), '--type', 'interval', '--expr', '5m', '--input', '{}'])
        assert result.exit_code == 0

        # Verify the schedule was created
        schedule = temp_db.query(Schedule).first()
        assert schedule is not None
        assert schedule.flow_id == flow_id
        assert schedule.schedule_type == "interval"
        assert schedule.schedule_expr == "5m"
    
    def test_flow_sync(self, runner, temp_db, monkeypatch):
        """Test syncing flows to the database."""
        # Mock environment variables
        monkeypatch.setenv('LANGFLOW_API_URL', 'http://test.com')
        monkeypatch.setenv('LANGFLOW_API_KEY', 'test-key')

        # Mock the LangFlow client
        def mock_get_flows():
            return [
                {
                    'id': 'flow1',
                    'name': 'Flow 1',
                    'description': 'Test flow 1',
                    'data': {'nodes': [], 'edges': []},
                    'source': 'langflow',
                    'source_id': 'flow1'
                },
                {
                    'id': 'flow2',
                    'name': 'Flow 2',
                    'description': 'Test flow 2',
                    'data': {'nodes': [], 'edges': []},
                    'source': 'langflow',
                    'source_id': 'flow2'
                }
            ]
        
        def mock_get_flow(flow_id):
            flows = {
                'flow1': {
                    'id': 'flow1',
                    'name': 'Flow 1',
                    'description': 'Test flow 1',
                    'data': {'nodes': [], 'edges': []},
                    'source': 'langflow',
                    'source_id': 'flow1'
                },
                'flow2': {
                    'id': 'flow2',
                    'name': 'Flow 2',
                    'description': 'Test flow 2',
                    'data': {'nodes': [], 'edges': []},
                    'source': 'langflow',
                    'source_id': 'flow2'
                }
            }
            return flows.get(flow_id)

        def mock_get_db_session():
            return temp_db

        # Mock the flow manager
        class MockFlowManager:
            def __init__(self, *args, **kwargs):
                pass

            def get_available_flows(self):
                return [
                    {
                        'id': 'flow1',
                        'name': 'Flow 1',
                        'description': 'Test flow 1',
                        'data': {'nodes': [], 'edges': []},
                        'source': 'langflow',
                        'source_id': 'flow1'
                    },
                    {
                        'id': 'flow2',
                        'name': 'Flow 2',
                        'description': 'Test flow 2',
                        'data': {'nodes': [], 'edges': []},
                        'source': 'langflow',
                        'source_id': 'flow2'
                    }
                ]

            def get_flow_details(self, flow_id):
                flows = {
                    'flow1': {
                        'id': 'flow1',
                        'name': 'Flow 1',
                        'description': 'Test flow 1',
                        'data': {'nodes': [], 'edges': []},
                        'source': 'langflow',
                        'source_id': 'flow1'
                    },
                    'flow2': {
                        'id': 'flow2',
                        'name': 'Flow 2',
                        'description': 'Test flow 2',
                        'data': {'nodes': [], 'edges': []},
                        'source': 'langflow',
                        'source_id': 'flow2'
                    }
                }
                return flows.get(flow_id)

            def sync_flow(self, flow_data):
                flow = FlowDB(
                    id=uuid.uuid4(),
                    name=flow_data['name'],
                    description=flow_data['description'],
                    data=flow_data['data'],
                    source=flow_data['source'],
                    source_id=flow_data['source_id']
                )
                temp_db.add(flow)
                temp_db.commit()
                return flow.id

        monkeypatch.setattr('automagik.cli.commands.flows.get_db_session', mock_get_db_session)
        monkeypatch.setattr('automagik.cli.commands.flows.FlowManager', MockFlowManager)

        # Run the sync command with testing flag
        result = runner.invoke(flows, ['sync'], obj={'testing': True})
        assert result.exit_code == 0

        # Verify the flows were synced
        flows_in_db = temp_db.query(FlowDB).all()
        assert len(flows_in_db) == 2
        assert any(f.name == 'Flow 1' for f in flows_in_db)
        assert any(f.name == 'Flow 2' for f in flows_in_db)