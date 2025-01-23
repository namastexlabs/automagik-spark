# AutoMagik Project Documentation

AutoMagik is a powerful CLI tool designed to manage and schedule LangFlow workflows. It provides a seamless interface for syncing, scheduling, and monitoring workflow executions.

## Getting Started

1. Read [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) for practical development tips and patterns
2. Check [COMMON_PATTERNS.md](COMMON_PATTERNS.md) for common use cases and solutions
3. Set up your development environment following [/docs/DEVELOPMENT.md](/docs/DEVELOPMENT.md)
4. Review the architecture in [/docs/ARCHITECTURE.md](/docs/ARCHITECTURE.md)

## Project Structure

```
automagik/
├── api/                # FastAPI application
│   ├── dependencies.py # Dependency injection
│   ├── security.py    # API security
│   ├── schemas.py     # API schemas
│   └── main.py        # FastAPI app
├── cli/               # Click command-line interface
│   ├── commands/      # Command implementations
│   ├── models/        # CLI data models
│   ├── services/      # CLI services
│   └── utils/         # CLI utilities
├── core/              # Core business logic
│   ├── services/      # Main services
│   │   ├── flow_manager.py
│   │   ├── flow_analyzer.py
│   │   ├── flow_sync.py
│   │   ├── langflow_client.py
│   │   └── task_runner.py
│   ├── database/      # Database models and sessions
│   └── utils/         # Utility functions
├── alembic/           # Database migrations
├── scripts/           # Utility scripts
├── tests/             # Test suite
└── docs/              # Documentation
```

## Core Components

### Flow Management (`core/services/`)

1. **FlowManager**: Main interface for flow operations
   - Syncs flows with LangFlow server
   - Manages flow metadata and components
   - Handles flow versioning
   - Supports both string and dict data formats

2. **FlowAnalyzer**: Analyzes flow structure
   - Identifies input/output components
   - Maps component dependencies
   - Validates flow configurations
   - Extracts tweakable parameters

3. **FlowSync**: Handles LangFlow API communication
   - Fetches available flows
   - Retrieves flow details
   - Validates API responses
   - Handles different response formats

4. **LangflowClient**: Dedicated API client
   - Manages API authentication
   - Handles API requests/responses
   - Provides high-level API operations
   - Implements retry and error handling

5. **TaskRunner**: Manages task execution
   - Runs workflow tasks
   - Handles task logging
   - Manages task state
   - Processes task input/output

### API Components (`api/`)

1. **FastAPI Application**:
   - RESTful API endpoints
   - OpenAPI documentation
   - Request/response validation
   - Error handling

2. **Security**:
   - API key authentication
   - Role-based access control
   - Request validation
   - Security middleware

3. **Dependencies**:
   - Database session management
   - Service injection
   - Configuration management
   - Logging setup

### CLI Components (`cli/`)

1. **Command Structure**:
   - Flow management commands
   - Task scheduling commands
   - Monitoring commands
   - Configuration commands

2. **Services**:
   - Scheduler service
   - Flow sync service
   - Task management
   - Configuration management

## Development Environment

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (for task queue)
- Docker (optional)

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
alembic upgrade head
```

### Docker Support
```bash
# Build and run with Docker
docker-compose up -d

# Run specific service
docker-compose up api
```

## Testing Strategy

### Integration Tests
- Uses SQLite for ephemeral testing
- Mocks LangFlow API responses
- Tests flow sync and schedule creation
- Verifies database operations

### Unit Tests
- Tests individual components
- Validates core functionality
- Ensures data integrity
- Uses pytest fixtures

## Development Resources

### Command Line Tools
- `jq`: Essential for JSON parsing and API testing
- `curl`: Testing HTTP endpoints
- `watch`: Monitoring status changes
- `grep`: Filtering and searching
- `tee`: Logging while viewing output

### Environment Setup
```bash
# Activate environment and set debug mode
source .venv/bin/activate
source .env.debug  # See DEVELOPMENT_WORKFLOW.md for contents

# Verify setup
which python  # Should point to .venv/bin/python
echo $AUTOMAGIK_LOG_LEVEL  # Should be DEBUG
```

## Quick Development Commands
```bash
# Run tests with coverage
pytest --cov=automagik -v | grep -v "no tests ran"

# Test API with formatted output
curl -s -H "X-API-Key: $AUTOMAGIK_API_KEY" http://localhost:8000/api/v1/flows | jq .

# Monitor flow status
watch -n 5 'automagik flows list --format json | jq ".[] | {id, status}"'
```

## Common Development Tasks

See [COMMON_PATTERNS.md](COMMON_PATTERNS.md) for detailed examples of:
- Running tests
- Managing the development environment
- Debugging issues
- API testing
- Database operations
- Flow management
- Schedule management
- Task monitoring

## Troubleshooting

For common issues and solutions, refer to the "Common Issues and Solutions" section in [COMMON_PATTERNS.md](COMMON_PATTERNS.md).