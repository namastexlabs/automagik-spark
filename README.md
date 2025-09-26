<p align="center">
  <img src="assets/images/spark-logo.svg" alt="Automagik Spark Logo" width="400">
</p>
<h2 align="center">The Automation Engine That Never Sleeps</h2>

<p align="center">
  <strong>🎯 Turn Reactive AI into Proactive Intelligence</strong><br>
  Schedule workflows, orchestrate agents, automate everything—<br>
  so your AI works while you sleep
</p>

<p align="center">
  <a href="https://github.com/namastexlabs/automagik-spark/actions"><img alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/namastexlabs/automagik-spark/test.yml?branch=main&style=flat-square" /></a>
  <a href="https://github.com/namastexlabs/automagik-spark/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/namastexlabs/automagik-spark?style=flat-square&color=00D9FF" /></a>
  <a href="https://discord.gg/xcW8c7fF3R"><img alt="Discord" src="https://img.shields.io/discord/1234567890?style=flat-square&color=00D9FF&label=discord" /></a>
</p>

<p align="center">
  <a href="#-key-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-development">Development</a> •
  <a href="#-contributing">Contributing</a>
</p>

![Automagik Spark Dashboard](assets/images/screenshot.png)

---

## 🚀 What is Automagik Spark?

**Automagik Spark** is the automation engine that gives your AI agents a sense of time. While LangFlow and Hive create powerful workflows and agents, Spark makes them **proactive**—running tasks on schedules, triggering actions automatically, and working 24/7 without manual intervention.

Think of Spark as the alarm clock, calendar, and scheduler for your entire AI infrastructure.

### 💡 The Problem We Solve

**The Challenge**: Your AI workflows are brilliant but passive. They sit idle until you remember to trigger them:
- Daily reports that you forget to generate
- Monitoring tasks that need constant attention
- Routine automations that require manual kicks
- Agents that only respond when asked

**Our Solution**: Spark transforms passive workflows into active systems that work autonomously on your schedule.

### ✅ How Spark Changes the Game

**Before Spark**:
- ❌ Manually trigger workflows every time
- ❌ Set reminders to run routine tasks
- ❌ AI that only reacts when prompted
- ❌ Miss opportunities because agents weren't watching

**After Spark**:
- ✅ Workflows run automatically on schedule
- ✅ Set it once, runs forever
- ✅ AI that takes initiative proactively
- ✅ Never miss a beat with 24/7 automation

---

## 🌟 Key Features

- **⏰ Smart Scheduling**: Cron expressions, intervals, or one-time runs—schedule anything
- **🔄 Multi-Source Integration**: Connect unlimited LangFlow and Hive instances
- **🤖 Workflow Orchestration**: Sync and manage flows/agents from a unified control center
- **👷 Distributed Workers**: Scale task execution with Celery-powered workers
- **📊 Real-time Monitoring**: Track every task execution with detailed logs and status
- **🎯 MCP Native**: Control Spark programmatically via Model Context Protocol
- **🔒 Privacy-First Telemetry**: Anonymous usage analytics with full opt-out control
- **📡 REST API**: Full-featured API with interactive Swagger documentation
- **🛠️ Powerful CLI**: Manage everything from the command line
- **🐳 Flexible Deployment**: Docker, PM2, or bare metal—your choice

---

## 🎭 Real-World Use Cases

### For Solo Developers
```bash
# Morning briefing agent runs daily at 9 AM
automagik-spark schedule create my-briefing-agent "0 9 * * *"

# Database backup runs every Sunday at 2 AM
automagik-spark schedule create backup-flow "0 2 * * 0"

# Monitor API health every 5 minutes
automagik-spark schedule create health-check "*/5 * * * *"
```

### For Teams
- **Customer Support**: Auto-respond to tickets during off-hours
- **DevOps**: Automated health checks and incident response
- **Data Teams**: Scheduled ETL pipelines and report generation
- **Marketing**: Automated content generation and social posts

### For Enterprises
- **Compliance**: Scheduled audits and compliance checks
- **Operations**: Proactive monitoring and alerting systems
- **Analytics**: Automated data processing and insights
- **Finance**: Scheduled reconciliation and reporting

---

## 🏗️ How Spark Works

### Architecture Overview

```mermaid
graph TB
    subgraph "Your AI Infrastructure"
        LF[LangFlow Instances]
        HV[Automagik Hive]
        OM[Automagik Omni]
    end

    subgraph "Spark Engine"
        API[API Server<br/>FastAPI]
        WK[Workers<br/>Celery]
        DB[(PostgreSQL<br/>State & Tasks)]
        RD[(Redis<br/>Queue)]
    end

    subgraph "Interfaces"
        CLI[CLI Tool]
        MCP[MCP Server]
        REST[REST API]
    end

    LF <-->|Sync Flows| API
    HV <-->|Sync Agents| API
    API -->|Queue Tasks| RD
    RD -->|Execute| WK
    WK -->|Trigger| LF
    WK -->|Trigger| HV
    WK -->|Notify| OM
    API <-->|Store State| DB
    CLI -->|Commands| API
    MCP -->|Control| API
    REST -->|HTTP| API
```

