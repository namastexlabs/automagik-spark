# AutoMagik Spark API Documentation for UI Implementation

## Overview

This documentation provides comprehensive examples and payloads for the AutoMagik Spark API, focusing on **workflow management across multiple source types** including AutoMagik Agents and AutoMagik Hive Multi-Agent Systems. All examples use real API responses from a running instance.

### Supported Source Types
- **AutoMagik Agents**: Traditional single-agent workflows from AutoMagik instances
- **AutoMagik Hive**: Multi-agent systems with agents, teams, and structured workflows
- **LangFlow**: Flow-based workflow systems (legacy support)

**Base URL**: `http://localhost:8883`  
**Authentication**: API Key via `X-API-Key` header  
**Test Credentials**: `spark_test_key`  

## API Health & Status

### Health Check
```bash
GET /health
```

**Response Example:**
```json
{
  "status": "degraded",
  "timestamp": "2025-08-14 19:13:05",
  "services": {
    "api": {
      "status": "healthy",
      "version": "0.3.6"
    },
    "worker": {
      "status": "error",
      "active_workers": 0,
      "available_tasks": [],
      "error": "Authentication required."
    },
    "redis": {
      "status": "unhealthy"
    }
  }
}
```

## Agent Discovery & Management

### 1. List Available Remote Agents

**Endpoint**: `GET /api/v1/workflows/remote`

```bash
curl -H "X-API-Key: spark_test_key" \
  "http://localhost:8883/api/v1/workflows/remote?source_url=http://localhost:8881"
```

**Response**: Array of available agents from AutoMagik instance
```json
[
  {
    "id": "simple",
    "name": "simple",
    "description": "Enhanced Simple Agent with multimodal capabilities.\n\nFeatures:\n- Image analysis and description\n- Document reading and summarization\n- Audio transcription (when supported)\n- Automatic model switching to vision-capable models\n- Built-in multimodal analysis tools",
    "origin": {
      "instance": "localhost:8881",
      "source_url": "http://localhost:8881"
    },
    "components": []
  },
  {
    "id": "prompt_maker",
    "name": "prompt_maker", 
    "description": "Enhanced Prompt Maker Agent for creating high-quality prompts.",
    "origin": {
      "instance": "localhost:8881",
      "source_url": "http://localhost:8881"
    },
    "components": []
  },
  {
    "id": "multimodal_specialist",
    "name": "multimodal_specialist",
    "description": "Multimodal Specialist Agent using Agno framework for superior multimodal processing.",
    "origin": {
      "instance": "localhost:8881", 
      "source_url": "http://localhost:8881"
    },
    "components": []
  }
]
```

**Available Agent Types:**
- `simple` - Basic conversational agent with multimodal capabilities
- `prompt_maker` - Specialized in creating high-quality prompts
- `multimodal_specialist` - Advanced multimodal content processing
- `discord` - Discord integration agent
- `sofia` - Meeting and Airtable integration agent
- `summary` - Document summarization agent
- Plus specialized architecture, security, and workflow agents

## AutoMagik Hive Multi-Agent Workflows

AutoMagik Hive provides three types of execution entities that can be imported as workflows:

### Entity Types
- **Agents** (`hive_agent`): Individual AI agents with specific capabilities
- **Teams** (`hive_team`): Multi-agent coordinated teams for complex tasks  
- **Workflows** (`hive_workflow`): Structured multi-step processes

### 1. List AutoMagik Hive Workflows

After adding an AutoMagik Hive source, workflows are automatically imported and appear in the standard workflows list:

**Endpoint**: `GET /api/v1/workflows`

