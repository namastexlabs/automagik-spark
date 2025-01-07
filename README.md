# AutoMagik CLI

AutoMagik CLI is a powerful command-line interface for managing and scheduling LangFlow workflows. It provides seamless integration with LangFlow, allowing you to run and schedule flows directly from your terminal.

## Features

- Run LangFlow workflows from the command line
- Schedule workflows with cron expressions or intervals
- Daemon mode for background execution
- Systemd service integration
- PostgreSQL database for workflow and task management
- Comprehensive logging and error handling

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- LangFlow server running

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/automagik.git
cd automagik
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Install the packages in development mode:
```bash
pip install -e ./shared  # Install shared package first
pip install -e ./cli    # Install CLI package
```

## Configuration

1. Create a `.env` file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your settings:
```ini
TIMEZONE=America/Sao_Paulo
LANGFLOW_API_URL=http://localhost:7860
DATABASE_URL=postgresql://user:password@localhost:5432/automagik_db
AUTOMAGIK_DEBUG=1
AUTOMAGIK_LOG_LEVEL=DEBUG
```

## Database Setup

1. Create the PostgreSQL database:
```bash
# Connect to PostgreSQL and create the database
psql -h your_host -U your_user postgres -c "CREATE DATABASE automagik_db;"
```

2. Initialize the database schema:
```bash
# Make sure you're in the project directory
cd /path/to/automagik

# Run database initialization
automagik db init
```

To verify the database setup:
```bash
# List all tables
psql -h your_host -U your_user automagik_db -c "\dt"

# View specific table structure
psql -h your_host -U your_user automagik_db -c "\d flows"
```

## Usage

### Running Flows

1. List available flows:
```bash
automagik flows list
```

2. Run a flow:
```bash
automagik run start --flow-id <flow_id> --input '{"key": "value"}'
```

### Scheduling Flows

1. Create a new schedule:
```bash
# Using cron expression (run every 5 minutes)
automagik schedules create --flow-id <flow_id> --type cron --expr "*/5 * * * *" --params '{"key": "value"}'

# Using interval (run every 30 minutes)
automagik schedules create --flow-id <flow_id> --type interval --expr "30m" --params '{"key": "value"}'
```

2. List schedules:
```bash
automagik schedules list
```

3. Delete a schedule:
```bash
automagik schedules delete --id <schedule_id>
```

## Running as a Service

1. Install the service:
```bash
automagik install-service
```

2. Start the service:
```bash
sudo systemctl start automagik
```

3. Enable autostart:
```bash
sudo systemctl enable automagik
```

4. Check service status:
```bash
sudo systemctl status automagik
```

### Service Logs

View service logs:
```bash
journalctl -u automagik -f
```

## Troubleshooting

### Database Issues

1. Check database connection:
```bash
psql -h your_host -U your_user automagik_db
```

2. View migration status:
```bash
cd cli  # Go to directory with alembic.ini
alembic current
```

3. Reset migrations if needed:
```bash
alembic downgrade base  # Reset to beginning
alembic upgrade head    # Apply all migrations
```

### Service Issues

1. Check service logs for errors:
```bash
journalctl -u automagik -n 50 --no-pager
```

2. Verify environment configuration:
```bash
sudo systemctl cat automagik
```

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

1. Create a new migration:
```bash
alembic revision -m "description of changes"
```

2. Apply migrations:
```bash
alembic upgrade head
```

## License

[MIT License](LICENSE)