### The Spark Lifecycle

1. **Connect**: Link your LangFlow/Hive instances
2. **Sync**: Discover all available workflows and agents
3. **Schedule**: Define when and how often tasks should run
4. **Execute**: Workers trigger workflows automatically
5. **Monitor**: Track execution history and results
6. **Scale**: Add more workers as your automation grows

### Example: Daily Report Automation

```bash
# 1. Add your LangFlow instance
automagik-spark source add http://langflow:7860 YOUR_API_KEY

# 2. Sync available flows
automagik-spark workflow sync "daily-sales-report"

# 3. Schedule it to run every weekday at 8 AM
automagik-spark schedule create WORKFLOW_ID "0 8 * * 1-5"

# That's it! Your report generates automatically every morning
```

---

## 📦 Quick Start

### Prerequisites

- **Python 3.12+** (we use the latest async features)
- **PostgreSQL 12+** (for persistent state)
- **Redis 6+** (for task queuing)
- **Optional**: Docker & Docker Compose (for containerized setup)

### One-Command Installation

#### For Production (Docker)
```bash
git clone https://github.com/namastexlabs/automagik-spark.git
cd automagik-spark
./scripts/setup_local.sh
```

#### For Development
```bash
git clone https://github.com/namastexlabs/automagik-spark.git
cd automagik-spark
./scripts/setup_dev.sh
```

### What Gets Installed

After setup completes, you'll have:

- **API Server**: `http://localhost:8883`
- **Interactive Docs**: `http://localhost:8883/api/v1/docs`
- **PostgreSQL**: `localhost:15432`
- **Redis**: `localhost:6379`
- **CLI Tool**: `automagik-spark` command
- **Workers**: Running and ready to execute tasks

### Verify Installation

```bash
# Check API health
curl http://localhost:8883/api/v1/health

# Try CLI commands
source .venv/bin/activate
automagik-spark --help

# View API documentation
open http://localhost:8883/api/v1/docs
```

---

## 🎮 Using Spark

### Via CLI (Recommended for Developers)

```bash
# Add a workflow source
automagik-spark source add https://my-langflow.com API_KEY_HERE

# List all available workflows
automagik-spark workflow list

# Sync a specific workflow
automagik-spark workflow sync "email-processor"

# Create a schedule (runs daily at midnight)
automagik-spark schedule create WORKFLOW_ID "0 0 * * *"

# List all schedules
automagik-spark schedule list

# View task execution history
automagik-spark task list
```

### Via REST API (For Integrations)

```bash
# Add a source
curl -X POST http://localhost:8883/api/v1/sources \
  -H "Content-Type: application/json" \
  -d '{"url": "https://langflow.example.com", "api_key": "..."}'

# Create a schedule
curl -X POST http://localhost:8883/api/v1/schedules \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "...", "cron": "0 0 * * *"}'
```

### Via MCP (From AI Coding Agents)

