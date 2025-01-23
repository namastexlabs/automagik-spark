import os
import uuid
import pytest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from automagik.core.database.models import Base, FlowDB, Schedule
from automagik.cli.commands.flows import flows
from automagik.cli.commands.run import run
from automagik.cli.commands.schedules import schedules
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
    
    def test_flows_list(self, runner, temp_db, sample_flow):
        """Test listing flows from the database."""
        result = runner.invoke(flows, ['list'])
        assert result.exit_code == 0
        assert "Test Flow" in result.output
        
    def test_schedules_list(self, runner, temp_db, sample_schedule):
        """Test listing schedules from the database."""
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert "interval" in result.output
        assert "1m" in result.output
        
    def test_schedule_create(self, runner, temp_db, sample_flow):
        """Test creating a schedule in the database."""
        result = runner.invoke(schedules, ['create'], input='3cf82804-41b2-4731-9306-f77e17193799\ninterval\n1m\n{"test":"input"}\n')
        assert result.exit_code == 0
        
        # Verify schedule was created
        schedule = temp_db.query(Schedule).first()
        assert schedule is not None
        assert schedule.schedule_type == "interval"
        assert schedule.schedule_expr == "1m"
        
    def test_flow_sync(self, runner, temp_db, monkeypatch):
        """Test syncing flows to the database."""
        # Mock environment variables
        monkeypatch.setenv('LANGFLOW_API_URL', 'http://test.com')
        monkeypatch.setenv('LANGFLOW_API_KEY', 'test_key')

        # First, ensure the database is empty
        temp_db.query(FlowDB).delete()
        temp_db.commit()
        
        # Mock FlowSync methods
        def mock_get_remote_flows():
            return [{
                'id': '123',
                'name': 'Test Flow',
                'description': 'A test flow'
            }]
            
        def mock_get_flow_details(flow_id):
            return {
                'id': flow_id,
                'name': 'Test Flow',
                'description': 'A test flow',
                'data': {
                    'nodes': [],
                    'edges': []
                }
            }
            
        from automagik.core.services.flow_sync import FlowSync
        monkeypatch.setattr(FlowSync, 'get_remote_flows', mock_get_remote_flows)
        monkeypatch.setattr(FlowSync, 'get_flow_details', mock_get_flow_details)
        
        result = runner.invoke(flows, ['sync'])
        assert result.exit_code == 0
        
        # Verify flows were synced
        flows_count = temp_db.query(FlowDB).count()
        assert flows_count > 0