**Example Response with Hive Workflows:**
```json
[
  {
    "id": "f9c38d51-56a4-42e8-8b0f-10b180345468",
    "name": "🧞 Master Genie - Ultimate Development Companion",
    "description": "The ultimate development companion with dual identity",
    "source": "AutoMagik Hive Local",
    "remote_flow_id": "master-genie",
    "flow_version": 1,
    "input_component": "input",
    "output_component": "output",
    "folder_name": "Agents",
    "icon": "🤖",
    "icon_bg_color": "#4F46E5",
    "tags": ["agent", "hive"],
    "data": {
      "type": "hive_agent",
      "model": {"name": "OpenAIChat", "model": "gpt-4o"},
      "tools": [],
      "memory": {"name": "Memory"},
      "storage": {"name": "PostgresStorage"}
    },
    "latest_run": "COMPLETED",
    "task_count": 2,
    "failed_task_count": 0
  },
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "🧞 Genie",
    "description": "Clean, efficient coordination through 3 domain specialists",
    "source": "AutoMagik Hive Local", 
    "remote_flow_id": "genie",
    "data": {
      "type": "hive_team",
      "mode": "coordinate",
      "members": [
        {"agent_id": "genie-dev", "name": "🧞 Genie Dev"},
        {"agent_id": "genie-testing", "name": "🧪 Genie Testing"},
        {"agent_id": "genie-quality", "name": "🔧 Genie Quality"}
      ],
      "members_count": 4
    },
    "folder_name": "Teams",
    "icon": "👥",
    "icon_bg_color": "#059669",
    "tags": ["team", "multi-agent", "hive"]
  }
]
```

### 2. Execute AutoMagik Hive Workflows

AutoMagik Hive workflows use the same execution API as other workflows:

**Endpoint**: `POST /api/v1/workflows/{workflow_id}/run`

**Agent Execution Example:**
```bash
curl -X POST -H "X-API-Key: spark_test_key" \
  -H "Content-Type: application/json" \
  -d '"Please provide a helpful development tip."' \
  "http://localhost:8883/api/v1/workflows/f9c38d51-56a4-42e8-8b0f-10b180345468/run"
```

**Team Execution Example:**
```bash
curl -X POST -H "X-API-Key: spark_test_key" \
  -H "Content-Type: application/json" \
  -d '"Create a complete REST API with authentication, database models, and tests"' \
  "http://localhost:8883/api/v1/workflows/a1b2c3d4-e5f6-7890-abcd-ef1234567890/run"
```

**Response Format:**
```json
{
  "id": "ddabe5c6-672a-466f-b24b-74f233788238",
  "workflow_id": "f9c38d51-56a4-42e8-8b0f-10b180345468",
  "status": "completed",
  "input_data": {"value": "Please provide a helpful development tip."},
  "output_data": {
    "result": "Hello! Here's a development tip that can help optimize your workflow: **Automate Frequent Tasks with Scripts or Tools.** Identify tasks that you do repeatedly...",
    "session_id": "91e43347-0ab3-4f0a-93ef-550ea4ad04da_master-genie",
    "run_id": "run_abc123",
    "agent_id": "master-genie",
    "metadata": {"tokens_used": 250, "duration_ms": 4500},
    "status": "completed",
    "success": true
  },
  "started_at": "2025-08-15T17:39:00.007846Z",
  "finished_at": "2025-08-15T17:39:05.019619Z",
  "created_at": "2025-08-15T17:39:00.007848Z"
}
```

### 3. Schedule AutoMagik Hive Workflows

AutoMagik Hive workflows support the same scheduling capabilities:

**Example - Schedule Master Genie for Daily Tips:**
```bash
curl -X POST -H "X-API-Key: spark_test_key" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "f9c38d51-56a4-42e8-8b0f-10b180345468",
    "schedule_type": "cron",
    "schedule_expr": "0 9 * * *",
    "input_value": "Provide a daily development tip for the team."
  }' \
  "http://localhost:8883/api/v1/schedules"
```

### 4. AutoMagik Hive Workflow Types

**Agent Workflows (`hive_agent`)**
- Single AI agent execution
- Personalized with memory and storage
- Tool integration capabilities
- Session continuity support

**Team Workflows (`hive_team`)**  
- Multi-agent coordination
- Coordinator + member agent responses
- Specialized domain experts
- Complex task decomposition

**Structured Workflows (`hive_workflow`)**
- Multi-step orchestrated processes
- Step-by-step execution tracking
- Workflow-specific input/output handling
- Process automation capabilities

### 2. Get Specific Remote Agent Details

**Endpoint**: `GET /api/v1/workflows/remote/{agent_id}`

```bash
curl -H "X-API-Key: spark_test_key" \
  "http://localhost:8883/api/v1/workflows/remote/simple?source_url=http://localhost:8881"
```

### 3. Sync Agent from Remote Source

**Endpoint**: `POST /api/v1/workflows/sync/{agent_id}`

