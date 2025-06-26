# AutoMagik Spark API - UX Developer Guide

## Overview
AutoMagik Spark provides a comprehensive REST API for managing workflow sources, syncing workflows, and executing automation tasks. This guide documents all endpoints with practical examples for building a user interface.

## Authentication
All API endpoints (except health check) require authentication via API key:
```
X-API-Key: dev-key-12345
```

## Base URL
- Development: `http://localhost:8883`
- API Prefix: `/api/v1`

---

## 🏥 System Endpoints

### Health Check
**GET** `/health`
- **Purpose**: System health monitoring
- **Auth**: Not required
- **Response**: Simple health status

```bash
curl http://localhost:8883/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-25 19:27:08"
}
```

### System Information
**GET** `/`
- **Purpose**: API status and version information
- **Auth**: Required
- **Use Case**: Dashboard overview, version display

```bash
curl -H "X-API-Key: dev-key-12345" http://localhost:8883/
```

**Response:**
```json
{
  "status": "online",
  "service": "AutoMagik API",
  "message": "Welcome to AutoMagik API, it's up and running!",
  "version": "0.2.2",
  "server_time": "2025-06-25 19:27:16",
  "docs_url": "http://localhost:8883/api/v1/docs"
}
```

---

## 🔗 Workflow Sources Management

### List All Sources
**GET** `/api/v1/sources/`
- **Purpose**: Display all configured workflow sources (LangFlow, AutoMagik Agents)
- **Use Case**: Sources overview page, source selection dropdowns

```bash
curl -H "X-API-Key: dev-key-12345" http://localhost:8883/api/v1/sources/
```

**Response:**
```json
[
  {
    "id": "c662db6e-6b77-4e4a-80af-dcb724712c60",
    "source_type": "langflow",
    "url": "http://localhost:17860/",
    "status": "active",
    "version_info": {
      "version": "1.4.3",
      "package": "Langflow"
    },
    "created_at": "2025-06-25T16:20:32.296887Z"
  },
  {
    "id": "77be32f3-1a3a-4c21-8831-f0f49184c378",
    "source_type": "automagik-agents",
    "url": "http://localhost:18881/",
    "status": "active",
    "version_info": {
      "version": "0.1.4"
    }
  }
]
```

**UI Components Needed:**
- Source cards with type badges (LangFlow/AutoMagik Agents)
- Status indicators (active/inactive)
- Version display
- Add/Edit/Delete actions

### Get Specific Source
**GET** `/api/v1/sources/{source_id}`
- **Purpose**: View detailed source information
- **Use Case**: Source detail modal, edit forms

### Create New Source
**POST** `/api/v1/sources/`
- **Purpose**: Add new workflow source
- **Body**: `{"source_type": "langflow", "url": "http://example.com", "api_key": "key"}`
- **Use Case**: Add source wizard/form

### Update Source
**PATCH** `/api/v1/sources/{source_id}`
- **Purpose**: Update source configuration
- **Use Case**: Edit source settings

### Delete Source
**DELETE** `/api/v1/sources/{source_id}`
- **Purpose**: Remove workflow source
- **Use Case**: Source management with confirmation dialogs

---

## 🔄 Workflows Management

### List Local Workflows
**GET** `/api/v1/workflows`
- **Purpose**: Show all synced workflows in local database
- **Use Case**: Main workflows dashboard

```bash
curl -H "X-API-Key: dev-key-12345" http://localhost:8883/api/v1/workflows
```

**Response:**
```json
[
  {
    "id": "1b0d2d07-25e7-4249-aaad-6f6cf6e9ae5a",
    "name": "Simple Test",
    "description": "A simple but powerful starter agent.",
    "source": "http://localhost:17860",
    "remote_flow_id": "0cd5870f-0c23-4a0b-91d4-927fee405394",
    "input_component": "ChatInput-1C1Z5",
    "output_component": "ChatOutput-WMb72",
    "latest_run": "COMPLETED",
    "task_count": 1,
    "failed_task_count": 0,
    "tags": ["assistants", "agents"]
  }
]
```

**UI Components Needed:**
- Workflow cards with status badges
- Source type indicators
- Latest run status
- Task count statistics
- Quick action buttons (Run, Schedule, View)

