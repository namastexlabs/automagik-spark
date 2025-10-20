# Release Notes Template

This template is used by `.github/workflows/publish-pypi.yml` to generate release notes automatically.

## How to Customize

Edit this file to change the default release notes structure. The workflow will:
1. Use `generate_release_notes: true` to create automatic changelog from commits
2. Append this template content below the auto-generated changelog

## Template Variables

The following variables are available and will be replaced by the workflow:
- `{{VERSION}}` - The release version (e.g., 0.3.7, 0.3.8rc1)
- `{{REPOSITORY}}` - The GitHub repository (e.g., namastexlabs/automagik-spark)

---

## Default Template

```markdown
## 📦 PyPI Release {{VERSION}}

This release has been published to PyPI and is ready for installation and testing.

### 🚀 Installation

\```bash
# Install from PyPI
pip install automagik-spark=={{VERSION}}

# Or upgrade existing installation
pip install --upgrade automagik-spark=={{VERSION}}

# Install with Docker
docker pull namastexlabs/automagik-spark-api:v{{VERSION}}
docker pull namastexlabs/automagik-spark-worker:v{{VERSION}}
\```

### 🐳 Docker Compose Quick Start

\```bash
# Download and run with Docker Compose
curl -O https://raw.githubusercontent.com/{{REPOSITORY}}/v{{VERSION}}/docker/docker-compose.yml
docker compose up -d

# Access the API
curl http://localhost:8888/api/v1/health
\```

---

## 📋 Release Assets

- Python wheel (`.whl`) for fast installation
- Source distribution (`.tar.gz`) for building from source
- Docker images for API and Worker services
- Digital attestations for supply chain security

---

## 🔗 Links

- 📦 [PyPI Package](https://pypi.org/project/automagik-spark/{{VERSION}}/)
- 🐳 [Docker Hub - API](https://hub.docker.com/r/namastexlabs/automagik-spark-api)
- 🐳 [Docker Hub - Worker](https://hub.docker.com/r/namastexlabs/automagik-spark-worker)
- 📚 [Documentation](https://github.com/{{REPOSITORY}}/blob/main/README.md)
- 📝 [Full Changelog](https://github.com/{{REPOSITORY}}/compare/v0.3.6...v{{VERSION}})

---

## 🛠️ Key Features

**AutoMagik Spark** is an automagion engine that integrates with LangFlow instances to:
- 🔄 Deploy and execute AI-powered workflows without coding
- ⏰ Schedule workflows with cron or interval-based triggers
- 📊 Monitor task execution and workflow performance
- 🔌 Connect to LangFlow's visual flow editor
- 🐳 Run with Docker or standalone Python

---

🤖 **Automated Release**: Published via GitHub Actions using [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)

**Co-Authored-By**: Automagik Genie 🧞 <genie@namastex.ai>
```