```bash
curl -X POST -H "X-API-Key: spark_test_key" \
  "http://localhost:8883/api/v1/workflows/sync/simple?input_component=input&output_component=output"
```

**Response**: Synced agent details
```json
{
  "id": "90e0325b-e222-4956-9ac8-43d50af22be5",
  "name": "simple",
  "description": "Enhanced Simple Agent with multimodal capabilities...",
  "source": "http://localhost:8881",
  "remote_flow_id": "simple",
  "flow_version": 1,
  "input_component": "input",
  "output_component": "output",
  "workflow_source_id": "10eabadf-4f89-4261-a08f-5e4535b65cde",
  "created_at": "2025-08-14T19:33:03.401883+00:00",
  "updated_at": "2025-08-14T22:04:25.589545+00:00",
  "schedules": []
}
```

## Local Agent Management

### 1. List Synchronized Agents

**Endpoint**: `GET /api/v1/workflows`

```bash
curl -H "X-API-Key: spark_test_key" http://localhost:8883/api/v1/workflows
```

**Response**: Array of local agents
```json
[
  {
    "name": "simple",
    "description": "Enhanced Simple Agent with multimodal capabilities...",
    "source": "http://localhost:8881",
    "remote_flow_id": "simple",
    "flow_version": 1,
    "input_component": "input",
    "output_component": "output",
    "id": "90e0325b-e222-4956-9ac8-43d50af22be5",
    "created_at": "2025-08-14T19:33:03.401883Z",
    "updated_at": "2025-08-14T22:04:25.589545Z",
    "latest_run": "COMPLETED",
    "task_count": 5,
    "failed_task_count": 4
  },
  {
    "name": "prompt_maker",
    "description": "Enhanced Prompt Maker Agent for creating high-quality prompts.",
    "source": "http://localhost:8881",
    "remote_flow_id": "prompt_maker",
    "id": "dfeb2f68-9f35-4fe9-976b-6ded5d954f4c",
    "latest_run": "COMPLETED",
    "task_count": 1,
    "failed_task_count": 0
  }
]
```

### 2. Get Specific Agent

**Endpoint**: `GET /api/v1/workflows/{agent_id}`

```bash
curl -H "X-API-Key: spark_test_key" \
  http://localhost:8883/api/v1/workflows/90e0325b-e222-4956-9ac8-43d50af22be5
```

### 3. Delete Agent

**Endpoint**: `DELETE /api/v1/workflows/{agent_id}`

```bash
curl -X DELETE -H "X-API-Key: spark_test_key" \
  http://localhost:8883/api/v1/workflows/90e0325b-e222-4956-9ac8-43d50af22be5
```

## Agent Execution

### 1. Run Agent with Input

**Endpoint**: `POST /api/v1/workflows/{agent_id}/run`

```bash
curl -X POST -H "X-API-Key: spark_test_key" \
  -H "Content-Type: application/json" \
  -d '"What is the capital of France?"' \
  "http://localhost:8883/api/v1/workflows/90e0325b-e222-4956-9ac8-43d50af22be5/run"
```

**Request Body**: Simple string input
```json
"What is the capital of France?"
```

**Response**: Task execution details
```json
{
  "workflow_id": "90e0325b-e222-4956-9ac8-43d50af22be5",
  "input_data": {
    "value": "What is the capital of France?"
  },
  "output_data": {
    "value": "The capital of France is Paris."
  },
  "error": null,
  "tries": 0,
  "max_retries": 3,
  "next_retry_at": null,
  "started_at": "2025-08-14T22:15:05.733473Z",
  "finished_at": "2025-08-14T22:15:10.376064Z",
  "id": "07412ae1-6ff2-46e5-ab47-9dd38a1c5da9",
  "status": "completed",
  "created_at": "2025-08-14T22:15:05.733803Z",
  "updated_at": "2025-08-14T22:15:10.376448Z"
}
```

**Input Types for Different Agents:**
- **Simple Agent**: Plain text questions, instructions
- **Prompt Maker**: Description of desired prompt type
- **Multimodal Specialist**: Text + file references, image descriptions
- **Summary Agent**: Text or document content to summarize

## Task Management

### 1. List Tasks

**Endpoint**: `GET /api/v1/tasks`

```bash
curl -H "X-API-Key: spark_test_key" http://localhost:8883/api/v1/tasks
```

