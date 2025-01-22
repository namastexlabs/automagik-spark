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
├── cli/                  # CLI implementation
├── core/                # Core business logic
├── alembic/             # Database migrations
├── instructions/        # Project documentation
├── setup.py            # Package configuration
├── alembic.ini         # Alembic configuration
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 13 or higher
- LangFlow server

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/namastexlabs/automagik.git
cd automagik
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

3. Install the package:
```bash
# For normal installation
pip install -e .

# For development (includes testing tools)
pip install -e ".[dev]"
```

## Configuration

Create a `.env` file in your project directory:

```bash
LANGFLOW_API_URL=http://your-langflow-server:7860
LANGFLOW_API_KEY=your-api-key
DATABASE_URL=postgresql://user:password@localhost:5432/automagik
TIMEZONE=UTC  # Or your local timezone, e.g., America/New_York
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