Spark is available as an MCP tool in [Automagik Tools](https://github.com/namastexlabs/automagik-tools):

```bash
# Install MCP server
uvx automagik-tools hub

# Now use natural language from Claude Code, Cursor, etc:
# "Schedule my daily-report workflow to run every morning at 9am"
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:15432/spark

# Redis
REDIS_URL=redis://localhost:6379

# API
API_HOST=0.0.0.0
API_PORT=8883

# Telemetry (optional)
AUTOMAGIK_SPARK_DISABLE_TELEMETRY=false
```

### Cron Expression Examples

```bash
"*/5 * * * *"      # Every 5 minutes
"0 * * * *"        # Every hour
"0 0 * * *"        # Daily at midnight
"0 9 * * 1-5"      # Weekdays at 9 AM
"0 0 * * 0"        # Every Sunday at midnight
"0 0 1 * *"        # First day of every month
```

---

## 📊 Monitoring & Telemetry

### Built-in Monitoring

```bash
# View recent task executions
automagik-spark task list --limit 20

# Check worker status
automagik-spark worker status

# View system health
curl http://localhost:8883/api/v1/health
```

### Privacy-Focused Telemetry

Spark collects anonymous usage metrics to improve the product:

**What we collect**:
- Command usage frequency
- API endpoint usage patterns
- Workflow execution statistics
- Error rates (no error details)

**What we DON'T collect**:
- Personal information
- Workflow content or data
- API keys or credentials
- File paths or environment variables

**Disable telemetry anytime**:
```bash
# Environment variable
export AUTOMAGIK_SPARK_DISABLE_TELEMETRY=true

# CLI command
automagik-spark telemetry disable

# Opt-out file
touch ~/.automagik-no-telemetry
```

---

## 🌐 Integration with Automagik Suite

Spark is the heartbeat of the Automagik ecosystem:

- **[Automagik Hive](https://github.com/namastexlabs/automagik-hive)**: Schedule multi-agent workflows
- **[Automagik Omni](https://github.com/namastexlabs/automagik-omni)**: Send notifications on schedule
- **[Automagik Forge](https://github.com/namastexlabs/automagik-forge)**: Trigger task execution
- **[Automagik Tools](https://github.com/namastexlabs/automagik-tools)**: Control Spark via MCP
- **[LangFlow](https://github.com/langflow-ai/langflow)**: Schedule visual AI workflows

---

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/namastexlabs/automagik-spark.git
cd automagik-spark
./scripts/setup_dev.sh

# Activate virtual environment
source .venv/bin/activate

# Run tests
pytest

# Check code quality
ruff format . && ruff check . && mypy .

# Run API server in dev mode
python -m automagik_spark.api
```

### Project Structure

```
automagik-spark/
├── automagik_spark/          # Main package
│   ├── api/                  # FastAPI application
│   ├── workers/              # Celery workers
│   ├── models/               # SQLAlchemy models
│   ├── services/             # Business logic
│   └── cli/                  # CLI commands
├── tests/                    # Test suite
├── scripts/                  # Setup and utility scripts
└── docs/                     # Documentation
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=automagik_spark --cov-report=html

# Run specific test file
pytest tests/test_scheduler.py

# Run with verbose output
pytest -v
```

---

## 🗺️ Roadmap

### Completed ✅
- [x] Multi-source workflow management (LangFlow + Hive)
- [x] Cron-based scheduling with interval support
- [x] Distributed worker architecture with Celery
- [x] REST API with Swagger documentation
- [x] Powerful CLI tool for workflow management
- [x] MCP server integration via Automagik Tools
- [x] Privacy-focused telemetry system

### Next Up 🚀
- [ ] **Step-by-step Workflows**: Break complex automations into discrete steps
- [ ] **Step Outputs**: Pass data between workflow steps seamlessly
- [ ] **Natural Language Scheduling**: "Run every morning" instead of cron syntax
- [ ] **/wish System**: AI assistant that helps build workflows
- [ ] **Improved DX**: Simpler setup and instance management
- [ ] **Workflow Dependencies**: Trigger workflows based on other completions
- [ ] **Omni Integration**: Deep integration with messaging platform
- [ ] **Forge Integration**: Trigger tasks from Kanban board
- [ ] **Conditional Execution**: Run workflows based on conditions
- [ ] **Retry Policies**: Auto-retry failed tasks with backoff
- [ ] **Workflow Marketplace**: Share and discover automation templates
- [ ] **Visual Workflow Builder**: Drag-and-drop scheduling interface

### Future Vision 🌟
- Advanced workflow orchestration with branching logic
- Multi-tenant support for enterprise deployments
- Real-time collaboration on workflow management
- AI-powered workflow optimization suggestions
- Integration with major observability platforms
- Cloud-hosted version for zero-setup deployments

---

## 🤝 Contributing

We love contributions! However, to maintain project coherence:

1. **Discuss First**: Open an issue before starting work
2. **Align with Roadmap**: Ensure changes fit our vision
3. **Follow Standards**: Match existing code patterns (async/await, type hints)
4. **Test Thoroughly**: Include tests for new features (>70% coverage)
5. **Document Well**: Update docstrings and documentation
6. **Quality Checks**: Run `ruff format . && ruff check . && mypy .`
7. **Conventional Commits**: Use proper commit messages with co-author:
   ```
   feat: add step-based workflow execution

   Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>
   ```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🙏 Acknowledgments

Special thanks to:
- The LangFlow team for building an amazing visual workflow platform
- The Celery project for robust distributed task execution
- All our early adopters and contributors who helped shape Spark
- The open-source community for inspiration and support

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **GitHub**: [github.com/namastexlabs/automagik-spark](https://github.com/namastexlabs/automagik-spark)
- **Discord**: [discord.gg/xcW8c7fF3R](https://discord.gg/xcW8c7fF3R)
- **Twitter**: [@automagikdev](https://twitter.com/automagikdev)
- **DeepWiki Docs**: [deepwiki.com/namastexlabs/automagik-spark](https://deepwiki.com/namastexlabs/automagik-spark)

---

<p align="center">
  <strong>🚀 Stop manually triggering workflows. Start automating everything.</strong><br>
  <strong>Spark - The Automation Engine That Never Sleeps ⚡</strong><br><br>
  <a href="https://github.com/namastexlabs/automagik-spark">Star us on GitHub</a> •
  <a href="https://discord.gg/xcW8c7fF3R">Join our Discord</a>
</p>

<p align="center">
  Made with ❤️ by <a href="https://namastex.ai">Namastex Labs</a><br>
  <em>AI that elevates human potential, not replaces it</em>
</p>
<a href="https://deepwiki.com/namastexlabs/automagik-spark"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>