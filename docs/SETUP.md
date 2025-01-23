# AutoMagik Setup Guide

This guide covers the installation and setup of AutoMagik.

## Prerequisites

Before installing AutoMagik, ensure you have:

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Redis Server
- LangFlow instance

## Installation Methods

### 1. Quick Installation (Recommended)

Use our automated setup script:

```bash
# Clone the repository
git clone https://github.com/namastexlabs/automagik.git
cd automagik

# Copy and edit environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the setup script
sudo ./scripts/setup.sh
```

### 2. Manual Installation

If you prefer manual control:

1. Clone and prepare:
```bash
git clone https://github.com/namastexlabs/automagik.git
cd automagik
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -e .
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Initialize database:
```bash
automagik db init
```

5. Set up logging:
```bash
sudo mkdir -p /var/log/automagik
sudo chown -R root:root /var/log/automagik
```

6. Install service:
```bash
automagik install-service
sudo systemctl daemon-reload
sudo systemctl enable automagik
sudo systemctl start automagik
```

## Environment Configuration

Required variables in `.env`:

```bash
# API Key for AutoMagik API authentication
AUTOMAGIK_API_KEY=your-api-key

# PostgreSQL database URL
DATABASE_URL=postgresql://user:password@localhost:5432/automagik_db

# LangFlow configuration
LANGFLOW_API_URL=http://your-langflow-instance
LANGFLOW_API_KEY=your-langflow-api-key
```

## Logging Configuration

Logs are stored in:
- `/var/log/automagik/api.log`: API access logs
- `/var/log/automagik/error.log`: Error logs

## Service Management

Control the service:
```bash
# Start service
sudo systemctl start automagik

# Check status
sudo systemctl status automagik

# Stop service
sudo systemctl stop automagik

# View logs
tail -f /var/log/automagik/api.log
tail -f /var/log/automagik/error.log
```

## Troubleshooting

### Common Issues

1. **Database Connection**
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Ensure database and user exist

2. **Service Won't Start**
   - Check error logs
   - Verify environment variables
   - Ensure PostgreSQL and Redis are running

3. **Port Conflicts**
   - Check if port 8000 is in use
   - Find conflicting process: `sudo lsof -i :8000`
   - Stop process or change port

### Getting Help

If you encounter issues:
1. Check the error logs
2. Review environment configuration
3. Ensure all prerequisites are met
4. Contact support with log files
