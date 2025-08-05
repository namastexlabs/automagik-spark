# automagik-spark - Development Configuration

## 🚀 Available Agents

### Universal Analysis
- **automagik-spark-analyzer**: Universal codebase analysis and tech stack detection

### Core Development
- **automagik-spark-dev-planner**: Requirements analysis and technical specifications
- **automagik-spark-dev-designer**: Architecture design and system patterns
- **automagik-spark-dev-coder**: Code implementation with tech-stack awareness
- **automagik-spark-dev-fixer**: Debugging and systematic issue resolution

### Specialized Development Experts
- **automagik-spark-api-specialist**: FastAPI development and async API optimization
- **automagik-spark-workflow-orchestrator**: Celery task management and workflow coordination
- **automagik-spark-database-architect**: SQLAlchemy optimization and PostgreSQL management
- **automagik-spark-devops-automation**: Docker orchestration and PM2 deployment
- **automagik-spark-quality-assurance**: pytest testing and code quality management
- **automagik-spark-security-expert**: Authentication systems and security hardening
- **automagik-spark-integration-manager**: External API integration and plugin architecture

### Agent Management
- **automagik-spark-agent-creator**: Create new specialized agents
- **automagik-spark-agent-enhancer**: Enhance and improve existing agents
- **automagik-spark-clone**: Multi-task coordination with context preservation

### Documentation
- **automagik-spark-claudemd**: CLAUDE.md documentation management

## 🏗️ AutoMagik Spark Project Overview

AutoMagik Spark is an **automagion engine** that integrates with LangFlow instances to deploy, schedule, and monitor AI-powered workflows without coding.

### Tech Stack & Architecture
- **Backend**: FastAPI (async) with SQLAlchemy + PostgreSQL
- **Task Queue**: Celery with Redis broker
- **CLI**: Click framework with rich terminal formatting  
- **Container**: Docker & Docker Compose orchestration
- **Version**: 0.2.2 (Python 3.12+)

### Core Components
- **API Server**: REST API on port 8888 with Swagger docs at `/api/v1/docs`
- **Worker Service**: Celery-based task processing with horizontal scaling
- **Database**: PostgreSQL (port 15432) with Alembic migrations
- **CLI Tool**: `automagik` command for workflow and task management
- **External Services**: Redis (port 16379), LangFlow (port 17860)

### Development Environment
```bash
# Development setup (hybrid: containers for DB/Redis, local for API/Worker)
./scripts/setup_dev.sh

# Production setup (all containerized)
./scripts/setup_local.sh

# Start API with hot reload
automagik api start --reload

# Start worker
automagik worker

# Database operations
automagik db upgrade
```

### Key Features
- **Workflow Management**: Import flows from LangFlow, schedule workflows (cron/interval)
- **API Authentication**: API key-based authentication via middleware
- **Task Processing**: Async task execution with built-in retry mechanisms
- **LangFlow Integration**: Visual flow editor integration on port 17860

### Common Commands
```bash
# Workflow operations
automagik workflow list
automagik workflow get <id>

# Task management  
automagik task list
automagik task retry <id>

# Schedule management
automagik schedule list
automagik schedule create

# Docker operations
docker compose -p automagik -f docker/docker-compose.yml up -d
```

### Project Structure
```
automagik-spark/
├── automagik_spark/         # Main application package
│   ├── api/                # FastAPI application & routers
│   ├── cli/                # Click CLI commands
│   └── core/               # Business logic
│       ├── celery_app/     # Task queue configuration
│       ├── database/       # Models and async sessions
│       ├── scheduler/      # Workflow scheduling
│       └── workflows/      # Flow management
├── docker/                 # Docker configurations
├── migrations/            # Alembic database migrations
├── tests/                 # Comprehensive test suite
└── scripts/              # Setup and deployment scripts
```

### Development Patterns
- **Async-first**: Comprehensive async/await throughout codebase
- **Type Safety**: Full mypy integration with type hints
- **Quality Tools**: Triple-tier stack (ruff, black, mypy)
- **Testing**: pytest with async support and >70% coverage target
- **Docker**: Multi-service orchestration with PM2 process management

## 🎮 Command Reference

### Wish Command
Use `/wish` for any development request:
- `/wish "add authentication to this app"`
- `/wish "fix the failing tests"`
- `/wish "optimize database queries"`
- `/wish "create API documentation"`

### Agent-Specific Tasks
The system automatically routes tasks to the appropriate specialized agents based on the request type and complexity.

## 💡 Development Guidelines

### Code Style Preferences
- Use ES modules (import/export) syntax where applicable
- Destructure imports when possible
- Use TypeScript for all new frontend code
- Follow existing naming conventions
- Add docstrings for public APIs
- Use async/await instead of Promise chains
- Prefer const/let over var

### Workflow Guidelines
- Always run quality checks after making code changes
- Run tests before committing changes
- Use meaningful commit messages with Co-authored-by: Automagik Genie 🧞<genie@namastex.ai>
- Create feature branches for new functionality
- Ensure all tests pass before merging

## 🔧 Build Commands
- `pytest`: Run the full test suite
- `ruff check`: Run linting checks
- `ruff format`: Format code
- `mypy .`: Run type checking
- `automagik api start --reload`: Start API server with hot reload
- `automagik worker`: Start Celery worker
- `automagik db upgrade`: Run database migrations