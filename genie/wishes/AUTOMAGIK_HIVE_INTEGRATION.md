# AutoMagik Hive Integration Guide

## 🎯 Overview

AutoMagik Hive integration enables AutoMagik Spark to connect to and execute workflows from AutoMagik Hive instances. AutoMagik Hive provides three types of execution entities:

- **🤖 Agents**: Individual AI agents with specialized capabilities
- **👥 Teams**: Multi-agent coordinated teams for complex tasks
- **⚡ Workflows**: Structured multi-step processes with defined stages

## 🏗️ Architecture

### Source Type
- **Source Type**: `automagik-hive`
- **Manager Class**: `AutomagikHiveManager`
- **API Base URL**: `http://localhost:8886` (default)
- **Authentication**: API key via `x-api-key` header

### Integration Points
1. **SourceType Enum**: Added `AUTOMAGIK_HIVE = "automagik-hive"`
2. **WorkflowManager**: Integrated via `_get_source_manager()` method
3. **WorkflowSync**: Added synchronous execution support
4. **API Endpoints**: Full CRUD operations for sources

## 🚀 Getting Started

### 1. Create AutoMagik Hive Source

```bash
# Create a new AutoMagik Hive source
curl -X POST http://localhost:8883/api/v1/sources/ \
  -H "Content-Type: application/json" \
  -H "x-api-key: namastex888" \
  -d '{
    "name": "Local AutoMagik Hive",
    "source_type": "automagik-hive",
    "url": "http://localhost:8886",
    "api_key": "hive_namastex888"
  }'
```

### 2. Sync Available Flows

```bash
# List remote flows from AutoMagik Hive
curl "http://localhost:8883/api/v1/workflows/remote?source_id={source_id}" \
  -H "x-api-key: namastex888"
```

### 3. Sync Specific Flow

```bash
# Sync an agent/team/workflow
curl -X POST "http://localhost:8883/api/v1/workflows/sync/{flow_id}" \
  -H "Content-Type: application/json" \
  -H "x-api-key: namastex888" \
  -d '{
    "input_component": "input",
    "output_component": "output"
  }'
```

### 4. Execute Flow

```bash
# Run a synced flow
curl -X POST "http://localhost:8883/api/v1/workflows/{workflow_id}/run" \
  -H "Content-Type: application/json" \
  -H "x-api-key: namastex888" \
  -d '{
    "input_data": "Create a Python script to calculate fibonacci numbers"
  }'
```

### 5. Schedule Recurring Execution

```bash
# Create a schedule for recurring execution
curl -X POST "http://localhost:8883/api/v1/schedules" \
  -H "Content-Type: application/json" \
  -H "x-api-key: namastex888" \
  -d '{
    "workflow_id": "{workflow_id}",
    "schedule_type": "interval",
    "schedule_expr": "*/5 * * * *",
    "params": {
      "value": "Generate daily development report"
    },
    "status": "active"
  }'
```

## 📋 API Examples

### Example Hive Entities

Based on the AutoMagik Hive API documentation, here are the types of entities you can work with:

#### 🤖 Agents
```json
{
  "agent_id": "master-genie",
  "name": "🧞 Master Genie - Ultimate Development Companion",
  "description": "The ultimate development companion with dual identity",
  "model": {
    "name": "OpenAIChat",
    "model": "gpt-4o",
    "provider": "OpenAI gpt-4o"
  },
  "tools": [],
  "memory": {
    "name": "Memory",
    "db": {
      "name": "PostgresMemoryDb",
      "table_name": "agent_memories_master-genie"
    }
  }
}
```

#### 👥 Teams
```json
{
  "team_id": "genie",
  "name": "🧞 Genie",
  "description": "Clean, efficient coordination through 3 domain specialists",
  "mode": "coordinate",
  "members": [
    {
      "agent_id": "genie-dev",
      "name": "🧞 Genie Dev - Development Domain Coordinator"
    },
    {
      "agent_id": "genie-testing", 
      "name": "🧪 Genie Testing - Testing Domain Coordinator"
    }
  ]
}
```

#### ⚡ Workflows
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
    }
  ]
}
```

## 🔧 Advanced Configuration

### Custom API Integration

```python
from automagik_spark.core.workflows.automagik_hive import AutomagikHiveManager

# Create manager instance
manager = AutomagikHiveManager(
    api_url="http://localhost:8886",
    api_key="your_hive_api_key",
    source_id=your_source_id
)

# Async usage
async def run_hive_workflow():
    async with manager:
        # List available flows
        flows = await manager.list_flows()
        print(f"Available flows: {len(flows)}")
        
        # Run a specific agent
        result = await manager.run_flow(
            flow_id="master-genie",
            input_data="Help me build a REST API",
            session_id="my-session"
        )
        print(f"Result: {result['result']}")

# Sync usage
def run_hive_workflow_sync():
    with manager:
        # List flows synchronously
        flows = manager.list_flows_sync()
        
        # Run flow synchronously  
        result = manager.run_flow_sync(
            flow_id="genie-team",
            input_data="Create a complete authentication system"
        )
        return result
