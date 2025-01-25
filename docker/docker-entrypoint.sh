#!/bin/bash
set -e

# Function to wait for database
wait_for_db() {
    echo "Waiting for database to be ready..."
    while ! automagik db init 2>/dev/null; do
        echo "Database not ready. Retrying in 5 seconds..."
        sleep 5
    done
    echo "Database is ready!"
}

# Initialize and migrate database
init_db() {
    echo "Initializing database..."
    automagik db init
    echo "Running database migrations..."
    automagik db upgrade
}

# Start services based on command
case "$1" in
    api)
        wait_for_db
        init_db
        echo "Starting API server..."
        exec automagik api --host 0.0.0.0 --port 8000
        ;;
    worker)
        wait_for_db
        init_db
        echo "Starting worker..."
        exec automagik worker start
        ;;
    *)
        exec "$@"
        ;;
esac
