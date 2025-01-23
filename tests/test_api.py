import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import uuid

from automagik.api.main import app
from automagik.core.database.models import FlowDB, Schedule, Task
from automagik.core.database.session import get_db_session

client = TestClient(app)

# Test data
TEST_API_KEY = "namastex-888"
HEADERS = {"X-API-Key": TEST_API_KEY}

# Sample data for testing
SAMPLE_FLOW_ID = str(uuid.uuid4())
SAMPLE_SCHEDULE_ID = str(uuid.uuid4())
SAMPLE_TASK_ID = str(uuid.uuid4())

@pytest.fixture
def db_session():
    """Get a database session for testing."""
    with get_db_session() as session:
        yield session

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_list_flows():
    """Test listing flows endpoint."""
    response = client.get("/flows", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "flows" in data
    assert isinstance(data["flows"], list)
    
    # Validate flow structure if any flows exist
    if data["flows"]:
        flow = data["flows"][0]
        assert "id" in flow
        assert "name" in flow
        assert "description" in flow
        assert "source" in flow
        assert "source_id" in flow
        assert "data" in flow
        assert "created_at" in flow
        assert "updated_at" in flow
        assert "tags" in flow

def test_get_flow():
    """Test getting a specific flow endpoint."""
    # First get list of flows
    response = client.get("/flows", headers=HEADERS)
    assert response.status_code == 200
    flows = response.json()["flows"]
    
    if flows:
        # Test getting an existing flow
        flow_id = flows[0]["id"]
        response = client.get(f"/flows/{flow_id}", headers=HEADERS)
        assert response.status_code == 200
        flow = response.json()
        assert flow["id"] == flow_id
    
    # Test getting a non-existent flow
    response = client.get(f"/flows/{uuid.uuid4()}", headers=HEADERS)
    assert response.status_code == 404

def test_list_schedules():
    """Test listing schedules endpoint."""
    response = client.get("/schedules", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "schedules" in data
    assert isinstance(data["schedules"], list)
    
    # Validate schedule structure if any schedules exist
    if data["schedules"]:
        schedule = data["schedules"][0]
        assert "id" in schedule
        assert "flow_id" in schedule
        assert "schedule_type" in schedule
        assert "schedule_expr" in schedule
        assert "flow_params" in schedule
        assert "status" in schedule
        assert "next_run_at" in schedule
        assert "created_at" in schedule
        assert "updated_at" in schedule

def test_get_schedule():
    """Test getting a specific schedule endpoint."""
    # First get list of schedules
    response = client.get("/schedules", headers=HEADERS)
    assert response.status_code == 200
    schedules = response.json()["schedules"]
    
    if schedules:
        # Test getting an existing schedule
        schedule_id = schedules[0]["id"]
        response = client.get(f"/schedules/{schedule_id}", headers=HEADERS)
        assert response.status_code == 200
        schedule = response.json()
        assert schedule["id"] == schedule_id
    
    # Test getting a non-existent schedule
    response = client.get(f"/schedules/{uuid.uuid4()}", headers=HEADERS)
    assert response.status_code == 404

def test_list_tasks():
    """Test listing tasks endpoint."""
    response = client.get("/tasks", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
    
    # Validate task structure if any tasks exist
    if data["tasks"]:
        task = data["tasks"][0]
        assert "id" in task
        assert "flow_id" in task
        assert "status" in task
        assert "input_data" in task
        assert "created_at" in task
        assert "updated_at" in task

def test_get_task():
    """Test getting a specific task endpoint."""
    # First get list of tasks
    response = client.get("/tasks", headers=HEADERS)
    assert response.status_code == 200
    tasks = response.json()["tasks"]
    
    if tasks:
        # Test getting an existing task
        task_id = tasks[0]["id"]
        response = client.get(f"/tasks/{task_id}", headers=HEADERS)
        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
    
    # Test getting a non-existent task
    response = client.get(f"/tasks/{uuid.uuid4()}", headers=HEADERS)
    assert response.status_code == 404

def test_api_key_validation():
    """Test API key validation."""
    # Test without API key
    response = client.get("/flows")
    assert response.status_code == 401
    
    # Test with invalid API key
    response = client.get("/flows", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 401
    
    # Test with valid API key
    response = client.get("/flows", headers=HEADERS)
    assert response.status_code == 200

def test_error_handling():
    """Test error handling."""
    # Test 404 error
    response = client.get("/nonexistent-endpoint", headers=HEADERS)
    assert response.status_code == 404
    
    # Test invalid UUID format
    response = client.get("/flows/not-a-uuid", headers=HEADERS)
    assert response.status_code in [400, 404, 422]  # Depending on how we handle invalid UUIDs
