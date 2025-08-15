# Automagik Hive API Documentation

## Base URL
```
http://localhost:8886
```

## Authentication
- **API Key**: Use header `x-api-key: {your_api_key}` (optional in dev mode)
- **Default Key**: `hive_namastex888` (development only)

## Table of Contents
1. [Core Endpoints](#core-endpoints)
2. [Agent Endpoints](#agent-endpoints)
3. [Team Endpoints](#team-endpoints)
4. [Workflow Endpoints](#workflow-endpoints)
5. [Version Management](#version-management)
6. [MCP Integration](#mcp-integration)

---

## Core Endpoints

### Health Check
Check if the API service is running and healthy.

**Endpoint:** `GET /api/v1/health`

**Response:**
```json
{
    "status": "success",
    "service": "Automagik Hive Multi-Agent System",
    "router": "health",
    "path": "/health",
    "utc": "2025-08-15T15:07:39.222047+00:00",
    "message": "System operational"
}
```

**cURL Example:**
```bash
curl http://localhost:8886/api/v1/health
```

### Playground Status
Get the overall playground status and configuration.

**Endpoint:** `GET /playground/status`

**Query Parameters:**
- `app_id` (optional): Specific application ID to check

**Response:**
```json
{
    "status": "running",
    "app_id": "automagik-hive",
    "agents_loaded": 6,
    "teams_loaded": 2,
    "workflows_loaded": 1,
    "database": "connected",
    "mcp_servers": ["claude-mcp", "postgres", "zen"]
}
```

---

## Agent Endpoints

### List All Agents
Get a list of all available agents with their configurations.

**Endpoint:** `GET /playground/agents`

**Response:**
```json
[
    {
        "agent_id": "master-genie",
        "name": "🧞 Master Genie - Ultimate Development Companion",
        "model": {
            "name": "OpenAIChat",
            "model": "gpt-4o",
            "provider": "OpenAI gpt-4o"
        },
        "add_context": true,
        "tools": [],
        "memory": {
            "name": "Memory",
            "model": {
                "name": "OpenAIChat",
                "model": "gpt-4.1-mini",
                "provider": "OpenAI"
            },
            "db": {
                "name": "PostgresMemoryDb",
                "table_name": "agent_memories_master-genie",
                "schema": "agno"
            }
        },
        "storage": {
            "name": "PostgresStorage"
        },
        "description": "The ultimate development companion with dual identity",
        "instructions": null
    }
]
```

### Run Agent
Execute a specific agent with a message.

**Endpoint:** `POST /playground/agents/{agent_id}/runs`

**Path Parameters:**
- `agent_id`: The ID of the agent to run (e.g., "master-genie")

**Request Body:**
```json
{
    "message": "Help me implement a user authentication system",
    "session_id": "optional-session-id",
    "user_id": "optional-user-id",
    "stream": false,
    "context": {
        "additional": "context if needed"
    }
}
```

**Response:**
```json
{
    "run_id": "run_abc123",
    "agent_id": "master-genie",
    "session_id": "session_xyz789",
    "response": {
        "content": "I'll help you implement a user authentication system! Let me break this down...",
        "metadata": {
            "tokens_used": 250,
            "model": "gpt-4o",
            "duration_ms": 1500
        }
    },
    "status": "completed"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8886/playground/agents/master-genie/runs \
  -H "Content-Type: application/json" \
  -H "x-api-key: hive_namastex888" \
  -d '{
    "message": "Help me implement a user authentication system",
    "stream": false
  }'
```

### Continue Agent Conversation
Continue an existing conversation with an agent.

**Endpoint:** `POST /playground/agents/{agent_id}/runs/{run_id}/continue`

**Path Parameters:**
- `agent_id`: The agent ID
- `run_id`: The previous run ID to continue from

**Request Body:**
```json
{
    "message": "Can you add OAuth2 support to that authentication system?"
}
```

### Get Agent Sessions
Retrieve all conversation sessions for a specific agent.

**Endpoint:** `GET /playground/agents/{agent_id}/sessions`

**Response:**
```json
[
    {
        "session_id": "session_xyz789",
        "agent_id": "master-genie",
        "user_id": "user123",
        "created_at": "2025-08-15T10:00:00Z",
        "updated_at": "2025-08-15T10:30:00Z",
        "message_count": 5,
        "name": "Authentication Implementation"
    }
]
```

### Get Agent Memories
Retrieve stored memories for an agent.

**Endpoint:** `GET /playground/agents/{agent_id}/memories`

**Query Parameters:**
- `user_id`: User ID to filter memories
- `limit`: Maximum number of memories to return (default: 10)

**Response:**
```json
[
    {
        "memory_id": "mem_123",
        "content": "User prefers JWT tokens for authentication",
        "created_at": "2025-08-15T10:00:00Z",
        "metadata": {
            "topic": "authentication",
            "importance": "high"
        }
    }
]
```

---

## Team Endpoints

### List All Teams
Get all available teams with their configurations.

**Endpoint:** `GET /playground/teams`

**Response:**
```json
[
    {
        "team_id": "genie",
        "name": "🧞 Genie",
        "description": "Clean, efficient coordination through 3 domain specialists",
        "mode": "coordinate",
        "model": {
            "name": "OpenAIChat",
            "model": "gpt-4o",
            "provider": "OpenAI"
        },
        "members": [
            {
                "agent_id": "genie-dev",
                "name": "🧞 Genie Dev - Development Domain Coordinator"
            },
            {
                "agent_id": "genie-testing",
                "name": "🧪 Genie Testing - Testing Domain Coordinator"
            },
            {
                "agent_id": "genie-quality",
                "name": "🔧 Genie Quality - Code Quality Domain Coordinator"
            },
            {
                "agent_id": "master-genie",
                "name": "🧞 Master Genie - Ultimate Development Companion"
            }
        ],
        "storage": {
            "name": "PostgresStorage"
        },
        "memory": {
            "name": "Memory",
            "db": {
                "name": "PostgresMemoryDb",
                "table_name": "team_memories_genie",
                "schema": "agno"
            }
        }
    }
]
```

### Run Team
Execute a team to handle complex multi-agent tasks.

**Endpoint:** `POST /playground/teams/{team_id}/runs`

**Path Parameters:**
- `team_id`: The team ID (e.g., "genie")

**Request Body:**
```json
{
    "message": "Create a complete REST API with authentication, database models, and tests",
    "session_id": "optional-session-id",
    "user_id": "optional-user-id",
    "stream": false,
    "mode": "coordinate",
    "context": {
        "project_type": "fastapi",
        "database": "postgresql"
    }
}
```

**Response:**
```json
{
    "run_id": "team_run_456",
    "team_id": "genie",
    "session_id": "team_session_789",
    "coordinator_response": {
        "content": "I'll coordinate the team to build your complete REST API!",
        "agent_assignments": [
            {
                "agent": "genie-dev",
                "task": "Design and implement API structure"
            },
            {
                "agent": "genie-testing",
                "task": "Create comprehensive test suite"
            }
        ]
    },
    "member_responses": [
        {
            "agent_id": "genie-dev",
            "response": "Created API structure with authentication endpoints..."
        },
        {
            "agent_id": "genie-testing",
            "response": "Implemented unit and integration tests..."
        }
    ],
    "status": "completed"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8886/playground/teams/genie/runs \
  -H "Content-Type: application/json" \
  -H "x-api-key: hive_namastex888" \
  -d '{
    "message": "Create a REST API with authentication",
    "stream": false
  }'
```

### Get Team Sessions
Retrieve all sessions for a specific team.

**Endpoint:** `GET /playground/teams/{team_id}/sessions`

### Get Team Memories
Retrieve stored memories for a team.

**Endpoint:** `GET /playground/team/{team_id}/memories`

---

## Workflow Endpoints

### List All Workflows
Get all available workflows.

**Endpoint:** `GET /playground/workflows`

**Response:**
```json
[
    {
        "workflow_id": "template-workflow",
        "name": "template_workflow",
        "description": "Template workflow demonstrating all Agno Workflows 2.0 features"
    }
]
```

### Get Workflow Details
Get detailed information about a specific workflow.

**Endpoint:** `GET /playground/workflows/{workflow_id}`

**Response:**
```json
{
    "workflow_id": "template-workflow",
    "name": "template_workflow",
    "description": "Template workflow demonstrating all Agno Workflows 2.0 features",
    "steps": [
        {
            "step_id": "analyze",
            "agent_id": "genie-dev",
            "description": "Analyze requirements"
        },
        {
            "step_id": "implement",
            "agent_id": "genie-dev",
            "description": "Implement solution"
        },
        {
            "step_id": "test",
            "agent_id": "genie-testing",
            "description": "Create and run tests"
        }
    ]
}
```

### Run Workflow
Execute a workflow with multiple steps.

**Endpoint:** `POST /playground/workflows/{workflow_id}/runs`

**Request Body:**
```json
{
    "input_data": {
        "requirements": "Build a user management system",
        "technology_stack": "Python/FastAPI",
        "include_tests": true
    },
    "session_id": "optional-session-id",
    "user_id": "optional-user-id"
}
```

**Response:**
```json
{
    "run_id": "workflow_run_123",
    "workflow_id": "template-workflow",
    "session_id": "workflow_session_456",
    "steps_completed": [
        {
            "step_id": "analyze",
            "status": "completed",
            "output": "Requirements analyzed successfully"
        },
        {
            "step_id": "implement",
            "status": "completed",
            "output": "Implementation completed"
        },
        {
            "step_id": "test",
            "status": "completed",
            "output": "Tests created and passing"
        }
    ],
    "final_output": "User management system successfully created with full test coverage",
    "status": "completed"
}
```

---

## Version Management

### Get All Components
List all components with their versions.

**Endpoint:** `GET /api/v1/version/components`

**Response:**
```json
[
    {
        "component_id": "master-genie",
        "component_type": "agent",
        "name": "Master Genie",
        "current_version": "2",
        "versions_available": ["1", "2"]
    }
]
```

### Get Components by Type
Filter components by type (agent, team, workflow).

**Endpoint:** `GET /api/v1/version/components/by-type/{component_type}`

**Path Parameters:**
- `component_type`: One of "agent", "team", or "workflow"

---

## MCP Integration

### MCP Status
Check Model Context Protocol server status.

**Endpoint:** `GET /api/v1/mcp/status`

**Response:**
```json
{
    "status": "connected",
    "servers": ["claude-mcp", "postgres", "zen"],
    "active_connections": 3
}
```

### List MCP Servers
Get all configured MCP servers.

**Endpoint:** `GET /api/v1/mcp/servers`

**Response:**
```json
[
    {
        "name": "claude-mcp",
        "status": "connected",
        "tools_available": ["Task", "Read", "Write", "Bash"]
    },
    {
        "name": "postgres",
        "status": "connected",
        "tools_available": ["query"]
    },
    {
        "name": "zen",
        "status": "connected",
        "tools_available": ["chat", "debug", "analyze"]
    }
]
```

---

## Streaming Responses

For real-time responses, add `"stream": true` to any agent/team/workflow run request.

**Example with Server-Sent Events:**
```bash
curl -N -X POST http://localhost:8886/playground/agents/master-genie/runs \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Help me build a feature",
    "stream": true
  }'
```

**Response format (SSE):**
```
data: {"type": "thinking", "content": "Analyzing requirements..."}

data: {"type": "content", "content": "I'll help you build that feature. Let me break it down:"}

data: {"type": "content", "content": "1. First, we need to..."}

data: {"type": "complete", "run_id": "run_123", "status": "completed"}
```

---

## Error Responses

All endpoints return standard error responses:

```json
{
    "error": {
        "type": "validation_error",
        "message": "Invalid agent_id provided",
        "details": {
            "agent_id": "unknown-agent",
            "available_agents": ["master-genie", "genie-dev", "genie-testing"]
        }
    },
    "status_code": 400
}
```

**Common Status Codes:**
- `200`: Success
- `400`: Bad Request (validation error)
- `401`: Unauthorized (missing/invalid API key in production)
- `404`: Not Found (agent/team/workflow doesn't exist)
- `422`: Unprocessable Entity (invalid request body)
- `500`: Internal Server Error

---

## Rate Limiting

Development mode has no rate limiting. Production mode defaults:
- **Requests per minute**: 100
- **Concurrent requests**: 10
- **Max request size**: 10MB

---

## WebSocket Support

For bidirectional real-time communication:

```javascript
const ws = new WebSocket('ws://localhost:8886/ws');

ws.onopen = () => {
    ws.send(JSON.stringify({
        type: 'agent_run',
        agent_id: 'master-genie',
        message: 'Help me code'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

---

## Quick Start Examples

### 1. Simple Agent Query
```bash
# Ask Master Genie for help
curl -X POST http://localhost:8886/playground/agents/master-genie/runs \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I implement authentication in FastAPI?"}'
```

### 2. Complex Team Task
```bash
# Use Genie team for multi-step development
curl -X POST http://localhost:8886/playground/teams/genie/runs \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Build a complete user management system with CRUD operations and tests",
    "context": {"framework": "fastapi", "database": "postgresql"}
  }'
```

### 3. Workflow Execution
```bash
# Run template workflow
curl -X POST http://localhost:8886/playground/workflows/template-workflow/runs \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "task": "Create API endpoints",
      "include_tests": true
    }
  }'
```

---


For more details, check the OpenAPI specification at: `http://localhost:8886/docs`
