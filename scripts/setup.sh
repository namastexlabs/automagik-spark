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

# Check if we're on Ubuntu/Debian
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
    
    # Remove old versions
    sudo apt-get remove -y docker docker-engine docker.io containerd runc || true
    
    # Install prerequisites
    sudo apt-get update
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/$ID/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Set up the stable repository
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/$ID \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker Engine
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    # Add user to docker group
    sudo usermod -aG docker $USER
    print_warning "Please log out and back in for docker group changes to take effect"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_warning "Docker is not installed"
    if check_os; then
        if prompt_yes_no "Would you like to install Docker?"; then
            install_docker
        else
            print_error "Docker is required to run AutoMagik. Please install it manually."
            exit 1
        fi
    else
        print_error "Automatic Docker installation is only supported on Ubuntu and Debian."
        print_error "Please install Docker manually from https://docs.docker.com/engine/install/"
        exit 1
    fi
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    print_error "Docker Compose (V2) is not available. Please install it manually."
    exit 1
fi

# Create automagik directory
AUTOMAGIK_DIR="$HOME/.automagik"
mkdir -p "$AUTOMAGIK_DIR"
cd "$AUTOMAGIK_DIR"

# Download required files
print_status "Downloading required files..."
curl -fsSL -o docker-compose.yml https://raw.githubusercontent.com/namastexlabs/automagik/main/docker/docker-compose.yml
curl -fsSL -o .env.example https://raw.githubusercontent.com/namastexlabs/automagik/main/.env.example

# Function to create .env file from example
create_env_file() {
    if [ ! -f .env.example ]; then
        print_error ".env.example file not found"
        exit 1
    fi

    if [ -f .env ]; then
        print_warning "An existing .env file was found."
        if ! prompt_yes_no "Would you like to create a new one? (This will overwrite the existing file)"; then
            print_status "Keeping existing .env file."
            return
        fi
    fi

    print_status "Creating .env file from example..."
    cp .env.example .env
    
    # Generate a random API key
    API_KEY=$(openssl rand -hex 32)
    sed -i "s/AUTOMAGIK_API_KEY=.*/AUTOMAGIK_API_KEY=$API_KEY/" .env
    
    print_status "Environment file created successfully!"
    print_warning "Your API key is: $API_KEY"
}

# Create .env file if it doesn't exist
create_env_file

# Export environment variables
set -a
source .env
set +a

print_status "Creating logs directory..."
mkdir -p "$(dirname "$AUTOMAGIK_WORKER_LOG")"
touch "$AUTOMAGIK_WORKER_LOG"

# Check if LangFlow is already running
check_langflow() {
    if curl -s http://localhost:7860 > /dev/null; then
        print_status "LangFlow detected at http://localhost:7860"
        return 0
    elif curl -s http://localhost:17860 > /dev/null; then
        print_status "LangFlow detected at http://localhost:17860"
        return 0
    fi
    return 1
}

# Check if LangFlow is already running and ask to install if not
INSTALL_LANGFLOW=false
if ! check_langflow; then
    print_warning "LangFlow is not detected"
    if prompt_yes_no "Would you like to install LangFlow?"; then
        INSTALL_LANGFLOW=true
    fi
fi

# Start services with docker compose
if [ "$INSTALL_LANGFLOW" = true ]; then
    docker compose -p automagik -f docker-compose.yml --profile langflow --profile api pull && \
    docker compose -p automagik -f docker-compose.yml --profile langflow --profile api up -d
else
    docker compose -p automagik -f docker-compose.yml --profile api pull && \
    docker compose -p automagik -f docker-compose.yml --profile api up -d
fi

# Function to check container logs for errors
check_container_logs() {
    local container=$1
    local error_count=$(docker logs $container 2>&1 | grep -iE 'error|exception|fatal' | wc -l)
    if [ $error_count -gt 0 ]; then
        print_error "Found errors in $container logs:"
        docker logs $container 2>&1 | grep -iE 'error|exception|fatal'
        return 1
    fi
    return 0
}

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 5