### List Remote Workflows
**GET** `/api/v1/workflows/remote?source_url={source_url}`
- **Purpose**: Browse available workflows from external sources
- **Use Case**: Workflow discovery and sync interface

```bash
# LangFlow workflows
curl -H "X-API-Key: dev-key-12345" "http://localhost:8883/api/v1/workflows/remote?source_url=http://localhost:17860"

# AutoMagik Agents
curl -H "X-API-Key: dev-key-12345" "http://localhost:8883/api/v1/workflows/remote?source_url=http://localhost:18881"
```

**AutoMagik Agents Response:**
```json
[
  {
    "id": "simple",
    "name": "simple",
    "description": "Enhanced Simple Agent with multimodal capabilities...",
    "origin": {"instance": "localhost:18881", "source_url": "http://localhost:18881"},
    "components": []
  },
  {
    "id": "flashinho",
    "name": "flashinho", 
    "description": "Enhanced Flashinho Agent with specialized Flashed API integration..."
  }
]
```

**UI Components Needed:**
- Source-specific workflow browsers
- Filter/search capabilities
- Sync buttons for each workflow
- Preview descriptions
- Bulk sync functionality

### Get Specific Workflow
**GET** `/api/v1/workflows/{workflow_id}`
- **Purpose**: View detailed workflow information
- **Use Case**: Workflow detail page, configuration view

### Sync Workflow from Remote Source
**POST** `/api/v1/workflows/sync/{flow_id}?input_component={input}&output_component={output}&source_url={url}`
- **Purpose**: Import workflow from external source to local database
- **Use Case**: Workflow sync wizard

```bash
# LangFlow workflow sync (requires components)
curl -X POST -H "X-API-Key: dev-key-12345" \
  "http://localhost:8883/api/v1/workflows/sync/0cd5870f-0c23-4a0b-91d4-927fee405394?input_component=ChatInput-1C1Z5&output_component=ChatOutput-WMb72&source_url=http://localhost:17860"

# AutoMagik Agents sync (empty components)
curl -X POST -H "X-API-Key: dev-key-12345" \
  "http://localhost:8883/api/v1/workflows/sync/flashinho?input_component=&output_component=&source_url=http://localhost:18881"
```

**UI Components Needed:**
- Component selection for LangFlow workflows
- Auto-detection of workflow type
- Progress indicators for sync process
- Success/error notifications

### Execute Workflow
**POST** `/api/v1/workflows/{workflow_id}/run`
- **Purpose**: Run workflow with input data
- **Body**: Plain text input data
- **Use Case**: Workflow execution interface

```bash
curl -X POST -H "Content-Type: text/plain" -H "X-API-Key: dev-key-12345" \
  -d "Hello, test message!" \
  http://localhost:8883/api/v1/workflows/1b0d2d07-25e7-4249-aaad-6f6cf6e9ae5a/run
```

**Response:**
```json
{
  "id": "f27e4074-f1c0-40db-b31a-19b14b401c0c",
  "workflow_id": "1b0d2d07-25e7-4249-aaad-6f6cf6e9ae5a",
  "status": "completed",
  "input_data": {"value": "Hello, test message!"},
  "output_data": {/* execution results */},
  "started_at": "2025-06-25T19:28:24.413980Z",
  "finished_at": "2025-06-25T19:28:24.660492Z"
}
```

**UI Components Needed:**
- Input form/text area
- Run button with loading states
- Real-time execution status
- Output display area
- Execution history

---

## 📋 Tasks Management

### List Tasks
**GET** `/api/v1/tasks?workflow_id={id}&status={status}&limit={n}`
- **Purpose**: View execution history and monitor running tasks
- **Use Case**: Task dashboard, workflow execution history

```bash
curl -H "X-API-Key: dev-key-12345" http://localhost:8883/api/v1/tasks
```

**Response:**
```json
[
  {
    "id": "f27e4074-f1c0-40db-b31a-19b14b401c0c",
    "workflow_id": "1b0d2d07-25e7-4249-aaad-6f6cf6e9ae5a",
    "status": "completed",
    "input_data": {"value": "Test execution"},
    "output_data": "/* results */",
    "error": null,
    "started_at": "2025-06-25T19:28:24.413980Z",
    "finished_at": "2025-06-25T19:28:24.660492Z",
    "tries": 1,
    "max_retries": 3
  }
]
```

