# Common Development Patterns

## Flow Management

### Flow Synchronization
```bash
# Basic sync
automagik flows sync

# Sync with debug logging
AUTOMAGIK_LOG_LEVEL=DEBUG automagik flows sync

# Sync specific flow
automagik flows sync --flow-id <id>

# Force sync (ignore cache)
automagik flows sync --force
```

### Flow Analysis
```bash
# Analyze flow structure
automagik flows analyze <flow-id>

# Export flow diagram
automagik flows export-diagram <flow-id>

# Validate flow
automagik flows validate <flow-id>

# List flow dependencies
automagik flows deps <flow-id>
```

### Flow Testing
```bash
# Test with default input
automagik flows test <flow-id>

# Test with custom input
automagik flows test <flow-id> --input '{"key": "value"}'

# Test with debug output
AUTOMAGIK_LOG_LEVEL=DEBUG automagik flows test <flow-id>

# Test and save output
automagik flows test <flow-id> --save-output output.json
```

## Task Management

### Task Creation
```bash
# Create basic task
automagik tasks create --flow-id <id>

# Create with input
automagik tasks create --flow-id <id> --input '{"key": "value"}'

# Create with retries
automagik tasks create --flow-id <id> --retries 3

# Create with timeout
automagik tasks create --flow-id <id> --timeout 300
```

### Task Monitoring
```bash
# View task status
automagik tasks status <task-id>

# Follow task logs
automagik tasks logs <task-id> --follow

# View task output
automagik tasks output <task-id>

# List recent tasks
automagik tasks list --limit 10
```

### Task Management
```bash
# Cancel task
automagik tasks cancel <task-id>

# Retry failed task
automagik tasks retry <task-id>

# Clean up old tasks
automagik tasks cleanup --older-than 7d

# Export task results
automagik tasks export <task-id> --format json
```

## Schedule Management

### Schedule Creation
```bash
# Create basic schedule
automagik schedules create --flow-id <id> --cron "*/5 * * * *"

# Create with retries
automagik schedules create --flow-id <id> --cron "0 * * * *" --retries 3

# Create with timeout
automagik schedules create --flow-id <id> --cron "0 0 * * *" --timeout 600

# Create with input
automagik schedules create --flow-id <id> --cron "0 12 * * *" --input '{"key": "value"}'
```

### Schedule Management
```bash
# List schedules
automagik schedules list

# View schedule details
automagik schedules get <schedule-id>

# Pause schedule
automagik schedules pause <schedule-id>

# Resume schedule
automagik schedules resume <schedule-id>
```

## API Usage

### Authentication
```bash
# Set API key
export AUTOMAGIK_API_KEY="your-api-key"

# Test authentication
curl -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/health

# Refresh API key
automagik api refresh-key
```

### Flow Operations
```bash
# List flows
curl -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/flows

# Get flow details
curl -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/flows/<flow-id>

# Create task
curl -X POST -H "X-API-Key: $AUTOMAGIK_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"input": {"key": "value"}}' \
     http://localhost:8000/api/v1/flows/<flow-id>/tasks
```

### Task Operations
```bash
# Get task status
curl -H "X-API-Key: $AUTOMAGIK_API_KEY" \
     http://localhost:8000/api/v1/tasks/<task-id>

# Get task logs
curl -H "X-API-Key: $AUTOMAGIK_API_KEY" \
     http://localhost:8000/api/v1/tasks/<task-id>/logs

# Cancel task
curl -X POST -H "X-API-Key: $AUTOMAGIK_API_KEY" \
     http://localhost:8000/api/v1/tasks/<task-id>/cancel
```

## Common Issues and Solutions

### Flow Sync Issues
1. **API Connection Failed**
   ```bash
   # Check API health
   curl -v http://localhost:8000/health
   
   # Verify API key
   curl -v -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/health
   ```

2. **Flow Validation Failed**
   ```bash
   # Check flow structure
   automagik flows validate <flow-id>
   
   # View flow details
   automagik flows get <flow-id> --format json
   ```

### Task Execution Issues
1. **Task Timeout**
   ```bash
   # Check task logs
   automagik tasks logs <task-id>
   
   # View resource usage
   automagik tasks stats <task-id>
   ```

2. **Task Failed**
   ```bash
   # View error details
   automagik tasks logs <task-id> --level ERROR
   
   # Check flow status
   automagik flows validate <flow-id>
   ```

### Schedule Issues
1. **Schedule Not Running**
   ```bash
   # Check schedule status
   automagik schedules get <schedule-id>
   
   # Verify cron expression
   automagik schedules validate-cron "*/5 * * * *"
   ```

2. **Schedule Failed**
   ```bash
   # View schedule history
   automagik schedules history <schedule-id>
   
   # Check schedule logs
   automagik schedules logs <schedule-id>
   ```

## Performance Optimization

### Database Optimization
```bash
# Analyze query performance
AUTOMAGIK_SQL_ECHO=true automagik flows list

# Clean up old data
automagik cleanup --older-than 30d

# Optimize database
automagik db optimize
```

### Memory Usage
```bash
# Monitor memory usage
mprof run automagik flows sync
mprof plot

# Clean up cache
automagik cache clear
```

### API Performance
```bash
# Check API latency
for i in {1..5}; do
  curl -w "%{time_total}\n" -s -o /dev/null \
    -H "X-API-Key: $AUTOMAGIK_API_KEY" \
    http://localhost:8000/api/v1/health
done

# Use batch operations
curl -X POST -H "X-API-Key: $AUTOMAGIK_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"flow_ids": ["id1", "id2"]}' \
     http://localhost:8000/api/v1/flows/batch/sync
```
