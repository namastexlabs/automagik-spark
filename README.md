# AutoMagik

AutoMagik is a powerful task automation and scheduling system that integrates with LangFlow to run AI workflows.

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis (for Celery)
- LangFlow server

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/namastexlabs/automagik.git
cd automagik

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### 2. Development Setup

For development, you'll need additional tools and configurations:

```bash
# Run the setup script (requires root)
sudo ./scripts/setup.sh

# This will:
# - Install all dependencies (including dev dependencies)
# - Set up git hooks for pre-push checks
# - Configure logging
# - Set up and start the service
```

The setup includes git hooks that run automated checks before pushing:
- Pre-push hook runs all tests with coverage checks
- Current minimum coverage threshold: 45%

To run tests manually:
```bash
./scripts/run_tests.sh
```

### 3. Configuration

Create a `.env` file in the root directory:

```bash
# Environment
ENV=development

# Security
AUTOMAGIK_API_KEY=your-api-key

# PostgreSQL Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/automagik_db

# Redis & Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# LangFlow Configuration
LANGFLOW_API_URL=http://localhost:7860
LANGFLOW_API_KEY=your-langflow-api-key

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 4. Database Setup

```bash
# Start PostgreSQL (if not running)
sudo service postgresql start

# Create database and user
sudo -u postgres psql
postgres=# CREATE USER your_user WITH PASSWORD 'your_password';
postgres=# CREATE DATABASE automagik_db OWNER your_user;
postgres=# \q
```

### 5. Running the Services

```bash
# Start Redis (if not running)
sudo service redis-server start

# Start the API server
uvicorn automagik.api.main:app --reload --port 8000 --host 0.0.0.0

# Start the task processor
automagik run start

# Start the Celery worker (in a new terminal)
celery -A automagik.core.celery_app worker --loglevel=info
```

### 6. Testing the Setup

```bash
# Test the API
curl http://localhost:8000/health

# Create and test a flow
automagik flows sync  # Sync flows from LangFlow
automagik flows list  # List available flows
automagik run test <flow-id>  # Test run a flow
```

### 6. Scheduling Tasks

AutoMagik supports three types of task scheduling:

1. **Cron Schedules**: Run tasks on a recurring schedule using cron expressions
   ```bash
   # Run daily at 8 AM
   automagik schedules create my-flow --type cron --expr "0 8 * * *" --input '{"key": "value"}'
   ```

2. **Interval Schedules**: Run tasks at fixed time intervals
   ```bash
   # Run every 30 minutes
   automagik schedules create my-flow --type interval --expr "30m" --input '{"key": "value"}'
   ```

3. **One-Time Schedules**: Run tasks once at a specific date and time
   ```bash
   # Run once on January 24, 2025 at midnight UTC
   automagik schedules create my-flow --type oneshot --expr "2025-01-24T00:00:00" --input '{"key": "value"}'
   ```

View and manage your schedules:
```bash
# List all schedules
automagik schedules list

# Filter by type
automagik schedules list --type oneshot

# Filter by status
automagik schedules list --status active
```

For more details on scheduling, see the [CLI documentation](docs/CLI.md).

## Features

- **Flow Management**: Sync and manage LangFlow workflows
- **Task Scheduling**: Schedule flows to run at specific intervals
- **Task Execution**: Run flows with custom inputs and handle retries
- **API Integration**: RESTful API for managing flows, schedules, and tasks
- **Monitoring**: Track task status and view execution logs

## Documentation

### Guides and References
- [Setup Guide](/docs/SETUP.md) - Detailed installation and configuration
- [CLI Reference](/docs/CLI.md) - Command-line interface documentation
- [Development Guide](/docs/DEVELOPMENT.md) - Contributing and development setup
- [Architecture](/docs/ARCHITECTURE.md) - System design and components

### API Documentation
- [API Guide](/docs/API.md) - REST API overview and usage
- Interactive API Explorer (Swagger UI): http://localhost:8000/docs
- API Reference (ReDoc): http://localhost:8000/redoc

## CLI Reference

```bash
# General commands
automagik --help                  # Show all available commands

# Flow management
automagik flows list             # List all flows
automagik flows sync             # Sync flows from LangFlow
automagik flows get <flow-id>    # Get flow details

# Schedule management
automagik schedules list         # List all schedules
automagik schedules create       # Create a new schedule
automagik schedules get <id>     # Get schedule details

# Task management
automagik run start             # Start the task processor
automagik run test <flow-id>    # Test run a flow
```

## CLI Examples

### Flow Management
```bash
# List all flows with their IDs and status
automagik flows list

