# AutoMagik Project Documentation

AutoMagik is a powerful CLI tool designed to manage and schedule LangFlow workflows. It provides a seamless interface for syncing, scheduling, and monitoring workflow executions.

## Project Structure

```
automagik/
├── cli/                    # CLI implementation
│   └── automagik_cli/
│       ├── commands/      # CLI command modules
│       │   ├── flows.py
│       │   ├── schedules.py
│       │   └── tasks.py
│       └── cli.py         # Main CLI entry point
├── core/                  # Core business logic
│   ├── flows/            # Flow management
│   │   ├── flow_analyzer.py
│   │   ├── flow_sync.py
│   │   └── flow_manager.py
│   ├── database/         # Database management
│   │   ├── models.py
│   │   ├── session.py
│   │   └── base.py
│   └── scheduler/        # Task scheduling
│       ├── scheduler.py
│       ├── task_runner.py
│       └── exceptions.py
└── tests/                # Test suite
```

## Core Components

### Flow Management (`core/flows/`)

1. **FlowManager**: Main interface for flow operations
   - Syncs flows with LangFlow server
   - Manages flow metadata and components
   - Handles flow versioning

2. **FlowAnalyzer**: Analyzes flow structure
   - Identifies input/output components
   - Maps component dependencies
   - Validates flow configurations

3. **FlowSync**: Handles LangFlow API communication
   - Fetches available flows
   - Retrieves flow details
   - Validates API responses

### Database Management (`core/database/`)

1. **Models**:
   - `FlowDB`: Flow metadata and configuration
   - `FlowComponent`: Flow component information
   - `Task`: Task execution records
   - `Log`: Execution logs
   - `Schedule`: Task scheduling information

2. **Session Management**:
   - Handles database connections
   - Manages transactions
   - Provides connection pooling

### Task Scheduler (`core/scheduler/`)

1. **SchedulerService**:
   - Manages task scheduling
   - Handles cron and interval schedules
   - Maintains schedule state

2. **TaskRunner**:
   - Executes flow tasks
   - Manages task lifecycle
   - Handles retries and failures

## CLI Interface

The CLI provides three main command groups:

1. **Flows**:
   ```bash
   automagik flows sync    # Sync flows from LangFlow
   automagik flows list    # List available flows
   ```

2. **Schedules**:
   ```bash
   automagik schedules create  # Create new schedule
   automagik schedules list    # List schedules
   automagik schedules delete  # Delete schedule
   ```

3. **Tasks**:
   ```bash
   automagik tasks list    # List tasks
   automagik tasks logs    # View task logs
   automagik tasks output  # View task output
   ```

## Environment Configuration

Required environment variables:
- `LANGFLOW_API_URL`: LangFlow server URL
- `LANGFLOW_API_KEY`: API authentication key
- `DATABASE_URL`: Database connection string
- `TIMEZONE`: Local timezone (default: UTC)

## Error Handling

Custom exceptions are defined in respective modules:
- `core.flows.exceptions`: Flow-related errors
- `core.scheduler.exceptions`: Scheduling errors
- `core.database.exceptions`: Database errors

## Development Guidelines

1. **Code Organization**:
   - Business logic belongs in `core/`
   - CLI commands should be thin wrappers around core components
   - Keep database models in `core/database/models.py`

2. **Error Handling**:
   - Use custom exceptions for specific error cases
   - Provide meaningful error messages
   - Log errors appropriately

3. **Testing**:
   - Write unit tests for core components
   - Use mocks for external services
   - Test CLI commands independently

4. **Documentation**:
   - Document all public interfaces
   - Include usage examples
   - Keep API documentation up-to-date

## Security Considerations

1. **API Keys**:
   - Never log API keys
   - Store sensitive data in environment variables
   - Validate API key before operations

2. **Database**:
   - Use connection pooling
   - Implement proper transaction management
   - Sanitize all user inputs

3. **Task Execution**:
   - Implement proper isolation
   - Handle timeouts
   - Limit resource usage

## Future Improvements

1. **API Development**:
   - REST API interface
   - WebSocket support for real-time updates
   - API authentication

2. **Monitoring**:
   - Prometheus metrics
   - Health checks
   - Performance monitoring

3. **Enhanced Features**:
   - Flow versioning
   - Flow templates
   - Advanced scheduling options

## Troubleshooting

Common issues and solutions:

1. **Database Connectivity**:
   - Verify DATABASE_URL format
   - Check database permissions
   - Ensure proper SSL configuration

2. **LangFlow API**:
   - Validate API URL format
   - Check API key permissions
   - Verify network connectivity

3. **Task Execution**:
   - Check task logs
   - Verify flow configuration
   - Ensure required components are available