**Query Parameters:**
- `workflow_id` (optional): Filter by specific agent
- `status` (optional): Filter by status (pending, running, completed, failed)
- `limit` (optional): Number of tasks to return (default: 50)

**Response**: Array of task executions
```json
[
  {
    "workflow_id": "dfeb2f68-9f35-4fe9-976b-6ded5d954f4c",
    "input_data": "Create a prompt for writing a professional email",
    "output_data": "To help you create a prompt for writing a professional email...",
    "error": null,
    "tries": 0,
    "max_retries": 3,
    "next_retry_at": null,
    "started_at": "2025-08-14T22:06:19.987600Z",
    "finished_at": "2025-08-14T22:06:36.023260Z",
    "id": "d1f449a2-0a27-40ca-bc91-358cfce92fc5",
    "status": "completed",
    "created_at": "2025-08-14T22:06:19.987988Z",
    "updated_at": "2025-08-14T22:06:36.023647Z"
  }
]
```

### 2. Get Specific Task

**Endpoint**: `GET /api/v1/tasks/{task_id}`

### 3. Delete Task

**Endpoint**: `DELETE /api/v1/tasks/{task_id}`

## Schedule Management

### 1. List Schedules

**Endpoint**: `GET /api/v1/schedules`

```bash
curl -H "X-API-Key: spark_test_key" http://localhost:8883/api/v1/schedules
```

**Response**: Array of active schedules
```json
[
  {
    "id": "32c82946-93e4-4344-b115-07fa30367885",
    "workflow_id": "90e0325b-e222-4956-9ac8-43d50af22be5",
    "schedule_type": "interval",
    "schedule_expr": "10m",
    "input_value": null,
    "status": "active",
    "next_run_at": "2025-08-14T19:45:54.895927Z",
    "created_at": "2025-08-14T22:35:54.897818Z",
    "updated_at": "2025-08-14T22:35:54.897820Z"
  },
  {
    "id": "b64d7718-a07b-4f72-aab9-e508f73e63c7",
    "workflow_id": "90e0325b-e222-4956-9ac8-43d50af22be5",
    "schedule_type": "cron",
    "schedule_expr": "*/15 * * * *",
    "input_value": null,
    "status": "active",
    "next_run_at": "2025-08-14T19:45:00Z",
    "created_at": "2025-08-14T22:35:59.783684Z",
    "updated_at": "2025-08-14T22:35:59.783686Z"
  }
]
```

### 2. Create Schedule

**Endpoint**: `POST /api/v1/schedules`

```bash
curl -X POST -H "X-API-Key: spark_test_key" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "90e0325b-e222-4956-9ac8-43d50af22be5",
    "schedule_type": "interval",
    "schedule_expr": "30m",
    "input_value": "Tell me a random fact about science"
  }' \
  "http://localhost:8883/api/v1/schedules"
```

**Request Body Schema:**
```json
{
  "workflow_id": "string",           // Required: Agent ID to schedule
  "schedule_type": "interval|cron",  // Required: Schedule type
  "schedule_expr": "string",         // Required: Expression (e.g., "30m", "0 9 * * *")
  "input_value": "string"            // Optional: Input to send to agent
}
```

**Schedule Expression Examples:**
- **Interval**: `"5m"`, `"1h"`, `"30s"`, `"2d"`
- **Cron**: `"0 9 * * *"` (daily at 9 AM), `"*/15 * * * *"` (every 15 minutes)

**Response**: Created schedule
```json
{
  "id": "c604192f-c921-4139-9002-043eec756501",
  "workflow_id": "90e0325b-e222-4956-9ac8-43d50af22be5",
  "schedule_type": "interval",
  "schedule_expr": "30m",
  "input_value": null,
  "status": "active",
  "next_run_at": "2025-08-14T22:45:16.072757Z",
  "created_at": "2025-08-14T22:15:16.073180",
  "updated_at": "2025-08-14T22:15:16.073182"
}
```

### 3. Get Schedule

**Endpoint**: `GET /api/v1/schedules/{schedule_id}`

### 4. Update Schedule

**Endpoint**: `PUT /api/v1/schedules/{schedule_id}`

### 5. Delete Schedule

**Endpoint**: `DELETE /api/v1/schedules/{schedule_id}`

