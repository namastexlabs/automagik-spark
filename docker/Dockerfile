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

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AUTOMAGIK_ENV=production

# Expose port for API
EXPOSE 8000
