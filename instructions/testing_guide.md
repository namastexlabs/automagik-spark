# Automagik Testing Guide

## Common Pitfalls and Solutions

### 1. SQLAlchemy AsyncMock Issues

#### Problem: Unawaited Coroutine Warnings
When using `AsyncMock` with SQLAlchemy, you might encounter warnings like:
```
RuntimeWarning: coroutine 'AsyncMockMixin._execute_mock_call' was never awaited
```

#### Solution:
Add these filters to your `pytest.ini`:
```ini
[pytest]
filterwarnings = 
    ignore::RuntimeWarning:sqlalchemy.*:
    ignore::RuntimeWarning:tests.*:
    ignore:coroutine 'AsyncMockMixin._execute_mock_call' was never awaited:RuntimeWarning
```

### 2. Mock Session Setup

#### Problem: Complex Query Results
Mocking SQLAlchemy's session methods can be tricky, especially with chained calls like `session.execute().scalars().all()`.

#### Solution:
Use this pattern for reliable mocking:
```python
# For single results
mock_result = MagicMock()
mock_result.scalar_one_or_none.return_value = your_mock_data
mock_session.execute.return_value = mock_result

# For multiple results
mock_result = MagicMock()
mock_result.scalars.return_value.all.return_value = [your_mock_data]
mock_session.execute.return_value = mock_result
```

### 3. UUID and Mock Objects

#### Problem: MagicMock Objects in UUID Fields
Using `MagicMock` for UUID fields can cause comparison issues and make tests unreliable.

#### Solution:
Always use real UUIDs in test data:
```python
from uuid import uuid4

# Create real UUIDs for test data
flow_id = uuid4()
flow = Flow(
    id=flow_id,
    source_id=str(uuid4()),
    # ... other fields
)
```

## Best Practices

### 1. Async Test Setup

```python
@pytest.mark.asyncio
async def test_async_function(session: AsyncSession):
    # Test setup
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = your_mock_data
    session.execute.return_value = mock_result

    # Run test
    result = await your_async_function(session)
    
    # Verify
    assert result is not None
    session.execute.assert_awaited_once()
```

### 2. Mock Session Classes

Create reusable mock session classes for common patterns:

```python
class MockSession:
    """Mock database session with async context manager support."""
    
    def __init__(self):
        self.execute = AsyncMock()
        self.commit = AsyncMock()
        self.rollback = AsyncMock()
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
```

### 3. Fixture Organization

Keep fixtures organized by scope and purpose:

```python
# conftest.py

@pytest.fixture
def sample_flow():
    """Base flow fixture for tests."""
    return Flow(
        id=uuid4(),
        name="test-flow",
        source="langflow",
        # ... minimal required fields
    )

@pytest.fixture
async def mock_session():
    """Session fixture with common mocks."""
    session = MockSession()
    yield session
```

### 4. Testing Worker Processes

When testing worker processes:
1. Mock process management functions
2. Use temporary files for PID and logs
3. Clean up resources after tests

```python
@pytest.fixture
def mock_pid_file(tmp_path):
    """Create a temporary PID file."""
    pid_file = tmp_path / "worker.pid"
    yield pid_file
    if pid_file.exists():
        pid_file.unlink()

def test_worker_start(mock_pid_file, caplog):
    # Test worker startup
    assert not mock_pid_file.exists()
    # ... start worker
    assert mock_pid_file.exists()
```

## Testing Patterns

### 1. Database Tests
- Use transaction rollback to keep tests isolated
- Mock database calls when testing business logic
- Use real database connections for integration tests

### 2. API Tests
- Use FastAPI's `TestClient`
- Mock external service calls
- Test both success and error cases

### 3. Worker Tests
- Mock process management
- Test both running and stopped states
- Verify proper cleanup

## Test Quality Guidelines

1. **Isolation**
   - Each test should be independent
   - Clean up resources in fixtures
   - Use fresh test data

2. **Coverage**
   - Test error conditions
   - Verify async call counts
   - Check cleanup operations

3. **Maintenance**
   - Use descriptive test names
   - Document complex fixtures
   - Keep mock data minimal

4. **Performance**
   - Use appropriate fixture scopes
   - Mock expensive operations
   - Clean up test resources

## Common Test Scenarios

### 1. Testing Schedules
```python
@pytest.mark.asyncio
async def test_process_schedules(session: AsyncSession):
    # Create test schedule
    schedule = Schedule(
        id=uuid4(),
        flow_id=uuid4(),
        status="active",
        schedule_type="interval",
        schedule_expr="1h"
    )
    
    # Mock session response
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [schedule]
    session.execute.return_value = mock_result
    
    # Run and verify
    await process_schedules(session)
    session.execute.assert_awaited_once()
```

### 2. Testing Tasks
```python
@pytest.mark.asyncio
async def test_retry_task(session: AsyncSession):
    # Create test task
    task = Task(
        id=uuid4(),
        flow_id=uuid4(),
        status="failed",
        retry_count=0
    )
    
    # Mock session
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = task
    session.execute.return_value = mock_result
    
    # Run and verify
    await retry_task(session, str(task.id))
    assert task.retry_count == 1
```

Remember: Tests should be reliable, maintainable, and provide value in catching bugs and regressions. Don't hesitate to refactor tests when they become difficult to maintain or understand.
