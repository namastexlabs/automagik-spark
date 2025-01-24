# Current Task: Flow Scheduling System

## Project Overview

Automagik is a CLI tool that integrates with LangFlow to manage and execute flows. The system allows users to sync flows from a LangFlow server and schedule their execution.

## Current Implementation

### Flow Components
- Each flow has designated input and output components
- Components are identified by their IDs in the LangFlow system
- Only necessary component IDs are stored in the database

### Database Schema
- **Flows**: Stores flow metadata and component configurations
  - `id`: String (Primary Key)
  - `name`: String
  - `data`: JSON
  - `input_component`: String
  - `output_component`: String
  - `created_at`, `updated_at`: DateTime

- **Schedules**: Manages flow execution schedules
  - `id`: UUID
  - `flow_id`: String (FK to flows)
  - `schedule_type`: String (interval, cron, oneshot)
  - `schedule_expr`: String (e.g., "5m", "* * * * *", "2025-01-01T00:00:00")
  - `flow_params`: JSON
  - `next_run_at`: DateTime
  - `status`: String (active, paused, completed)

- **Tasks**: Tracks flow executions
  - `id`: UUID
  - `flow_id`: String (FK to flows)
  - `status`: String (pending, running, completed, failed)
  - `input_data`, `result`: JSON
  - Various timestamps

### Key Features
1. **Flow Sync**
   - Fetch flows from LangFlow server
   - User selects input/output components
   - Store only necessary data

2. **Scheduling**
   - Multiple schedule types:
     - Interval (e.g., "5m", "1h")
     - Cron (e.g., "* * * * *")
     - One-time (ISO datetime)
   - Schedule status management
   - Automatic task creation

3. **Task Execution**
   - Async task processing
   - Error handling and retries
   - Execution logging

## Running the CLI

### Basic Commands:

1. **Initialize Database**
```bash
python -m automagik.cli.cli db init
```

2. **Sync Flows**
```bash
python -m automagik.cli.cli flows sync
```

3. **Create Schedule**
```bash
python -m automagik.cli.cli schedules create --type interval --expr "1m" --input '{"input": "message"}' <flow-id>
```

4. **List Schedules**
```bash
python -m automagik.cli.cli schedules list
```

5. **List Tasks**
```bash
python -m automagik.cli.cli tasks list
```

### Environment Setup
Required environment variables:
```
LANGFLOW_API_URL=http://localhost:7860
LANGFLOW_API_KEY=<your-key>
DATABASE_URL=postgresql://automagik:automagik@localhost:5432/automagik
TIMEZONE=America/Sao_Paulo
```

## Current Issues and Next Steps

1. **Database Schema**
   - Simplified schema to focus on essential data
   - Removed unnecessary columns
   - Fixed foreign key constraints

2. **Async Support**
   - Implemented proper async database operations
   - Added event loop management in CLI commands
   - Improved error handling for async operations

3. **Next Steps**
   - Test schedule execution
   - Add component validation
   - Implement schedule status updates
   - Add task retry mechanism
   - Improve logging and monitoring
