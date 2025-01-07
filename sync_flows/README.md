# Sync Flows CLI Tool

This tool allows you to sync flows from a Langflow server to your local database.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following variables:
```env
LANGFLOW_API_URL=http://your-langflow-server/api/v1
LANGFLOW_API_KEY=your-api-key-if-required
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## Usage

Run the sync tool:
```bash
python sync_flows.py
```

The tool will:
1. Connect to your Langflow server
2. Display available flows
3. Let you select a flow to sync
4. Store or update the flow in your local database

## Database Schema

The flows table contains:
- `id`: Primary key
- `name`: Flow name
- `description`: Flow description
- `data`: Flow data (JSON)
- `source`: Source system (e.g., "langflow")
- `source_id`: ID from the source system
- `flow_version`: Version number (increments on updates)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
