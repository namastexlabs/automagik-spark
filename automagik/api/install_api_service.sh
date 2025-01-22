#!/bin/bash

# Make script executable
chmod +x "$0"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "Error: .env file not found in $PROJECT_ROOT"
    echo "Please create a .env file by copying .env.example and configuring the required environment variables:"
    echo "cp .env.example .env"
    echo "Then configure the environment variables in the .env file"
    exit 1
fi

# Check required environment variables
REQUIRED_VARS=(
    "AUTOMAGIK_API_KEY"
    "DATABASE_URL"
    "CELERY_BROKER_URL"
    "CELERY_RESULT_BACKEND"
)

for var in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "^${var}=" "$PROJECT_ROOT/.env"; then
        echo "Error: ${var} not found in .env file"
        echo "Please configure ${var} in your .env file"
        exit 1
    fi
done

# Install dependencies
echo "Installing dependencies..."
python3 -m venv "$PROJECT_ROOT/.venv"
source "$PROJECT_ROOT/.venv/bin/activate"
pip install -e "$PROJECT_ROOT"

# Copy service file
echo "Installing service file..."
cp "$SCRIPT_DIR/automagik-api.service" /etc/systemd/system/

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

# Enable and start service
echo "Enabling and starting service..."
systemctl enable automagik-api
systemctl restart automagik-api

echo "Installation complete."
echo "Check service status with: systemctl status automagik-api"
echo "Check logs with: journalctl -u automagik-api"