# Wait for PostgreSQL
print_status "Waiting for PostgreSQL to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0
PG_READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if docker compose -p automagik -f docker-compose.yml exec -T automagik-db pg_isready -U automagik; then
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
    docker compose -p automagik -f docker-compose.yml logs automagik-db
    exit 1
fi

# Initialize database
print_status "Applying database migrations..."
if ! docker compose -p automagik -f docker-compose.yml exec -T automagik-api python -m automagik db upgrade; then
    print_error "Database migration failed. Checking logs..."
    docker compose -p automagik -f docker-compose.yml logs automagik-api
    exit 1
fi

# Check API
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
    docker compose -p automagik -f docker-compose.yml logs automagik-api
    exit 1
fi

# Start worker containers after API is ready
print_status "Starting worker containers..."
if [ "$INSTALL_LANGFLOW" = true ]; then
    docker compose -p automagik -f docker-compose.yml --profile langflow --profile worker up -d
else
    docker compose -p automagik -f docker-compose.yml --profile worker up -d
fi

# Check LangFlow if installed
if [ "$INSTALL_LANGFLOW" = true ]; then
    print_status "Waiting for LangFlow to be ready..."
    RETRY_COUNT=0
    LANGFLOW_READY=false

    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if curl -s http://localhost:17860 &> /dev/null; then
            LANGFLOW_READY=true
            break
        fi
        echo -n "."
        sleep 2
        RETRY_COUNT=$((RETRY_COUNT + 1))
    done
    echo "" # New line after dots

    if [ "$LANGFLOW_READY" = false ]; then
        print_error "LangFlow failed to start. Checking logs..."
        docker compose -p automagik -f docker-compose.yml logs langflow
        exit 1
    fi
fi

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

# Ask to install CLI
if prompt_yes_no "Would you like to install the AutoMagik CLI? (Recommended for managing flows and tasks)"; then
    print_status "Installing CLI..."
    # Check if Python 3.10 or higher is installed
    PYTHON_VERSION=$(python3 -c 'import sys; print("".join(map(str, sys.version_info[:2])))' 2>/dev/null || echo "0")
    if [ "$PYTHON_VERSION" = "0" ] || [ "$PYTHON_VERSION" -lt "310" ]; then
        print_warning "Python 3.10 or higher is required but not found."
        
        # Check if we can offer automatic installation
        if check_os; then
            if prompt_yes_no "Would you like to install Python 3.10?"; then
                print_status "Installing Python 3.10..."
                # Add deadsnakes PPA for Python 3.10
                if ! command -v add-apt-repository &> /dev/null; then
                    sudo apt-get update
                    sudo apt-get install -y software-properties-common
                fi
                sudo add-apt-repository -y ppa:deadsnakes/ppa
                sudo apt-get update
                sudo apt-get install -y python3.10 python3.10-venv python3.10-dev
            else
                print_error "Python 3.10 is required. Please install it manually."
                exit 1
            fi
        else
            print_error "Automatic Python installation is only supported on Ubuntu and Debian."
            print_error "Please install Python 3.10 manually."
            exit 1
        fi
    fi

    # Create virtual environment
    print_status "Creating virtual environment..."
    python3 -m venv ~/.automagik/venv
    source ~/.automagik/venv/bin/activate

    # Install AutoMagik with CLI dependencies
    print_status "Installing AutoMagik CLI..."
    pip install --upgrade pip
    pip install automagik

    print_status "CLI installed successfully! "
    print_status "You can now use commands like (after activating the venv with 'source ~/.automagik/venv/bin/activate'):"
    print_status "- automagik api"
    print_status "- automagik worker"
    print_status "- automagik flow list"
    print_status "- automagik task list"
fi

print_status ""
print_status "To view logs:"
print_status "docker compose -p automagik -f docker-compose.yml logs -f"
print_status ""
print_status "To stop services:"
print_status "docker compose -p automagik -f docker-compose.yml down"
