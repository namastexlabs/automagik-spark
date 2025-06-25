# AutoMagik Spark - Automagion Engine

## Project Overview

AutoMagik Spark (formerly automagik) is an automagion engine that integrates with LangFlow instances to deploy, schedule, and monitor AI-powered workflows without coding.

## Repository Information
- **Name**: automagik-spark
- **Location**: `/home/cezar/automagik-bundle/automagik/`
- **Type**: Python FastAPI application with Celery workers
- **Version**: 0.2.2
- **License**: MIT

## Tech Stack
- **Backend Framework**: FastAPI (async)
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Task Queue**: Celery with Redis
- **CLI**: Click
- **Container**: Docker & Docker Compose
- **Python**: 3.10+
- **Testing**: Pytest with async support

## Architecture Components

### 1. API Server (`/automagik/api/`)
- REST API on port 8888
- Authentication via API keys
- Endpoints for workflows, tasks, schedules, sources
- Swagger docs at `/api/v1/docs`
- ReDoc at `/api/v1/redoc`

### 2. Worker Service (`/automagik/core/`)
- Celery-based task processing
- Handles workflow execution
- Manages scheduled tasks (cron & interval)
- Retry mechanisms for failed tasks

### 3. Database (`/migrations/`)
- PostgreSQL on port 15432
- Alembic for migrations
- Async database operations
- Models in `/automagik/core/database/models/`

### 4. CLI Tool (`/automagik/cli/`)
- Command-line interface for management
- Commands: api, worker, db, workflow, task, schedule, source
- Installed as `automagik` command

### 5. External Services
- Redis (port 16379) - Message broker
- LangFlow (port 17860) - Optional visual flow editor

## Project Structure
```
automagik/
├── automagik/              # Main application package
│   ├── api/               # FastAPI application
│   │   ├── routers/       # API endpoints
│   │   └── middleware/    # Authentication, CORS
│   ├── cli/               # Click CLI commands
│   ├── core/              # Business logic
│   │   ├── celery_app/    # Task queue configuration
│   │   ├── database/      # Models and sessions
│   │   ├── scheduler/     # Workflow scheduling
│   │   └── workflows/     # Flow management
│   └── version.py         # Version tracking
├── docker/                # Docker configurations
│   ├── api/              # API Dockerfile
│   ├── worker/           # Worker Dockerfile
│   └── docker-compose.yml # Main compose file
├── migrations/           # Alembic database migrations
├── tests/               # Test suite
├── scripts/             # Setup scripts
│   ├── setup_local.sh   # Production setup
│   └── setup_dev.sh     # Development setup
└── docs/                # Documentation
```

## Development Workflow

### Setup Options

#### 1. Local Production (Docker)
```bash
./scripts/setup_local.sh
# Runs all services in containers
# Installs CLI tool
# Sets up database
```

#### 2. Development (Hybrid)
```bash
./scripts/setup_dev.sh
# PostgreSQL & Redis in Docker
# API & Worker run locally
# Hot reload enabled
```

### Common Commands

#### Docker Operations
```bash
# Start services
docker compose -p automagik -f docker/docker-compose.yml up -d

# With LangFlow
docker compose -p automagik -f docker/docker-compose.yml --profile langflow up -d

# View logs
docker compose -p automagik -f docker/docker-compose.yml logs -f

# Stop services
docker compose -p automagik -f docker/docker-compose.yml down
```

#### CLI Commands
```bash
# API management
automagik api start [--reload]
automagik api stop

# Worker management
automagik worker

# Database operations
automagik db init
automagik db upgrade

# Workflow operations
automagik workflow list
automagik workflow get <id>
automagik workflow delete <id>

# Task operations
automagik task list
automagik task get <id>
automagik task retry <id>

# Schedule operations
automagik schedule list
automagik schedule get <id>
automagik schedule delete <id>

# Source management
automagik source list
automagik source create
automagik source sync <id>
```

### Environment Configuration
Key environment variables in `.env`:
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:15432/automagik

# API Configuration
AUTOMAGIK_API_HOST=0.0.0.0
AUTOMAGIK_API_PORT=8888
AUTOMAGIK_API_KEY=your-api-key

