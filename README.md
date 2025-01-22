# AutoMagik

AutoMagik is a powerful tool for managing and scheduling LangFlow workflows. It provides seamless integration with LangFlow, allowing you to run and schedule flows directly from your terminal.

## Features

- Run LangFlow workflows from the command line
- Schedule workflows with cron expressions or intervals
- Real-time task monitoring and logging
- PostgreSQL database for workflow and task management
- Comprehensive error handling and retries
- Flow analysis and component validation

## Project Structure

```
automagik/
├── cli/                 # CLI implementation
├── core/                # Core business logic
├── alembic/             # Database migrations
├── instructions/        # Project documentation
├── setup.py             # Package configuration
├── alembic.ini          # Alembic configuration
└── README.md            # This file
```

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Redis Server
- LangFlow instance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/namastexlabs/automagik.git
cd automagik
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the package:
```bash
pip install -e .
```

4. Configure environment variables:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Required variables:
AUTOMAGIK_API_KEY=your-api-key
DATABASE_URL=postgresql://user:password@localhost:5432/automagik_db
LANGFLOW_API_URL=http://your-langflow-instance
LANGFLOW_API_KEY=your-langflow-api-key
```

5. Initialize the database:
```bash
automagik db init
```

6. Install as a system service (optional):
```bash
automagik install-service
```

## Docker Setup

AutoMagik requires PostgreSQL and Redis for its operation. We provide a Docker Compose configuration to easily spin up these services.

### Prerequisites
- Docker
- Docker Compose

### Starting the Services

1. Make sure you have configured your `.env` file (see Configuration section above)

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Verify the services are running:
   ```bash
   docker-compose ps
   ```

The services will be available at:
- PostgreSQL: localhost:5432 (credentials as configured in your .env file)
- Redis: localhost:6379

### Stopping the Services

To stop the services:
```bash
docker-compose down
```

To stop the services and remove all data:
```bash
docker-compose down -v
```

## Configuration

Create a `.env` file in your project directory:

```bash
LANGFLOW_API_URL=http://your-langflow-server:7860
LANGFLOW_API_KEY=your-api-key
DATABASE_URL=postgresql://user:password@localhost:5432/automagik
TIMEZONE=UTC  # Or your local timezone, e.g., America/New_York
```

## API Authentication

The AutoMagik API uses API key authentication. To set up authentication:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Generate a secure API key:
   ```bash
   openssl rand -hex 32
   ```

3. Add the generated key to your `.env` file:
   ```bash
   AUTOMAGIK_API_KEY=your-generated-key
   ```

4. When making API requests, include the API key in the `X-API-Key` header:
   ```bash
   curl http://localhost:8000/flows -H "X-API-Key: your-generated-key"
   ```

## Usage

### Flow Management

```bash
# List available flows
automagik flows list

# Sync flows from LangFlow
automagik flows sync
```

### Schedule Management

```bash
# Create a new schedule
automagik schedules create

# List all schedules
automagik schedules list

# Delete a schedule
automagik schedules delete <schedule-id>
```

### Task Management

```bash
# List all tasks
automagik tasks list

# View task logs
automagik tasks logs <task-id>

# View task output
automagik tasks output <task-id>
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Formatting

```bash
# Format code
black .
isort .

# Check style
flake8
```

### Type Checking

```bash
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
