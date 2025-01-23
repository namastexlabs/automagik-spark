# Development Workflow

## Environment Setup

### Prerequisites
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3.8-venv postgresql redis-server

# Clone repository
git clone https://github.com/yourusername/automagik.git
cd automagik
```

### Virtual Environment
Always use the virtual environment when working with AutoMagik:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify Python interpreter
which python  # Should point to .venv/bin/python

# Check installed packages
pip list | grep automagik
```

### Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit environment variables
nano .env

# Verify configuration
source .env
echo $AUTOMAGIK_LOG_LEVEL  # Should show configured level
```

## Development Tools

### Database Management
```bash
# Initialize database
alembic upgrade head

# Create new migration
alembic revision -m "description"

# Reset test database
python -m automagik.core.database.reset_db
```

### Docker Development
```bash
# Build and start all services
docker-compose up -d

# Build specific service
docker-compose build api

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Testing

```bash
# Run all tests with coverage and output in pretty format
pytest --cov=automagik -v | grep -v "no tests ran"

# Run specific test with debug output
AUTOMAGIK_LOG_LEVEL=DEBUG pytest tests/test_integration.py::TestIntegration::test_flow_sync -v

# Run tests and output coverage report in HTML
pytest --cov=automagik --cov-report=html

# Watch tests (using ptw)
ptw tests/ -- -v

# Run specific test suite
pytest tests/test_integration.py -v
```

### API Development

```bash
# Start API in development mode
uvicorn automagik.api.main:app --reload --log-level debug

# Test API endpoints with formatted JSON output
curl -s -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/flows | jq .

# Filter specific fields from API response
curl -s -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/flows | jq '.[] | {id, name}'

# Test flow sync with debug output
curl -v -H "X-API-Key: $LANGFLOW_API_KEY" "http://localhost:80/api/v1/flows/" | jq .

# Monitor API logs in real-time
tail -f /var/log/automagik/api.log | jq .
```

### Flow Management

```bash
# List flows with formatted output
automagik flows list --format json | jq .

# Get specific flow details
automagik flows get <flow-id> | jq '.data'

# Sync flows with debug logging
AUTOMAGIK_LOG_LEVEL=DEBUG automagik flows sync 2>&1 | tee flow-sync.log

# Analyze flow components
automagik flows analyze <flow-id> | jq '.components'
```

### Task Management

```bash
# Create new task
automagik tasks create --flow-id <id> --input '{"key": "value"}'

# List recent tasks
automagik tasks list --limit 10

# View task logs
automagik tasks logs <task-id> --follow

# Cancel running task
automagik tasks cancel <task-id>
```

### Schedule Management

```bash
# Create schedule with retry policy
automagik schedules create --flow-id <id> --cron "*/5 * * * *" --retries 3

# List active schedules
automagik schedules list --status active

# Pause specific schedule
automagik schedules pause <schedule-id>

# Resume schedule
automagik schedules resume <schedule-id>
```

## Debugging

### Using Python Debugger

```python
# Add breakpoint in code
breakpoint()
# Or
import pdb; pdb.set_trace()

# Common pdb commands:
# n (next line)
# s (step into)
# c (continue)
# p variable (print variable)
# ll (list surrounding code)
```

### Log Analysis

```bash
# Follow logs with jq formatting
tail -f /var/log/automagik/app.log | jq .

# Filter error logs
grep -i error /var/log/automagik/app.log | jq .

# Search for specific flow ID in logs
grep "flow-id" /var/log/automagik/app.log | jq 'select(.flow_id == "your-flow-id")'

# Monitor task logs
tail -f /var/log/automagik/tasks/*.log
```

### Performance Profiling

```bash
# Install profiling tools
pip install memory_profiler line_profiler

# Profile memory usage
mprof run automagik flows sync
mprof plot

# Profile specific function
@profile
def your_function():
    pass

# Run with line profiler
kernprof -l -v script.py
```

## Best Practices

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Write docstrings for all functions
   - Keep functions focused and small

2. **Testing**
   - Write tests for new features
   - Maintain high coverage
   - Use appropriate fixtures
   - Mock external dependencies

3. **Git Workflow**
   - Create feature branches
   - Write descriptive commit messages
   - Keep commits focused
   - Rebase before merging

4. **Documentation**
   - Update docs with code changes
   - Include examples
   - Document configuration
   - Explain breaking changes

5. **Error Handling**
   - Use custom exceptions
   - Log errors appropriately
   - Provide helpful error messages
   - Handle edge cases

6. **Security**
   - Never commit secrets
   - Use environment variables
   - Validate input data
   - Follow security best practices
