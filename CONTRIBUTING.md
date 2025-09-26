# Contributing to Automagik Spark

Thank you for your interest in contributing to Automagik Spark! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

We love feature suggestions! Please create an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. **Discuss First**: Open an issue to discuss your proposed changes
2. **Fork & Branch**: Fork the repo and create a feature branch
3. **Follow Standards**: Match existing code patterns (async/await, type hints)
4. **Add Tests**: Include tests for new features (we aim for >70% coverage)
5. **Document**: Update docstrings and documentation
6. **Quality Checks**: Run `ruff format .` and `ruff check .`
7. **Commit Format**: Use conventional commits with co-author:
   ```
   feat: add amazing feature

   Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>
   ```

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/automagik-spark.git
cd automagik-spark

# Run development setup
./scripts/setup_dev.sh

# Activate virtual environment
source .venv/bin/activate

# Run tests
pytest

# Check code quality
ruff format . && ruff check . && mypy .
```

### Code Style

- Use async/await for asynchronous operations
- Add type hints to all functions
- Follow PEP 8 style guidelines
- Write descriptive docstrings
- Keep functions focused and small

### Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for >70% code coverage
- Use fixtures for common test data

## Code of Conduct

Please be respectful and professional in all interactions. We are committed to providing a welcoming and inclusive environment for all contributors.

## Questions?

Join our [Discord](https://discord.gg/xcW8c7fF3R) or open a discussion on GitHub.

---

Thank you for contributing to Automagik Spark! 🎉