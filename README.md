# AutoMagik CLI

AutoMagik CLI is a powerful command-line interface for managing and scheduling LangFlow workflows. It provides seamless integration with LangFlow, allowing you to run and schedule flows directly from your terminal.

## Features

- Run LangFlow workflows from the command line
- Schedule workflows with cron expressions or intervals
- Daemon mode for background execution
- Systemd service integration
- SQLite database for workflow and task management
- Comprehensive logging and error handling

## Installation

### From PyPI

```bash
pip install automagik
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/automagik.git
cd automagik
```

2. Create a virtual environment and activate it:
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

4. Install the package in development mode:
```bash
pip install -e ./cli
```

## Configuration

1. Create a `.env` file in your project directory:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your settings:
```ini
LANGFLOW_API_URL=http://localhost:7860
AUTOMAGIK_DEBUG=1
AUTOMAGIK_LOG_LEVEL=DEBUG
TZ=America/Sao_Paulo
```

## Database Setup

The database will be automatically created on first run. By default, it uses SQLite and creates a file named `automagik.db` in your project directory.

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
# Using cron expression
automagik schedules create --flow-id <flow_id> --type cron --expr "*/5 * * * *" --params '{"key": "value"}'

# Using interval
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