```bash
curl -X DELETE -H "X-API-Key: spark_test_key" \
  "http://localhost:8883/api/v1/schedules/c604192f-c921-4139-9002-043eec756501"
```

### 6. Enable/Disable Schedule

**Enable**: `POST /api/v1/schedules/{schedule_id}/enable`  
**Disable**: `POST /api/v1/schedules/{schedule_id}/disable`

## Source Management

### 1. List Sources

**Endpoint**: `GET /api/v1/sources`

### 2. Add Source

**Endpoint**: `POST /api/v1/sources`

**AutoMagik Agents Source:**
```bash
curl -X POST -H "X-API-Key: spark_test_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AutoMagik Local",
    "source_type": "automagik-agents",
    "url": "http://localhost:8881",
    "api_key": "namastex888"
  }' \
  "http://localhost:8883/api/v1/sources"
```

**AutoMagik Hive Source:**
```bash
curl -X POST -H "X-API-Key: spark_test_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AutoMagik Hive Local",
    "source_type": "automagik-hive",
    "url": "http://localhost:8886",
    "api_key": "hive_namastex888"
  }' \
  "http://localhost:8883/api/v1/sources"
```

## Error Handling

### Common HTTP Status Codes
- `200`: Success
- `401`: Unauthorized (invalid/missing API key)
- `404`: Resource not found
- `422`: Validation error (invalid request data)
- `500`: Internal server error

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Validation Error Format
```json
{
  "detail": [
    {
      "loc": ["field_name"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

## UI Implementation Guidelines

### 1. Workflow Discovery Flow
1. **Connect to Source**: Add AutoMagik Agents or AutoMagik Hive instance via sources API
2. **Browse Workflows**: List available workflows (agents, teams, or structured workflows) with descriptions
3. **Preview Workflow**: Show workflow capabilities, type (`hive_agent`, `hive_team`, `hive_workflow`), and example inputs
4. **Auto-Import**: Workflows are automatically imported when source is added (no manual sync required for Hive)

### 2. Workflow Execution Flow  
1. **Select Workflow**: Choose from available workflows (agents, teams, structured workflows)
2. **Provide Input**: Text input appropriate for workflow type:
   - **Agents**: Direct conversational input
   - **Teams**: Complex task descriptions for multi-agent coordination
   - **Structured Workflows**: Task-specific input based on workflow requirements
3. **Execute**: Run workflow and get task ID
4. **Monitor**: Poll task status until completion
5. **View Results**: Display workflow output and execution details with type-specific formatting

### 3. Schedule Management Flow
1. **Select Workflow**: Choose workflow to schedule (supports all types: agents, teams, structured workflows)
2. **Configure Schedule**: Set interval or cron expression
3. **Set Input**: Optional default input for scheduled runs
4. **Manage**: Enable/disable, update, or delete schedules
5. **Monitor**: View scheduled task executions and results

### 4. Recommended UI Components

**Workflow Browser**
- Grid/list view of available workflows with type indicators
- Search and filter by workflow type (`hive_agent`, `hive_team`, `hive_workflow`)
- Workflow description, source, and examples
- Visual differentiation for agents (🤖), teams (👥), and workflows (⚡)

**Workflow Executor**
- Input form with workflow-specific placeholders and guidance
- Real-time execution status with progress indicators
- Output display with type-specific formatting:
  - **Agent results**: Direct response content
  - **Team results**: Coordinator + member responses
  - **Workflow results**: Step-by-step execution details
- Execution history with filtering

**Schedule Manager**
- Schedule creation wizard
- Calendar view of upcoming runs
- Schedule status controls
- Execution logs and monitoring

**Task Monitor**
- Real-time task status updates
- Filtering by agent, status, date
- Detailed task information
- Retry and cancel controls

### 5. Real-time Updates

For real-time UI updates, consider:
- **Polling**: Regular API calls to check task/schedule status
- **WebSocket**: If available, for real-time notifications
- **Server-Sent Events**: For streaming updates

### 6. Authentication

- Store API key securely (environment variables, secure storage)
- Include `X-API-Key` header in all requests
- Handle 401 errors gracefully with re-authentication

This documentation provides all the necessary API endpoints, request/response examples, and implementation guidance for building a comprehensive UI for AutoMagik Spark agent management.