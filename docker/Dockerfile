FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -e .

# Create directory for logs
RUN mkdir -p /root/.automagik/logs

# Copy entrypoint script
COPY scripts/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AUTOMAGIK_ENV=production

# Expose port for API
EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["api"]
