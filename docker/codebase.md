# docker-compose.yml

```yml
version: "3.8"

services:
  # Automagik's PostgreSQL
  automagik-db:
    image: postgres:16
    environment:
      POSTGRES_USER: automagik
      POSTGRES_PASSWORD: automagik
      POSTGRES_DB: automagik
    ports:
      - "5432:5432"
    volumes:
      - automagik-postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U automagik"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Database migrations
  automagik-migrations:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: ["sh", "-c", "cd /app && alembic upgrade head"]
    env_file: ../.env
    environment:
      DATABASE_URL: postgresql://automagik:automagik@automagik-db/automagik
    depends_on:
      automagik-db:
        condition: service_healthy

  langflow-init:
    image: busybox
    command: sh -c "mkdir -p /data/langflow && chown -R 1000:1000 /data/langflow"
    volumes:
      - langflow-data:/data

  langflow:
    image: langflowai/langflow:latest
    pull_policy: always
    user: "1000:1000"
    ports:
      - "7860:7860"
    environment:
      - LANGFLOW_DATABASE_URL=sqlite:////data/langflow/langflow.db
      - LANGFLOW_AUTO_LOGIN=true
      - LANGFLOW_CONFIG_DIR=/data/langflow
    volumes:
      - langflow-data:/data
    depends_on:
      langflow-init:
        condition: service_completed_successfully
      automagik-db:
        condition: service_healthy

  # Automagik API service
  automagik-api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: api
    env_file: ../.env
    environment:
      DATABASE_URL: postgresql://automagik:automagik@automagik-db/automagik
    ports:
      - "8000:8000"
    depends_on:
      automagik-migrations:
        condition: service_completed_successfully
      automagik-db:
        condition: service_healthy

  # Automagik Worker service
  automagik-worker:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: worker
    env_file: ../.env
    environment:
      DATABASE_URL: postgresql://automagik:automagik@automagik-db/automagik
    depends_on:
      automagik-migrations:
        condition: service_completed_successfully
      automagik-db:
        condition: service_healthy

  # Redis service
  # redis:
  #   image: redis:alpine
  #   ports:
  #     - "6379:6379"

volumes:
  automagik-postgres:
  langflow-data:
```

# docker-entrypoint.sh

```sh
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

```

# Dockerfile

```
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create directory for logs
RUN mkdir -p /root/.automagik/logs

# Copy entrypoint script
COPY docker/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AUTOMAGIK_ENV=production

# Expose port for API
EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["api"]

```

