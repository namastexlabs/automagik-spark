# AutoMagik

AutoMagik is a powerful CLI tool and API for managing and automating LangFlow workflows. It provides seamless integration with LangFlow, allowing you to sync, schedule, and monitor your flows with ease.

## Features

- **Flow Management**: Sync and manage your LangFlow flows
- **Task Management**: Execute and monitor flow tasks
- **Scheduling**: Set up automated flow executions
- **API**: RESTful API for integration with other services
- **Service Management**: Run as a system service

## Quick Start

```bash
# Clone the repository
git clone https://github.com/namastexlabs/automagik.git
cd automagik

# Copy and edit environment variables
cp .env.example .env

# Run the setup script
sudo ./scripts/setup.sh
```

## Documentation

Detailed documentation is available in the `docs` directory:

- [Setup Guide](docs/SETUP.md)
  - Installation instructions
  - Environment configuration
  - Service management
  - Troubleshooting

- [API Documentation](docs/API.md)
  - API endpoints
  - Authentication
  - Request/response formats
  - Error handling

- [CLI Guide](docs/CLI.md)
  - Command reference
  - Configuration
  - Usage examples
  - Environment variables

- [Development Guide](docs/DEVELOPMENT.md)
  - Development setup
  - Testing
  - Contributing
  - Code style

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Redis Server
- LangFlow instance

## Support

If you encounter any issues:

1. Check our [Setup Guide](docs/SETUP.md#troubleshooting) for common problems
2. Review the logs at `/var/log/automagik/`
3. Open an issue on GitHub

## License

This project is licensed under the terms of the MIT license.
