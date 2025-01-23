# Common Development Patterns

## Development Environment

### Virtual Environment
Always use the virtual environment when working with AutoMagik:

```bash
# Activate virtual environment
source .venv/bin/activate

# Deactivate when done
deactivate
```

### Running Tests
Common test patterns:

```bash
# Run all tests with coverage
source .venv/bin/activate && pytest --cov=automagik

# Run specific test file
source .venv/bin/activate && pytest tests/test_integration.py -v

# Run specific test class
source .venv/bin/activate && pytest tests/test_integration.py::TestIntegration -v

# Run specific test method
source .venv/bin/activate && pytest tests/test_integration.py::TestIntegration::test_flow_sync -v

# Run tests with debug logging
AUTOMAGIK_LOG_LEVEL=DEBUG pytest tests/test_integration.py -v
```

### Database Operations
Common database patterns:

```bash
# Reset test database
source .venv/bin/activate && python -m automagik.core.database.reset_db

# Run migrations
source .venv/bin/activate && alembic upgrade head

# Create new migration
source .venv/bin/activate && alembic revision -m "description"
```

### Flow Management
Common flow operations:

```bash
# Sync flows with debug logging
AUTOMAGIK_LOG_LEVEL=DEBUG automagik flows sync

# List flows with JSON output
automagik flows list --format json

# Test flow with specific input
automagik flows test <flow-id> --input '{"key": "value"}'
```

### Schedule Management
Common scheduling patterns:

```bash
# Create schedule with retry policy
automagik schedules create --flow-id <id> --cron "*/5 * * * *" --retries 3

# List active schedules
automagik schedules list --status active

# Pause all schedules
automagik schedules pause-all
```

### Task Monitoring
Common monitoring patterns:

```bash
# Watch task logs in real-time
automagik tasks logs <task-id> --follow

# Get task status with full details
automagik tasks status <task-id> --verbose

# List failed tasks from last hour
automagik tasks list --status failed --since 1h
```

## API Development

### Testing API Endpoints
Common API test patterns:

```bash
# Test with curl
curl -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/flows

# Test with httpie (more readable)
http :8000/api/v1/flows X-API-Key:$AUTOMAGIK_API_KEY

# Test with debug logging
AUTOMAGIK_LOG_LEVEL=DEBUG uvicorn automagik.api.main:app --reload
```

### API Documentation
Access API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Debugging

### Common Debug Patterns

1. Enable debug logging:
```bash
export AUTOMAGIK_LOG_LEVEL=DEBUG
```

2. Use pdb in tests:
```python
breakpoint()  # Add this line where you want to break
```

3. Debug database queries:
```bash
export AUTOMAGIK_SQL_ECHO=true
```

### Log Locations

- Application logs: `/var/log/automagik/app.log`
- Task logs: `/var/log/automagik/tasks/`
- API logs: `/var/log/automagik/api.log`

## Common Issues and Solutions

1. **Flow Sync Fails**
   ```bash
   # Check LangFlow API connectivity
   curl -v -H "X-API-Key: $LANGFLOW_API_KEY" $LANGFLOW_API_URL/health
   
   # Verify flow format
   automagik flows inspect <flow-id> --format json
   ```

2. **Schedule Not Running**
   ```bash
   # Check Celery worker
   celery -A automagik.core.celery_app status
   
   # Verify schedule
   automagik schedules inspect <schedule-id>
   ```

3. **Task Failures**
   ```bash
   # Get detailed error
   automagik tasks logs <task-id> --error-only
   
   # Check component status
   automagik flows validate <flow-id>
   ```
