# AutoMagik API Documentation

This document covers the AutoMagik REST API endpoints and usage.

## Authentication

All API requests require an API key passed in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-api-key" http://your-server:8000/flows
```

## Endpoints

### Health Check

```http
GET /health
```

Returns API health status.

### Flows

#### List Flows
```http
GET /flows
```

Returns all available flows.

#### Get Flow
```http
GET /flows/{flow_id}
```

Returns details of a specific flow.

### Tasks

#### List Tasks
```http
GET /tasks
```

Query Parameters:
- `flow_id` (optional): Filter by flow
- `status` (optional): Filter by status
- `limit` (optional): Maximum number of tasks to return

#### Get Task
```http
GET /tasks/{task_id}
```

Returns task details including logs and output.

### Schedules

#### List Schedules
```http
GET /schedules
```

Query Parameters:
- `flow_id` (optional): Filter by flow

#### Get Schedule
```http
GET /schedules/{schedule_id}
```

Returns schedule details.

## Response Formats

### Flow Response
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "source": "string",
  "source_id": "string",
  "data": {},
  "created_at": "datetime",
  "updated_at": "datetime",
  "tags": ["string"]
}
```

### Task Response
```json
{
  "id": "string",
  "flow_id": "string",
  "status": "string",
  "input_data": {},
  "output_data": {},
  "tries": 0,
  "max_retries": 0,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Schedule Response
```json
{
  "id": "string",
  "flow_id": "string",
  "schedule_type": "string",
  "schedule_expr": "string",
  "flow_params": {},
  "status": "string",
  "next_run_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized (invalid API key)
- 404: Not Found
- 500: Internal Server Error

Error responses include:
```json
{
  "error_id": "string",
  "type": "string",
  "detail": "string"
}
```

## Rate Limiting

The API currently has no rate limiting but may be added in future versions.

## Best Practices

1. Always check response status codes
2. Include error handling in your code
3. Store API key securely
4. Log API responses for debugging
