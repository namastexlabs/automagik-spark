# AutoMagik Development Guide

This guide covers development setup and best practices for AutoMagik.

## Development Setup

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/namastexlabs/automagik.git
cd automagik

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

### 2. Configure Environment

```bash
# Copy example environment
cp .env.example .env

# Edit .env with development settings
DATABASE_URL=postgresql://localhost/automagik_dev
AUTOMAGIK_API_KEY=dev-key
```

### 3. Setup Database

```bash
# Create development database
createdb automagik_dev

# Run migrations
automagik db upgrade
```

## Project Structure

```
automagik/
├── automagik/
│   ├── api/           # FastAPI application
│   ├── cli/           # CLI commands
│   ├── core/          # Core business logic
│   │   ├── services/   # Main services
│   │   ├── database/   # Database models
│   │   └── utils/      # Utilities
│   └── utils/         # Utility functions
├── docs/              # Documentation
├── scripts/           # Helper scripts
├── tests/             # Test suite
└── alembic/           # Database migrations
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=automagik

# Generate coverage report
coverage html
```

### Writing Tests

1. Place tests in `tests/` directory
2. Name test files `test_*.py`
3. Use fixtures from `conftest.py`
4. Mock external services

Example test:
```python
def test_flow_creation(client, mock_langflow):
    response = client.post("/flows", json={...})
    assert response.status_code == 200
```

## Code Style

We use:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run formatters:
```bash
# Format code
black automagik tests

# Sort imports
isort automagik tests

# Run linter
flake8 automagik tests

# Type check
mypy automagik
```

## Database Migrations

### Create Migration

```bash
# Generate migration
alembic revision -m "description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Migration Guidelines

1. Make migrations reversible
2. Test both upgrade and downgrade
3. Don't modify existing migrations
4. Include data migrations when needed

## Debugging

### API Debugging

1. Enable debug mode in `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

2. Run API with reload:
```bash
uvicorn automagik.api.main:app --reload --log-level debug
```

### CLI Debugging

Run with debug flag:
```bash
automagik --debug flows list
```

## Documentation

### API Documentation

1. Document new endpoints in `docs/API.md`
2. Update OpenAPI schema
3. Include request/response examples

### Code Documentation

1. Use Google-style docstrings
2. Document all public functions
3. Include type hints

Example:
```python
def get_flow(flow_id: str) -> Flow:
    """Get flow by ID.

    Args:
        flow_id: Unique flow identifier

    Returns:
        Flow object if found

    Raises:
        FlowNotFound: If flow doesn't exist
    """
```

## Logging

### Log Levels

- DEBUG: Detailed debugging
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical failures

### Best Practices

1. Use structured logging
2. Include context
3. Don't log sensitive data
4. Use appropriate levels

Example:
```python
logger.info("Processing flow", 
    extra={
        "flow_id": flow.id,
        "user_id": user.id
    }
)
```

## Error Handling

### API Errors

1. Use custom exceptions
2. Return consistent error responses
3. Log full stack traces
4. Hide internal details from users

Example:
```python
try:
    process_flow(flow_id)
except FlowNotFound:
    raise HTTPException(status_code=404)
except Exception as e:
    logger.exception("Flow processing failed")
    raise HTTPException(status_code=500)
```

## Contributing

1. Create feature branch
2. Write tests
3. Update documentation
4. Submit pull request

### Pull Request Checklist

- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
