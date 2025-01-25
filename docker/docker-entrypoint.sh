#!/bin/bash
set -e

# Start services based on command
case "$1" in
    api)
        echo "Starting API server..."
        exec automagik api --host 0.0.0.0 --port 8000
        ;;
    worker)
        echo "Starting worker..."
        exec automagik worker start
        ;;
    *)
        exec "$@"
        ;;
esac
