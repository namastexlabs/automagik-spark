FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the package
RUN uv pip install --system --no-cache -e .

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Run database migrations and start the application
CMD ["sh", "-c", "alembic upgrade head && automagik run"]
