# Development Workflow

## Environment Setup

Always ensure your environment is properly activated:
```bash
# Activate environment
source .venv/bin/activate

# Verify Python interpreter
which python  # Should point to .venv/bin/python

# Check installed packages
pip list | grep automagik
```

## Common Development Commands

### Testing

```bash
# Run all tests with coverage and output in pretty format
source .venv/bin/activate && pytest --cov=automagik -v | grep -v "no tests ran"

# Run specific test with debug output
AUTOMAGIK_LOG_LEVEL=DEBUG pytest tests/test_integration.py::TestIntegration::test_flow_sync -v

# Run tests and output coverage report in HTML
pytest --cov=automagik --cov-report=html

# Watch tests (using ptw)
ptw tests/ -- -v
```

### API Development

```bash
# Test API endpoints with formatted JSON output
curl -s -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/flows | jq .

# Filter specific fields from API response
curl -s -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/flows | jq '.[] | {id, name}'

# Test flow sync with debug output
curl -v -H "X-API-Key: $LANGFLOW_API_KEY" "http://192.168.112.132:80/api/v1/flows/" | jq .

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

### Database Operations

```bash
# Export query results to JSON
source .venv/bin/activate && python -c "
from automagik.core.database import get_session
session = get_session()
result = session.execute('SELECT * FROM flows').fetchall()
import json
print(json.dumps([dict(r) for r in result], default=str))
" | jq .

# Monitor database queries
AUTOMAGIK_SQL_ECHO=true automagik flows list

# Backup database
pg_dump $DATABASE_URL > backup.sql
```

## Debugging Tips

### Using Python Debugger

```python
# Add this in your code
import pdb; pdb.set_trace()
# Or
breakpoint()

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
```

### Network Debugging

```bash
# Test LangFlow API connectivity
curl -v -H "X-API-Key: $LANGFLOW_API_KEY" http://192.168.112.132:80/health

# Monitor API requests
sudo tcpdump -i any -n -A "port 8000" | grep -A 10 "POST /api"

# Check API latency
for i in {1..5}; do 
  curl -w "%{time_total}\n" -s -o /dev/null -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/health
done
```

### Memory Profiling

```bash
# Run with memory profiling
mprof run automagik flows sync
mprof plot  # View memory usage graph

# Profile specific test
mprof run pytest tests/test_integration.py::TestIntegration::test_flow_sync
```

## LLM-Friendly Documentation

### Using ai-digest

`ai-digest` is a tool that creates LLM-friendly documentation of your codebase. It's particularly useful when you want to:
- Generate comprehensive codebase summaries
- Create context for LLM-based code analysis
- Document code for AI pair programming

```bash
# Install ai-digest
npm install -g ai-digest

# Generate codebase documentation
npx ai-digest

# The output will be in codebase.md
```

### Configuring ai-digest

Create `.aidigestignore` to customize what files to include/exclude:
```bash
# Exclude specific directories
docker/
postgres_data/
redis_data/

# Exclude file types
*.pyc
*.pyo
*.pyd
*.so
*.egg
*.egg-info

# Include only specific files
!automagik/core/**/*.py
!automagik/cli/**/*.py
!automagik/api/**/*.py
```

### Best Practices

1. Run before major changes:
```bash
# Generate baseline documentation
npx ai-digest > codebase-baseline.md
```

2. Run after implementing features:
```bash
# Generate updated documentation
npx ai-digest > codebase-updated.md

# Compare changes
diff codebase-baseline.md codebase-updated.md
```

3. Include in documentation workflow:
```bash
# Update all documentation
source .venv/bin/activate
pytest --doctest-modules
sphinx-build -b html docs/ docs/_build/html
npx ai-digest
```

## Environment Variables

Create a `.env.debug` file for debugging:
```bash
AUTOMAGIK_LOG_LEVEL=DEBUG
AUTOMAGIK_SQL_ECHO=true
PYTHONBREAKPOINT=ipdb.set_trace  # Use ipdb instead of pdb
```

Then source it when needed:
```bash
source .env.debug && automagik flows sync
```

## Git Workflow

```bash
# Check changed files
git status -s

# View recent changes
git log --oneline --graph | head -n 10

# Search in codebase
git grep -n "flow_sync"

# Show file history
git log -p automagik/core/services/flow_manager.py
```

## Performance Tips

1. Use `jq` for JSON parsing:
```bash
# Instead of
automagik flows list

# Use
automagik flows list --format json | jq '.[] | {id, name, status}'
```

2. Use grep for filtering:
```bash
# Instead of
pytest tests/

# Use
pytest tests/ | grep -v "no tests ran"
```

3. Use tee for logging:
```bash
# Log command output while viewing it
automagik flows sync 2>&1 | tee sync.log
```

4. Use watch for monitoring:
```bash
# Monitor flow status
watch -n 5 'automagik flows list --format json | jq ".[] | {id, status}"'
```