```

### Flow Type Detection

AutoMagik Hive flows are automatically categorized by type:

```python
def get_flow_info(flow_data):
    flow_type = flow_data['data']['type']
    
    if flow_type == 'hive_agent':
        print(f"🤖 Agent: {flow_data['name']}")
        print(f"   Model: {flow_data['data']['model']}")
        print(f"   Tools: {len(flow_data['data']['tools'])}")
        
    elif flow_type == 'hive_team':
        print(f"👥 Team: {flow_data['name']}")
        print(f"   Mode: {flow_data['data']['mode']}")
        print(f"   Members: {flow_data['data']['members_count']}")
        
    elif flow_type == 'hive_workflow':
        print(f"⚡ Workflow: {flow_data['name']}")
        print(f"   Steps: {len(flow_data['data']['steps'])}")
```

## 🎯 Execution Patterns

### Agent Execution
- **Endpoint**: `POST /playground/agents/{agent_id}/runs`
- **Use Case**: Single AI agent tasks
- **Input**: Simple message string
- **Output**: Agent response with metadata

### Team Execution  
- **Endpoint**: `POST /playground/teams/{team_id}/runs`
- **Use Case**: Multi-agent coordination
- **Input**: Complex task description
- **Output**: Coordinator + member responses

### Workflow Execution
- **Endpoint**: `POST /playground/workflows/{workflow_id}/runs`
- **Use Case**: Structured multi-step processes
- **Input**: Structured input data
- **Output**: Step-by-step execution results

## 🛠️ Troubleshooting

### Common Issues

#### 1. Connection Failed
```
Failed to validate AutoMagik Hive source: Connection failed
```
**Solution**: Verify AutoMagik Hive is running on the specified port and URL is accessible.

#### 2. Authentication Error
```
HTTP Status: 401, Invalid API key
```
**Solution**: Check that the API key is correct and has proper permissions.

#### 3. Flow Not Found
```
Flow {flow_id} not found in AutoMagik Hive
```
**Solution**: Verify the flow exists and is accessible. List flows first to confirm availability.

#### 4. Execution Timeout
```
Request timed out
```
**Solution**: Increase timeout settings or check if the Hive instance is overloaded.

### Debug Logging

Enable detailed logging to troubleshoot issues:

```python
import logging
logging.getLogger('automagik_spark.core.workflows.automagik_hive').setLevel(logging.DEBUG)
```

## 📊 Monitoring

### Task Status

Monitor AutoMagik Hive task execution:

```bash
# List recent tasks
curl "http://localhost:8883/api/v1/tasks?limit=10" \
  -H "x-api-key: namastex888"

# Get specific task details
curl "http://localhost:8883/api/v1/tasks/{task_id}" \
  -H "x-api-key: namastex888"
```

### Schedule Management

```bash
# List active schedules
curl "http://localhost:8883/api/v1/schedules?status=active" \
  -H "x-api-key: namastex888"

# Update schedule status
curl -X PUT "http://localhost:8883/api/v1/schedules/{schedule_id}" \
  -H "Content-Type: application/json" \
  -H "x-api-key: namastex888" \
  -d '{"status": "paused"}'
```

## 🚀 Best Practices

### 1. Session Management
- Use consistent session IDs for conversation continuity
- Session format: `{source_id}_{flow_id}` (auto-generated)
- Sessions enable context preservation across multiple executions

### 2. Input Data Handling
- **Agents**: Simple string messages work best
- **Teams**: Provide detailed task descriptions
- **Workflows**: Use structured input with clear requirements

### 3. Error Handling
- Always check execution status before processing results
- Implement retry logic for transient failures
- Log detailed error information for debugging

### 4. Performance Optimization
- Use async methods for high-throughput scenarios
- Implement connection pooling for frequent API calls
- Cache flow metadata to reduce API calls

### 5. Security
- Store API keys securely using encryption
- Use HTTPS endpoints in production
- Implement proper access controls

## 🔄 Migration Guide

### From AutoMagik Agents to AutoMagik Hive

If migrating from the existing `automagik-agents` source type:

1. **Create new Hive source** with `automagik-hive` type
2. **Re-sync flows** - Hive provides richer metadata  
3. **Update schedules** to use new workflow IDs
4. **Test execution** - API responses may differ slightly
5. **Monitor performance** - Hive may have different response times

### Coexistence

AutoMagik Spark supports multiple source types simultaneously:
- Keep existing `automagik-agents` sources running
- Add new `automagik-hive` sources for enhanced features
- Gradually migrate workflows as needed

## 📈 Future Enhancements

Planned improvements for AutoMagik Hive integration:

1. **Streaming Support**: Real-time execution monitoring
2. **Workflow Composition**: Chain multiple Hive workflows
3. **Resource Management**: CPU/memory usage tracking  
4. **Advanced Scheduling**: Conditional and dependency-based scheduling
5. **Multi-Hive Support**: Connect to multiple Hive instances

---

## 🎉 Conclusion

AutoMagik Hive integration extends AutoMagik Spark's capabilities with:
- **Enhanced AI Agents**: More sophisticated individual agents
- **Team Coordination**: Multi-agent collaborative execution  
- **Structured Workflows**: Predefined multi-step processes
- **Rich Metadata**: Better monitoring and management
- **Session Continuity**: Conversation context preservation

The integration maintains full backward compatibility while providing powerful new execution patterns for complex AI-powered workflows.

For questions or support, refer to the AutoMagik Hive API documentation at `http://localhost:8886/docs` when your Hive instance is running.