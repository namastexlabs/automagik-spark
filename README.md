<p align="center">
  <img src=".github/images/automagik_logo.png" alt="AutoMagik Logo" width="600"/>
</p>

# AutoMagik Agents

A powerful toolkit for quickly building and deploying AI agents using the Pydantic AI framework. Create custom agents from templates, expose them through a RESTful API, and manage conversations with built-in memory and tool support. Perfect for teams looking to rapidly prototype and deploy AI agents with standardized patterns and best practices.

## 🌟 Features

### Extensible Agent System
- **Template-Based Development**: Create new agents from pre-built templates
- **Ready-to-Use Templates**: Start with Simple Agent or Notion Agent
- **Intuitive CLI**: Generate agents with simple commands
- **Automatic Tool Registration**: Register and manage tools effortlessly

### Powerful API Integration
- **FastAPI Backend**: High-performance RESTful endpoints
- **Sophisticated Session Management**: Track conversation history
- **Structured Data Models**: Clear request/response patterns
- **Security**: Built-in authentication and CORS support
- **Monitoring**: Health checks and version tracking

### Advanced Memory System
- **Persistent Conversation History**: Maintain context across sessions
- **Session-Based Organization**: Efficient memory management
- **Tool Interaction Tracking**: Record tool calls and outputs
- **Structured Storage**: Organized message repository

### Built-in Templates
- **Simple Agent**: Basic chat functionality with datetime tools
- **Notion Agent**: Full Notion integration with database management

## 🚀 Quick Start

### Installation

```bash
pip install automagik-agents
```

### Environment Setup

```bash
# Copy example environment file
cp .env-example .env

# Configure required variables
AM_API_KEY=your_api_key_here
AM_HOST=0.0.0.0
AM_PORT=8000
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=openai:gpt-4o-mini  # or your preferred model

# For Notion agent (optional)
NOTION_TOKEN=your_notion_token
```

### Creating Your First Agent

```bash
# Create from simple template
automagik-agents create-agent -n my_agent -t simple_agent

# Create from Notion template
automagik-agents create-agent -n my_notion_agent -t notion_agent
```

### Starting the API Server

```bash
automagik-agents api start --reload
```

## 💡 Usage Examples

### API Endpoints

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Running Agents

**Simple Agent**
```bash
curl -X POST http://localhost:8000/agent/simple_agent/run \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "message_input": "What time is it?",
    "session_id": "optional_session_id"
  }'
```

**Notion Agent**
```bash
curl -X POST http://localhost:8000/agent/notion_agent/run \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "message_input": "List my databases",
    "session_id": "optional_session_id"
  }'
```

#### Session Management

**Retrieve Session History**
```bash
curl http://localhost:8000/session/your_session_id \
  -H "X-API-Key: your_api_key"
```

**Clear Session Data**
```bash
curl -X DELETE http://localhost:8000/session/your_session_id \
  -H "X-API-Key: your_api_key"
```

### Creating Custom Agents

#### 1. Create Agent Template

```bash
automagik-agents create-agent -n custom -t simple_agent
```

#### 2. Customize Agent Files

- Edit `src/agents/custom_agent/prompts.py` for system prompts
- Modify `src/agents/custom_agent/agent.py` for agent behavior
- Update `src/agents/custom_agent/__init__.py` for configuration

#### 3. Register Custom Tools

```python
def register_tools(self):
    """Register custom tools with the agent."""
    # Register built-in tools
    self.agent.tool(self.get_current_time)
    
    # Register custom tools
    self.agent.tool(your_custom_tool)
    
def your_custom_tool(self, param1: str) -> str:
    """Custom tool description.
    
    Args:
        param1: Description of parameter
        
    Returns:
        Description of return value
    """
    # Tool implementation
    return f"Processed: {param1}"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>Part of the AutoMagik Ecosystem</b><br>
  <a href="https://github.com/namastexlabs/automagik">AutoMagik</a> |
  <a href="https://github.com/namastexlabs/automagik-agents">AutoMagik Agents</a> |
  <a href="https://github.com/namastexlabs/automagik-ui">AutoMagik UI</a>
</p>