# External Services
LANGFLOW_API_URL=http://localhost:17860
CELERY_BROKER_URL=redis://localhost:16379/0

# Worker Configuration
CELERY_RESULT_BACKEND=redis://localhost:16379/1
CELERY_TASK_TIME_LIMIT=3600
```

## Key Features

### Workflow Management
- Import flows from LangFlow
- Schedule workflows (cron or interval)
- Track execution history
- Handle retries and failures

### API Authentication
- API key-based authentication
- Middleware validates all requests
- Keys configured via environment

### Task Processing
- Asynchronous task execution
- Celery workers scale horizontally
- Built-in retry mechanisms
- Task status tracking

### Database Operations
- Async SQLAlchemy for performance
- Alembic migrations
- Connection pooling
- Transaction management

## Testing

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=automagik

# Specific module
pytest tests/test_api/

# Async tests
pytest -v tests/test_core/test_workflows/
```

### Test Structure
```
tests/
├── test_api/        # API endpoint tests
├── test_cli/        # CLI command tests
├── test_core/       # Core logic tests
└── conftest.py      # Fixtures and configuration
```

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Async/await for I/O operations
- Comprehensive docstrings

### Git Workflow
- Feature branches from main
- Conventional commits
- PR reviews required
- CI/CD via GitHub Actions

### Adding New Features
1. Create feature branch
2. Add models if needed
3. Create migrations: `alembic revision --autogenerate -m "message"`
4. Implement API endpoints
5. Add Celery tasks
6. Write tests
7. Update documentation

### Common Tasks

#### Add New API Endpoint
1. Create router in `/api/routers/`
2. Add to main router
3. Implement business logic in `/core/`
4. Add tests

#### Add New Celery Task
1. Define task in `/core/celery_app/tasks/`
2. Register with Celery app
3. Add task execution logic
4. Test with worker running

#### Add Database Model
1. Create model in `/core/database/models/`
2. Generate migration
3. Update database
4. Add CRUD operations

## Deployment

### Production Setup
1. Set production environment variables
2. Run database migrations
3. Start services with docker-compose
4. Configure reverse proxy (nginx)
5. Set up SSL certificates
6. Monitor with logs

### Scaling
- API: Multiple container instances
- Workers: Scale Celery workers
- Database: Connection pooling
- Redis: Sentinel for HA

## Troubleshooting

### Common Issues

#### API Not Starting
- Check port 8888 availability
- Verify DATABASE_URL
- Check logs: `docker logs automagik-api`

#### Worker Not Processing
- Verify Redis connection
- Check Celery logs
- Ensure tasks are registered

#### Database Errors
- Run migrations: `automagik db upgrade`
- Check PostgreSQL logs
- Verify connection string

### Debug Mode
```bash
# Enable debug logging
export AUTOMAGIK_LOG_LEVEL=DEBUG

# Run with reload
automagik api start --reload

# Check worker tasks
celery -A automagik.core.celery_app inspect active
```

## Important Notes

1. **Security**: Always use strong API keys in production
2. **Database**: Regular backups recommended
3. **Monitoring**: Set up logging aggregation
4. **Performance**: Use connection pooling
5. **Updates**: Keep dependencies updated

## Quick Reference

### Service URLs
- API: http://localhost:8888
- Docs: http://localhost:8888/api/v1/docs
- LangFlow: http://localhost:17860 (if enabled)
- PostgreSQL: localhost:15432
- Redis: localhost:16379

### File Locations
- API routes: `/automagik/api/routers/`
- Models: `/automagik/core/database/models/`
- Tasks: `/automagik/core/celery_app/tasks/`
- CLI: `/automagik/cli/commands/`
- Tests: `/tests/`

### Configuration Files
- Docker: `/docker/docker-compose.yml`
- Python: `/pyproject.toml`
- Database: `/alembic.ini`
- Tests: `/pytest.ini`

---

*This document provides instructions for working with the AutoMagik Spark automagion engine. For detailed API documentation, visit the Swagger UI at `/api/v1/docs` when the service is running.*