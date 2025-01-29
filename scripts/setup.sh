    #!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to print status messages
print_status() {
    echo -e "[${GREEN}+${NC}] $1"
}

# Function to print error messages
print_error() {
    echo -e "[${RED}!${NC}] $1"
}

# Function to print warning messages
print_warning() {
    echo -e "[${YELLOW}!${NC}] $1"
}

# Function to prompt yes/no questions
prompt_yes_no() {
    local prompt="$1"
    local default="${2:-N}"

    if [ "$default" = "Y" ]; then
        prompt="$prompt [Y/n] "
    else
        prompt="$prompt [y/N] "
    fi

    read -r -p "$prompt" response
    response=${response:-$default}
    echo "$response" | grep -iq "^y"
}

# Function to download required files
download_files() {
    print_status "Downloading required files..."
    
    # Create necessary directories
    mkdir -p migrations
    
    # List of files to download with their source and destination paths
    declare -A FILES=(
        ["docker/docker-compose.prod.yml"]="docker-compose.yml"
        [".env.example"]=".env.example"
    )
    
    # Base URL for raw GitHub content
    BASE_URL="https://raw.githubusercontent.com/namastexlabs/automagik/main"
    
    # Download each file
    for src in "${!FILES[@]}"; do
        dest="${FILES[$src]}"
        dir=$(dirname "$dest")
        mkdir -p "$dir"
        if ! curl -sSL "$BASE_URL/$src" -o "$dest"; then
            print_error "Failed to download $src to $dest"
            return 1
        fi
    done
    
    return 0
}

# Function to check if we're on Ubuntu/Debian
check_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "$ID" == "ubuntu" ]] || [[ "$ID" == "debian" ]]; then
            return 0
        fi
    fi
    return 1
}

# Function to install Docker on Ubuntu/Debian
install_docker() {
    print_status "Installing Docker..."
    
    # Add Docker's official GPG key
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    
    # Add the repository to Apt sources
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker packages
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Add current user to docker group
    sudo usermod -aG docker "$USER"
    
    print_status "Docker installed successfully!"
    print_warning "You may need to log out and back in for Docker group changes to take effect."
    return 0
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_warning "Docker is not installed"
    if check_os; then
        if prompt_yes_no "Would you like to install Docker?" "Y"; then
            if ! install_docker; then
                print_error "Failed to install Docker"
                exit 1
            fi
        else
            print_error "Docker is required to continue. Please install Docker and try again."
            exit 1
        fi
    else
        print_error "Automatic Docker installation is only supported on Ubuntu/Debian."
        print_error "Please install Docker manually: https://docs.docker.com/engine/install/"
        exit 1
    fi
fi

# Function to create .env file
create_env_file() {
    if [ ! -f ".env.example" ]; then
        print_error ".env.example not found"
        return 1
    fi

    print_status "Creating .env file from example..."
    cp .env.example .env

    # Generate API key
    API_KEY=$(openssl rand -hex 32)
    sed -i "s/your-api-key-here/$API_KEY/" .env

    print_status "Environment file created successfully!"
    print_warning "Your API key is: $API_KEY"

    return 0
}

# Download required files
if ! download_files; then
    print_error "Failed to download required files"
    exit 1
fi

# Create .env file if it doesn't exist
create_env_file

# Create logs directory
print_status "Creating logs directory..."
mkdir -p logs

# Start services with docker compose
if [ "$INSTALL_LANGFLOW" = true ]; then
    print_status "Starting services with LangFlow..."
    docker compose -p automagik -f ./docker-compose.yml --profile langflow up -d automagik-db automagik-api
else
    print_status "Starting services..."
    docker compose -p automagik -f ./docker-compose.yml up -d automagik-db automagik-api
fi

# Wait for PostgreSQL
print_status "Waiting for PostgreSQL to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0
PG_READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if docker compose -p automagik -f ./docker-compose.yml exec -T automagik-db pg_isready -U automagik; then
        PG_READY=true
        break
    fi
    echo -n "."
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT + 1))
done
echo "" # New line after dots

if [ "$PG_READY" = false ]; then
    print_error "PostgreSQL failed to start. Checking logs..."
    docker compose -p automagik -f ./docker-compose.yml logs automagik-db
    exit 1
fi

# Wait for API to be ready
print_status "Waiting for API to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0
API_READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s -f http://localhost:8888/health > /dev/null; then
        API_READY=true
        break
    fi
    echo -n "."
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT + 1))
done
echo "" # New line after dots

if [ "$API_READY" = false ]; then
    print_error "API failed to start. Checking logs..."
    docker compose -p automagik -f ./docker-compose.yml logs automagik-api
    exit 1
fi

# Initialize database
print_status "Applying database migrations..."
sleep 5  # Give PostgreSQL a moment to fully initialize
if ! docker compose -p automagik -f ./docker-compose.yml exec -T automagik-api python -m automagik db upgrade; then
    print_error "Database migration failed. Checking logs..."
    docker compose -p automagik -f ./docker-compose.yml logs automagik-api
    exit 1
fi

# Start worker after migrations
print_status "Starting worker..."
docker compose -p automagik -f ./docker-compose.yml up -d automagik-worker

# Print AutoMagik ASCII art
cat << "EOF"                                                                                                                                                                                
       ██            ███████████  ████████   ███        ███     █       ▓███████ ░██▓ ███   ████    
       ███   ▓██     ██          ███    ▒██░ ████      ████    ███     ███        ██  ██▒  ███      
      ████    ██     ██   ███   ██        ██ █████    █████   █████   ███  █████  ██  ██  ██▒       
     ▓██ ██   ██     ██   ███   ██   ██▓  ██ ██ ███  ███ ██   ██ ██   ███  █████  ██  █████         
     ██  ███  ██     ██   ███   ███      ░██ ██  ██  ██ ███  ██▒  ██  ███     ██  ██  ███░███       
    ██░   ██  ████▒████   ███    ████  ████  ██   ████      ███   ███  █████ ▓██  ██  █▓   ███░     
   ███    ███   █████     ███      ██████    ██▒   ██      ███░    ███   ▓████████████       ███    
                                                                                                                                                                                                                                    
                                    Production Environment Setup
EOF

print_status "Setup completed successfully! "
print_status "You can access:"
print_status "- API: http://localhost:8888"
if [ "$INSTALL_LANGFLOW" = true ]; then
    print_status "- LangFlow: http://localhost:17860"
fi
print_status "- PostgreSQL: localhost:15432"
print_status ""

# Offer to install AutoMagik CLI
if prompt_yes_no "Would you like to install the AutoMagik CLI? (Recommended for managing flows and tasks)"; then
    print_status "Installing AutoMagik CLI..."
    if command -v python3 &> /dev/null; then
        if ! python3 -m pip install automagik; then
            print_error "Failed to install AutoMagik CLI"
        fi
    else
        print_error "Python 3 is required to install the AutoMagik CLI"
    fi
fi

print_status ""
print_status "To view logs:"
print_status "docker compose -p automagik -f ./docker-compose.yml logs -f"
print_status ""
print_status "To stop services:"
print_status "docker compose -p automagik -f ./docker-compose.yml down"
