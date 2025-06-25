# AutoMagik Spark Development Guide

## Overview

This directory contains development guidelines and workflows for the AutoMagik Spark automagion engine. AutoMagik Spark enables rapid development and deployment of AI-driven workflows with LangFlow integration.

## Project Structure

### Core Components
- **API Server**: FastAPI application providing REST endpoints
- **Worker Service**: Celery-based task processing engine
- **Database**: PostgreSQL with async SQLAlchemy
- **CLI Tool**: Click-based management interface
- **Docker**: Containerized deployment

### Key Directories
```
/home/cezar/automagik-bundle/automagik/
├── automagik/              # Main application package
│   ├── api/               # FastAPI endpoints
│   ├── cli/               # CLI commands
│   └── core/              # Business logic
├── docker/                # Docker configurations
├── migrations/           # Database migrations
├── tests/               # Test suite
└── scripts/             # Setup scripts
```

## Development Workflow

### 1. Planning Phase
Use the ORCHESTRATOR workflow to plan new features:
```
@ORCHESTRATOR Create new workflow for [name] that [description].
Integration: [LangFlow/Custom API]
Schedule: [one-time/cron/interval]
Priority: [high/medium/low]
```

### 2. Implementation Phase
Follow these patterns for different components:

#### API Endpoints
```python
# /automagik/api/routers/{feature}.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/{endpoint}")
async def endpoint_name(
    data: RequestSchema,
    db: AsyncSession = Depends(get_db)
):
    # Implementation
```

#### Celery Tasks
```python
# /automagik/core/celery_app/tasks/{feature}.py
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def task_name(self, param: str):
    # Implementation
```

#### Database Models
```python
# /automagik/core/database/models/{feature}.py
from sqlalchemy import Column, String
from automagik.core.database.base import Base

class Feature(Base):
    __tablename__ = "features"
    # Model definition
```

### 3. Testing Phase
Write comprehensive tests:
```python
# /tests/test_{feature}.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_feature(client: AsyncClient):
    response = await client.post("/api/v1/endpoint")
    assert response.status_code == 200
```

### 4. Deployment Phase
Deploy using Docker:
```bash
# Build and run services
docker compose -p automagik -f docker/docker-compose.yml up -d

# Check service health
docker compose -p automagik -f docker/docker-compose.yml ps
```

## Common Development Tasks

### Add New Workflow
1. Define workflow requirements
2. Create API endpoints for workflow management
3. Implement Celery tasks for execution
4. Add database models if needed
5. Write tests
6. Update documentation

### Integrate with LangFlow
1. Configure LANGFLOW_API_URL
2. Use workflow sync functionality
3. Map LangFlow outputs to Celery tasks
4. Handle async execution

### Schedule Tasks
1. Define schedule in database
2. Use Celery beat for scheduling
3. Support cron and interval patterns
4. Monitor execution history

## Quick Reference

### Environment Setup
```bash
# Development setup
./scripts/setup_dev.sh

# Start API with hot reload
automagik api start --reload

# Start worker
automagik worker

# Run tests
pytest
```

### CLI Commands
```bash
# Workflow management
automagik workflow list
automagik workflow get <id>

# Task management
automagik task list
automagik task retry <id>

# Schedule management
automagik schedule list
automagik schedule create

# Database operations
automagik db upgrade
```

### Service URLs
- API: http://localhost:8888
- API Docs: http://localhost:8888/api/v1/docs
- LangFlow: http://localhost:17860 (optional)
- PostgreSQL: localhost:15432
- Redis: localhost:16379

## Best Practices

### Code Quality
- Use type hints throughout
- Follow async/await patterns
- Handle errors gracefully
- Add comprehensive logging

### Testing
- Aim for >70% test coverage
- Test both success and failure cases
- Use pytest fixtures
- Mock external dependencies

### Security
- Validate all inputs
- Use API key authentication
- Never expose sensitive data
- Follow OWASP guidelines

### Performance
- Use database connection pooling
- Implement caching where appropriate
- Monitor task execution times
- Scale workers as needed

## Troubleshooting

### Common Issues

**API Not Starting**
```bash
# Check logs
docker logs automagik-api

# Verify port availability
lsof -i :8888
```

**Worker Not Processing**
```bash
# Check Celery status
celery -A automagik.core.celery_app inspect active

# View worker logs
docker logs automagik-worker
```

**Database Connection Issues**
```bash
# Check PostgreSQL
docker logs automagik-postgres

# Run migrations
automagik db upgrade
```

## Contributing

1. Create feature branch from main
2. Follow coding standards
3. Write tests for new features
4. Update documentation
5. Submit PR for review

---

*For detailed project documentation, see `/home/cezar/automagik-bundle/automagik/.claude/automagik_spark_instructions.md`*