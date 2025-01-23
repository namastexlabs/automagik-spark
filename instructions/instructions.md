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
├── cli/                # Click command-line interface
├── core/               # Core business logic
│   ├── services/      # Main services
│   │   ├── flow_manager.py
│   │   ├── flow_analyzer.py
│   │   └── flow_sync.py
│   ├── database/      # Database models and sessions
│   └── utils/         # Utility functions
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

### Database Management (`core/database/`)

1. **Models**:
   - `FlowDB`: Flow metadata and configuration
   - `FlowComponent`: Flow component information
   - `Schedule`: Task scheduling information

2. **Session Management**:
   - SQLAlchemy session handling
   - SQLite for testing
   - PostgreSQL for production

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

### Quick Development Commands
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