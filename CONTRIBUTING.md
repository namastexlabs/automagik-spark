# 🤝 Contributing to AutoMagik Spark

First off, thank you for considering contributing to AutoMagik Spark! As a key component in the NamasteX Labs ecosystem, AutoMagik Spark aims to make workflow automation accessible and efficient. Every contribution, whether it's fixing a bug, improving documentation, or suggesting new features, helps make this goal a reality.

## 📜 Code of Conduct

This project adheres to the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior to maintainers@namastexlabs.com.

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 6+

### Development Environment Setup

1. **Fork and Clone**
```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/automagik-spark.git
cd automagik-spark
git remote add upstream https://github.com/namastexlabs/automagik-spark.git
```

2. **Set up the development environment**
```bash
# Install development dependencies and setup virtual environment
./scripts/setup_dev.sh

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
source .venv/bin/activate

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your local configuration
```

3. **Start required services**
```bash
# Start PostgreSQL and Redis
docker-compose -f docker/docker-compose.dev.yml up -d

# Run database migrations
alembic upgrade head
```

4. **Verify your setup**
```bash
# Run tests to ensure everything is working
pytest

# Run code quality checks
ruff format . && ruff check . && mypy .

# Start the development server
python -m automagik_spark.api
```

## 🔄 Development Workflow

### Branch Organization

Our repository has the following main branches:
- `main` - Production-ready code
- `develop` - Integration branch for features
- `release/*` - Release preparation branches

### Feature Development

1. **Create a new branch from develop**
   ```bash
   git checkout develop
   git pull upstream develop
   git checkout -b feature/your-feature-name
   ```
   
   Branch naming patterns:
   - Features: `feature/XXX-short-description` (XXX is issue number)
   - Fixes: `fix/XXX-issue-description`
   - Docs: `docs/XXX-documentation-scope`
   - Tests: `test/XXX-test-description`

2. **Development Guidelines**
   - Write clear, commented code following PEP 8
   - Include type hints for all functions:
     ```python
     from typing import Optional, List
     
     def process_data(input_data: List[dict], batch_size: Optional[int] = None) -> dict:
         """
         Process input data in batches.
         
         Args:
             input_data: List of dictionaries containing data to process
             batch_size: Optional batch size for processing
             
         Returns:
             dict: Processing results and statistics
         """
         pass
     ```
   - Add tests for new features
   - Update API documentation if endpoints change
   - Keep commits atomic and focused

3. **Commit your changes**
   - Follow conventional commit format:
   ```
   type(scope): description

   [optional body]

   [optional footer]

   Co-authored-by: name <email>
   ```
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   - Example:
   ```
   feat(scheduler): add custom cron expression support
   
   Implement custom cron expression parser for advanced scheduling
   Add validation for expression format
   Update documentation
   
   Closes #123
   ```

## ✅ Testing Guidelines

### Test Categories

1. **Unit Tests** (`tests/`)
   - Test individual components in isolation
   - Mock external dependencies
   - Fast execution, no I/O

2. **Integration Tests** (`tests/integration/`)
   - Test component interactions
   - Require Docker services
   - Run with real database/Redis

3. **API Tests** (`tests/api/`)
   - Test HTTP endpoints
   - Validate request/response schemas
   - Check authentication/authorization

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=automagik_spark --cov-report=html --cov-fail-under=85

# Run specific test categories
pytest tests/unit  # Unit tests only
pytest tests/integration  # Integration tests
pytest tests/api  # API tests

# Run tests matching a pattern
pytest -k "test_scheduler"  # Run tests containing "test_scheduler"

# Run with debug output
pytest -vv --log-cli-level=DEBUG

# Run failed tests only
pytest --lf
```

### Writing Tests

```python
import pytest
from automagik_spark.core.scheduler import WorkflowScheduler

@pytest.mark.asyncio
async def test_schedule_workflow(mock_db_session):
    # Given
    scheduler = WorkflowScheduler()
    workflow_data = {"id": "test-123", "schedule": "*/5 * * * *"}
    
    # When
    result = await scheduler.schedule_workflow(workflow_data)
    
    # Then
    assert result.status == "scheduled"
    assert result.next_run is not None
```

## 🎨 Code Style

We use several tools to maintain code quality:

1. **Ruff** for linting and formatting
   - Line length: 120 characters
   - Python target: 3.12
   - Auto-formatting: `ruff format .`
   - Linting: `ruff check .`

2. **MyPy** for type checking
   - Strict type checking enabled
   - Run: `mypy .`

3. **Code Style Guidelines**
   - Use descriptive variable names
   - Include docstrings for functions and classes:
   ```python
   def process_workflow(workflow_id: str) -> WorkflowResult:
       """
       Process a workflow by its ID.

       Args:
           workflow_id: Unique identifier of the workflow

       Returns:
           WorkflowResult: Results of the workflow execution
       """
       ...
   ```
   - Prefer async/await patterns where applicable
   - Keep functions focused and single-purpose

## 🌱 Good First Issues

We tag issues perfect for new contributors with `good-first-issue`. Here are some areas where we especially welcome help:

1. **Documentation and Examples**
   - Adding type hints to functions
   - Improving docstrings
   - Creating usage examples for API endpoints
   - Writing workflow templates
   - Adding validation error messages

2. **Testing and Coverage**
   - Writing integration tests for workflow types
   - Adding edge case tests for scheduler
   - Testing error handling scenarios
   - Improving mock data fixtures
   - Adding API endpoint tests

3. **Code Quality**
   - Implementing type hints in legacy code
   - Converting sync code to async
   - Improving error messages
   - Adding input validation
   - Optimizing database queries

4. **Feature Enhancement**
   - Adding new workflow templates
   - Implementing additional trigger types
   - Creating new API endpoints
   - Adding webhook integrations
   - Improving logging and monitoring

## 📝 Pull Request Process

1. **Before Creating a PR**
   ```bash
   # Update your fork's develop branch
   git checkout develop
   git pull upstream develop
   
   # Update your feature branch
   git checkout feature/XXX-your-feature
   git rebase develop
   
   # Run full test suite and quality checks
   docker-compose -f docker/docker-compose.dev.yml up -d
   pytest --cov=automagik_spark --cov-report=html
   ruff format . && ruff check . && mypy .
   ```

2. **PR Guidelines**
   - Target the `develop` branch
   - Include issue number in title: `feat(core): add custom scheduler (#123)`
   - Add detailed description using our PR template
   - Update CHANGELOG.md following Keep a Changelog format
   - Include migration scripts if database changes
   - Add tests covering new functionality
   - Update API documentation if endpoints change

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - Test coverage: XX%
   - New tests added: Yes/No
   - Breaking changes: Yes/No

   ## Checklist
   - [ ] Tests pass
   - [ ] Code follows style guide
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   ```

## ❓ Getting Help

- **Technical Questions**: Create a [Discussion](https://github.com/namastexlabs/automagik-spark/discussions)
- **Bug Reports**: Open an [Issue](https://github.com/namastexlabs/automagik-spark/issues/new/choose)
- **Discord**: Join our [Discord Server](https://discord.gg/namastexlabs)
- **Documentation**: Visit our [Documentation Site](https://docs.namastexlabs.com)

## 🙏 Recognition

Contributors are recognized in several ways:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Featured in our monthly newsletter
- Invited to join our Discord contributors channel

Thank you for helping make AutoMagik Spark better! 🚀