# Get details of a specific flow
automagik flows get 3cf82804-41b2-4731-9306-f77e17193799

# Sync flows from LangFlow server
automagik flows sync
```

### Schedule Management
```bash
# Create a new schedule for a flow
automagik schedules create \
  --flow-id 3cf82804-41b2-4731-9306-f77e17193799 \
  --type interval \
  --expr "1m" \
  --input '{"message": "Hello, World!"}'

# List all schedules
automagik schedules list

# Get schedule details
automagik schedules get 3cf82804-41b2-4731-9306-f77e17193799

# Update schedule status
automagik schedules update 3cf82804-41b2-4731-9306-f77e17193799 --status disabled
```

### Task Management
```bash
# Test run a flow with input
automagik run test 3cf82804-41b2-4731-9306-f77e17193799 \
  --input '{"message": "Test message"}'

# Start task processor in daemon mode
automagik run start --daemon

# Start task processor with debug logging
automagik run start --log-level DEBUG

# View task logs
automagik tasks logs 3cf82804-41b2-4731-9306-f77e17193799

# List recent tasks
automagik tasks list --limit 10 --status completed
```

### Common Testing Scenarios

1. **Test Flow Sync and Listing**
```bash
# Sync flows and verify they appear in list
automagik flows sync
automagik flows list | grep "WhatsApp"
```

2. **Test Schedule Creation and Execution**
```bash
# Create a one-time schedule
FLOW_ID=$(automagik flows list | grep "WhatsApp" | cut -d' ' -f1)
automagik schedules create \
  --flow-id $FLOW_ID \
  --type oneshot \
  --expr "2025-01-24T00:00:00" \
  --input '{"message": "Scheduled test"}'

# Verify schedule was created
automagik schedules list | grep $FLOW_ID
```


3. **Test Flow Execution with Different Inputs**
```bash
# Test with text input
automagik run test $FLOW_ID --input '{"message": "Text input test"}'

# Test with JSON input
automagik run test $FLOW_ID --input '{"message": "JSON test", "metadata": {"source": "cli", "priority": "high"}}'

# Test with file input
echo '{"message": "File test"}' > test_input.json
automagik run test $FLOW_ID --input @test_input.json
```

4. **Test Error Handling**
```bash
# Test with invalid flow ID
automagik run test invalid-id

# Test with invalid input format
automagik run test $FLOW_ID --input 'invalid json'

# Test with missing required input
automagik run test $FLOW_ID --input '{}'
```

5. **Test Task Monitoring**
```bash
# Monitor task execution
TASK_ID=$(automagik run test $FLOW_ID --input '{"message": "Monitor test"}' | grep "Created task" | cut -d' ' -f3)
automagik tasks logs $TASK_ID --follow

# Check task status
automagik tasks get $TASK_ID
```

### Environment Testing
```bash
# Test with different API URLs
LANGFLOW_API_URL=http://other-server:7860 automagik flows list

# Test with different API keys
LANGFLOW_API_KEY=new-key automagik flows sync

# Test with debug logging
AUTOMAGIK_LOG_LEVEL=DEBUG automagik run test $FLOW_ID
```

## Development Status

### Recent Updates
- Added integration testing with SQLite for ephemeral test databases
- Improved flow sync to handle different API response formats
- Added test cases for flow and schedule creation
- Enhanced error handling in core services

### Current Focus
- Improving integration test reliability
- Enhancing flow sync functionality
- Adding comprehensive test coverage

Check [TODO.md](TODO.md) for current tasks and upcoming features.

## Architecture

### Core Services
- **Flow Manager**: Handles flow synchronization and storage
  - Supports both string and dict data formats from LangFlow API
  - Extracts and stores input/output components
  - Manages flow metadata and versioning

- **Flow Analyzer**: Analyzes flow components and structure
  - Identifies input and output nodes
  - Extracts tweakable parameters
  - Validates flow structure

- **Schedule Manager**: Manages flow execution schedules
  - Creates and updates schedules
  - Handles schedule metadata
  - Manages schedule execution state

### Database Models
- **FlowDB**: Stores flow data and metadata
- **FlowComponent**: Tracks flow components and their relationships
- **Schedule**: Manages execution schedules for flows

### Testing
- **Integration Tests**: Uses SQLite for ephemeral testing
  - Mocks LangFlow API responses
  - Tests flow sync and schedule creation
  - Verifies database operations

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8
black .
isort .
```

For more detailed information, check out our [documentation](docs/README.md).

## License

This project is licensed under the terms of the MIT license.
