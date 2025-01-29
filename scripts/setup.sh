#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function to prompt yes/no questions
prompt_yes_no() {
    while true; do
        read -p "$1 [y/N] " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* | "" ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root"
    exit 1
fi

print_status "Starting AutoMagik setup..."

# Install basic system dependencies
print_status "Installing basic system dependencies..."
apt-get update
apt-get install -y python3-venv python3-pip lsof curl

# Optional PostgreSQL installation
if prompt_yes_no "Do you want to install PostgreSQL locally?"; then
    print_status "Installing PostgreSQL..."
    apt-get install -y postgresql postgresql-contrib
    
    # Start PostgreSQL service
    print_status "Starting PostgreSQL service..."
    systemctl start postgresql
    
    # Wait for service to be ready
    print_status "Waiting for PostgreSQL to be ready..."
    sleep 5
    
    # Check if PostgreSQL is running
    print_status "Checking PostgreSQL service..."
    if ! systemctl is-active --quiet postgresql; then
        print_error "PostgreSQL failed to start"
        exit 1
    fi
    
    # Configure PostgreSQL
    print_status "Configuring PostgreSQL..."
    # Create database user if it doesn't exist
    su - postgres -c "psql -c \"SELECT 1 FROM pg_roles WHERE rolname = 'automagik'\"" | grep -q 1 || \
        su - postgres -c "psql -c \"CREATE USER automagik WITH PASSWORD 'automagik';\""
    
    # Create database if it doesn't exist
    su - postgres -c "psql -lqt | cut -d \| -f 1 | grep -qw automagik" || \
        su - postgres -c "psql -c \"CREATE DATABASE automagik OWNER automagik;\""
    
    # Grant privileges
    su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE automagik TO automagik;\""
else
    print_warning "Skipping PostgreSQL installation. Make sure DATABASE_URL in .env points to your existing database."
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
pip install -e .

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning "Please update the .env file with your configuration"
    else
        print_error ".env.example file not found"
        exit 1
    fi
fi

# Load environment variables
set -a
source .env
set +a

# Test database connection
print_status "Testing database connection..."
if ! psql "${DATABASE_URL}" -c '\q' 2>/dev/null; then
    print_error "Could not connect to database. Please check your DATABASE_URL in .env"
    exit 1
fi

# Create log directory
print_status "Setting up logging..."
mkdir -p /var/log/automagik
chown -R root:root /var/log/automagik

# Check if port 8000 is in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    print_warning "Port 8000 is already in use. Stopping conflicting process..."
    lsof -ti :8000 | xargs kill -9
fi

# Setup git hooks
print_status "Setting up git hooks..."
git config core.hooksPath .githooks
chmod +x .githooks/pre-push
chmod +x scripts/run_tests.sh
print_status "Git hooks configured successfully"

# Install development dependencies
print_status "Installing development dependencies..."
pip install pytest pytest-cov

# Install systemd service
print_status "Installing systemd service..."
cat > /etc/systemd/system/automagik.service << EOL
[Unit]
Description=AutoMagik Service
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/automagik

# Environment setup
Environment=PATH=/root/automagik/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONPATH=/root/automagik
Environment=LOG_LEVEL=INFO
EnvironmentFile=/root/automagik/.env

# Logging
StandardOutput=append:/var/log/automagik/api.log
StandardError=append:/var/log/automagik/error.log

# Start command with proper logging
ExecStartPre=/bin/mkdir -p /var/log/automagik
ExecStartPre=/bin/chown -R root:root /var/log/automagik
ExecStart=/root/automagik/.venv/bin/uvicorn automagik.api.main:app --host 0.0.0.0 --port 8000 --log-level info

# Restart configuration
Restart=always
RestartSec=3

# Give the service time to start up
TimeoutStartSec=30

# Limit resource usage
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and enable service
print_status "Configuring service..."
systemctl daemon-reload
systemctl enable automagik
systemctl restart automagik

# Wait for service to start
print_status "Waiting for service to start..."
sleep 5

# Test API
print_status "Testing API..."
if curl -s -f -X GET "http://localhost:8000/health" -H "accept: application/json" > /dev/null; then
    print_status "API is running successfully!"
else
    print_error "API failed to start. Check logs at /var/log/automagik/error.log"
    exit 1
fi

print_status "Setup completed successfully!"
print_status "You can check the logs at:"
print_status "  - API logs: /var/log/automagik/api.log"
print_status "  - Error logs: /var/log/automagik/error.log"
print_status "To check service status: sudo systemctl status automagik"
