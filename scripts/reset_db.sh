
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

# Drop and recreate database
print_status "Dropping existing database..."
PGPASSWORD=automagik psql -h localhost -p 15432 -U automagik -d postgres -c "DROP DATABASE IF EXISTS automagik;"

print_status "Creating fresh database..."
PGPASSWORD=automagik psql -h localhost -p 15432 -U automagik -d postgres -c "CREATE DATABASE automagik;"

print_status "Initializing database..."
if ! automagik db init; then
    print_error "Database initialization failed."
    exit 1
fi

print_status "Applying migrations..."
if ! automagik db upgrade; then
    print_error "Database migration failed."
    exit 1
fi

print_status "Database reset completed successfully! 🎉"
