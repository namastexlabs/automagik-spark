import os
import uuid
import pytest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from automagik.cli.commands.flows import flows
from automagik.cli.commands.schedules import schedules
from automagik.cli.commands.run import run
from automagik.core.database.models import Base, FlowDB, Schedule
from automagik.core.database import get_db_session

@pytest.fixture
def temp_db(monkeypatch):
    """Create a temporary SQLite database for testing."""
    # Create a temporary file to store the SQLite database
    temp_db_file = tempfile.NamedTemporaryFile(delete=False)
    db_url = f"sqlite:///{temp_db_file.name}"
    
    # Create the database and tables
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Patch the get_db_session to use our temporary database
    monkeypatch.setattr('automagik.core.database.get_db_session', lambda: session)
    
    yield session
    
    # Cleanup
    session.close()
    temp_db_file.close()
    os.unlink(temp_db_file.name)

@pytest.fixture
def sample_flow(temp_db):
    """Create a sample flow in the database."""
    flow = FlowDB(
        id=uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799"),
        name="Test Flow",
        description="A test flow",
        data={"nodes": [], "edges": []},
        source="langflow",
        source_id="test_flow",
        flow_version=1,
        input_component="test_input",
        output_component="test_output"
    )
    temp_db.add(flow)
    temp_db.commit()
    return flow

@pytest.fixture
def sample_schedule(temp_db, sample_flow):
    """Create a sample schedule in the database."""
    schedule = Schedule(
        id=uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799"),
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="1m",
        flow_params={"test": "data"},
        status="active"
    )
    temp_db.add(schedule)
    temp_db.commit()
    return schedule

@pytest.fixture
def runner():
    """Create a Click CLI runner."""
    from click.testing import CliRunner
    return CliRunner()

class TestIntegration:
    """Integration tests using a real SQLite database."""
    
    def test_flows_list(self, runner, temp_db, sample_flow, monkeypatch):
        """Test listing flows from the database."""
        # Mock the database session to return our test flow
        test_id = uuid.uuid4()
        test_flow = FlowDB(
            id=test_id,
            name="Test Flow",
            description="Test Description",
            data={"nodes": [], "edges": []},
            source="test",
            source_id="test-source-id",
            folder_name="Test Folder",
            input_component=True,
            output_component=True,
            flow_version=1
        )

        # Clear existing flows and add our test flow
        temp_db.query(FlowDB).delete()
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
        assert "Test Folder" in result.output
        
    def test_schedules_list(self, runner, temp_db, sample_schedule):
        """Test listing schedules from the database."""
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
            description="Test Description",
            data={"nodes": [], "edges": []},
            source="test",
            source_id="test-source-id",
            input_component="test_input",
            output_component="test_output",
            flow_version=1
        )
        temp_db.add(test_flow)
        temp_db.commit()

        # Mock the database session
        def mock_get_db_session():
            return temp_db
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', mock_get_db_session)

        # Create a schedule using the CLI in interactive mode
        # Input sequence:
        # 0 - Select first flow
        # 0 - Select interval schedule type
        # 1h - Set interval to 1 hour
        # y - Yes to set input value
        # test - The input value
        result = runner.invoke(schedules, ['create'], input='0\n0\n1h\ny\ntest\n')
        
        assert result.exit_code == 0
        assert "Schedule created successfully!" in result.output
        
        # Verify schedule was created
        schedule = temp_db.query(Schedule).first()
        assert schedule is not None
        assert schedule.flow_id == flow_id
        assert schedule.schedule_type == "interval"
        assert schedule.schedule_expr == "1h"
        assert schedule.flow_params == {"input": "test"}
        
    def test_flow_sync(self, runner, temp_db, monkeypatch):
        """Test syncing flows to the database."""
        # Mock environment variables
        monkeypatch.setenv('LANGFLOW_API_URL', 'http://test.com')
        monkeypatch.setenv('LANGFLOW_API_KEY', 'test_key')

        # First, ensure the database is empty
        temp_db.query(FlowDB).delete()
        temp_db.commit()

        # Mock LangflowClient methods
        test_id = uuid.uuid4()

        def mock_get_flows():
            return [{
                'id': str(test_id),
                'name': 'Test Flow',
                'description': 'A test flow',
                'data': {'nodes': [], 'edges': []},
                'folder': 'test-folder'
            }]

        def mock_get_flow(flow_id):
            return {
                'id': str(test_id),
                'name': 'Test Flow',
                'description': 'A test flow',
                'data': {'nodes': [], 'edges': []},
                'folder': 'test-folder'
            }

        # Mock the get_db_session to return our temp_db
        def mock_get_db_session():
            return temp_db
        monkeypatch.setattr('automagik.cli.commands.flows.get_db_session', mock_get_db_session)
        monkeypatch.setattr('automagik.core.services.flow_manager.get_db_session', mock_get_db_session)

        # Mock FlowManager
        from automagik.core.services.flow_manager import FlowManager
        class MockFlowManager(FlowManager):
            def get_available_flows(self):
                return [{
                    'id': str(test_id),
                    'name': 'Test Flow',
                    'description': 'A test flow',
                    'data': {'nodes': [], 'edges': []},
                    'folder': 'test-folder'
                }]

            def get_flow_details(self, flow_id):
                return {
                    'id': str(test_id),
                    'name': 'Test Flow',
                    'description': 'A test flow',
                    'data': {'nodes': [], 'edges': []},
                    'folder': 'test-folder'
                }

        def mock_flow_manager(*args, **kwargs):
            return MockFlowManager(temp_db, 'http://test.com', 'test_key')

        monkeypatch.setattr('automagik.cli.commands.flows.FlowManager', mock_flow_manager)

        # Run the sync command with input '0' to select the first flow
        result = runner.invoke(flows, ['sync'], input='0\n')
        assert result.exit_code == 0

        # Verify that the flow was synced
        synced_flows = temp_db.query(FlowDB).all()
        assert len(synced_flows) == 1
        synced_flow = synced_flows[0]
        assert synced_flow.name == 'Test Flow'
        assert synced_flow.description == 'A test flow'