**UI Components Needed:**
- Task list with filtering (by workflow, status)
- Status badges (pending, running, completed, failed)
- Execution time indicators
- Retry buttons for failed tasks
- Input/output viewers

### Get Specific Task
**GET** `/api/v1/tasks/{task_id}`
- **Purpose**: View detailed task execution information
- **Use Case**: Task detail modal, debugging view

---

## ⏰ Schedules Management

### List Schedules
**GET** `/api/v1/schedules`
- **Purpose**: View all scheduled workflow executions
- **Use Case**: Schedule management dashboard

### Create Schedule
**POST** `/api/v1/schedules`
- **Purpose**: Schedule automatic workflow execution
- **Body**: `{"workflow_id": "...", "schedule_type": "interval", "schedule_expr": "300", "input_value": "data"}`
- **Use Case**: Schedule creation wizard

### Enable/Disable Schedule
**POST** `/api/v1/schedules/{schedule_id}/enable`
**POST** `/api/v1/schedules/{schedule_id}/disable`
- **Purpose**: Control schedule activation
- **Use Case**: Schedule management toggles

---

## 🎨 UX Design Recommendations

### 1. Dashboard Layout
```
┌─────────────────────────────────────────┐
│ AutoMagik Spark Dashboard               │
├─────────────────────────────────────────┤
│ [Sources: 2] [Workflows: 3] [Tasks: 45] │
├─────────────────────────────────────────┤
│ Quick Actions: [Add Source] [Sync All]  │
├─────────────────────────────────────────┤
│ Recent Tasks                            │
│ ┌─────────────────────────────────────┐ │
│ │ ✅ Simple Test (2min ago)          │ │
│ │ ❌ AutoAgent Failed (5min ago)     │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 2. Source Management Interface
- **Source Cards**: Display type, URL, status, version
- **Add Source Wizard**: Step-by-step configuration
- **Auto-Discovery**: Show detected sources with one-click add
- **Health Monitoring**: Real-time status indicators

### 3. Workflow Discovery & Sync
- **Two-Panel Layout**: Remote workflows | Local workflows
- **Filter by Source**: Tabs for LangFlow vs AutoMagik Agents
- **Sync Progress**: Real-time sync status with progress bars
- **Component Selection**: Smart UI for LangFlow component mapping

### 4. Execution Interface
- **Input Editor**: Syntax highlighting for different data types
- **Run Button**: With loading states and ETA estimates
- **Output Viewer**: Collapsible sections for large outputs
- **Execution History**: Timeline view with quick re-run options

### 5. Responsive Design Priorities
1. **Mobile**: Focus on monitoring and quick actions
2. **Tablet**: Workflow execution and task management
3. **Desktop**: Full featured administration interface

### 6. Real-time Features
- **WebSocket Integration**: For live task status updates
- **Auto-refresh**: Configurable intervals for task lists
- **Notifications**: Browser notifications for completed tasks

### 7. Error Handling & User Feedback
- **Validation**: Client-side validation for all forms
- **Error Messages**: Clear, actionable error descriptions
- **Loading States**: Skeleton screens and progress indicators
- **Success Feedback**: Toast notifications and visual confirmations

## 🔧 Development Notes

### API Behavior Patterns
1. **LangFlow Workflows**: Require input/output component specification
2. **AutoMagik Agents**: Use empty strings for component fields
3. **Error Responses**: Include detailed validation messages
4. **Pagination**: Some endpoints support limit/offset parameters
5. **Filtering**: Many list endpoints support query parameters

### State Management Recommendations
1. **Sources**: Cache source list with periodic refresh
2. **Workflows**: Separate remote and local workflow stores
3. **Tasks**: Real-time updates for running tasks
4. **Schedules**: Track next execution times

### Performance Considerations
1. **Lazy Loading**: Load workflow details on demand
2. **Caching**: Cache remote workflow lists for better UX
3. **Debouncing**: For search and filter operations
4. **Batch Operations**: Group multiple sync operations

This comprehensive guide provides all necessary information for building a complete AutoMagik Spark UI that leverages the full potential of the API while providing an excellent user experience.