# AutoMagik

AutoMagik is an AI-powered automation tool that helps you create and run workflows using LangFlow and other AI services.

## Quick Start with Docker (Recommended)

The easiest way to get started with AutoMagik is using Docker Compose:

1. Clone the repository:
```bash
git clone https://github.com/namastexlabs/automagik.git
cd automagik
```

2. Create a `.env` file with your configuration:
```bash
cp .env.example .env
```

3. Start the services:
```bash
docker compose up -d
```

This will start:
- LangFlow UI at http://localhost:7860
- AutoMagik API at http://localhost:8000
- AutoMagik CLI (accessible through docker exec)

### Using AutoMagik with Docker

1. Access LangFlow UI:
   - Open http://localhost:7860 in your browser
   - Use the default credentials or set your own in `.env`:
     ```
     LANGFLOW_API_KEY=your-api-key
     ```

2. Run AutoMagik commands:
```bash
# Using docker exec
docker exec -it automagik-cli automagik --help

# Or using docker run
docker run --rm -it --network automagik_default \
  -e LANGFLOW_API_URL=http://langflow:7860 \
  -e LANGFLOW_API_KEY=your-api-key \
  namastexlabs/automagik-cli automagik --help
```

## Alternative Installation Methods

### Local Installation

If you prefer to run AutoMagik locally:

1. Install Python 3.10 or later

2. Install `uv` (recommended):
```bash
# On Unix-like systems
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

3. Install AutoMagik using `uv`:
```bash
uv pip install automagik
```

Alternatively, you can use pip:
```bash
pip install automagik
```

4. Set up environment variables:
```bash
export LANGFLOW_API_URL=http://localhost:7860
export LANGFLOW_API_KEY=your-api-key
```

5. Run AutoMagik:
```bash
automagik --help
```

## Development

For development setup:

1. Clone the repository:
```bash
git clone https://github.com/namastexlabs/automagik.git
cd automagik
```

2. Create and activate a virtual environment using `uv`:
```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

## License

[MIT License](LICENSE)
