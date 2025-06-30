# ===========================================
# 🪄 AutoMagik Spark - Streamlined Makefile
# ===========================================

.DEFAULT_GOAL := help
MAKEFLAGS += --no-print-directory
SHELL := /bin/bash

# ===========================================
# 🎨 Colors & Symbols
# ===========================================
FONT_RED := $(shell tput setaf 1)
FONT_GREEN := $(shell tput setaf 2)
FONT_YELLOW := $(shell tput setaf 3)
FONT_BLUE := $(shell tput setaf 4)
FONT_PURPLE := $(shell tput setaf 5)
FONT_CYAN := $(shell tput setaf 6)
FONT_GRAY := $(shell tput setaf 7)
FONT_BLACK := $(shell tput setaf 8)
FONT_BOLD := $(shell tput bold)
FONT_RESET := $(shell tput sgr0)
CHECKMARK := ✅
WARNING := ⚠️
ERROR := ❌
ROCKET := 🚀
MAGIC := 🪄
AUTOMAGIK := 🔮
INFO := ℹ️
SPARKLES := ✨

# ===========================================
# 📁 Paths & Configuration
# ===========================================
PROJECT_ROOT := $(shell pwd)
VENV_PATH := $(PROJECT_ROOT)/.venv
PYTHON := python3
UV := uv
SERVICE_NAME := automagik-spark
DOCKER_COMPOSE_DEV := docker/docker-compose.dev.yml
DOCKER_COMPOSE_PROD := docker/docker-compose.prod.yml

# Docker Compose command detection
DOCKER_COMPOSE := $(shell if command -v docker-compose >/dev/null 2>&1; then echo "docker-compose"; else echo "docker compose"; fi)

# Load environment variables from .env file if it exists
-include .env
export

# Default values (will be overridden by .env if present)
HOST ?= 127.0.0.1
PORT ?= 8883
LOG_LEVEL ?= info

# ===========================================
# 🛠️ Utility Functions
# ===========================================
define print_status
	@echo -e "$(FONT_PURPLE)$(AUTOMAGIK) $(1)$(FONT_RESET)"
endef

define print_success
	@echo -e "$(FONT_GREEN)$(CHECKMARK) $(1)$(FONT_RESET)"
endef

define print_warning
	@echo -e "$(FONT_YELLOW)$(WARNING) $(1)$(FONT_RESET)"
endef

define print_error
	@echo -e "$(FONT_RED)$(ERROR) $(1)$(FONT_RESET)"
endef

define print_info
	@echo -e "$(FONT_CYAN)$(INFO) $(1)$(FONT_RESET)"
endef

define print_success_with_logo
	@echo -e "$(FONT_GREEN)$(CHECKMARK) $(1)$(FONT_RESET)"
	$(call show_automagik_logo)
endef

define show_automagik_logo
	@[ -z "$$AUTOMAGIK_QUIET_LOGO" ] && { \
		echo ""; \
		echo -e "$(FONT_PURPLE)                                                                                            $(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE)                                                                                            $(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE)     -+*         -=@%*@@@@@@*  -#@@@%*  =@@*      -%@#+   -*       +%@@@@*-%@*-@@*  -+@@*   $(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE)     =@#*  -@@*  -=@%+@@@@@@*-%@@#%*%@@+=@@@*    -+@@#+  -@@*   -#@@%%@@@*-%@+-@@* -@@#*    $(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE)    -%@@#* -@@*  -=@@* -@%* -@@**   --@@=@@@@*  -+@@@#+ -#@@%* -*@%*-@@@@*-%@+:@@+#@@*      $(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE)   -#@+%@* -@@*  -=@@* -@%* -@@*-+@#*-%@+@@=@@* +@%#@#+ =@##@* -%@#*-@@@@*-%@+-@@@@@*       $(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE)  -*@#==@@*-@@*  -+@%* -@%* -%@#*   -+@@=@@++@%-@@=*@#=-@@*-@@*:+@@*  -%@*-%@+-@@#*@@**     $(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE)  -@@* -+@%-+@@@@@@@*  -@%*  -#@@@@%@@%+=@@+-=@@@*    -%@*  -@@*-*@@@@%@@*#@@#=%*  -%@@*    $(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE) -@@*+  -%@*  -#@%+    -@%+     =#@@*   =@@+          +@%+  -#@#   -*%@@@*@@@@%+     =@@+   $(FONT_RESET)"; \
		echo ""; \
		echo -e "$(FONT_CYAN)🏢 Built by$(FONT_RESET) $(FONT_BOLD)Namastex Labs$(FONT_RESET) | $(FONT_YELLOW)📄 MIT Licensed$(FONT_RESET) | $(FONT_YELLOW)🌟 Open Source Forever$(FONT_RESET)"; \
		echo -e "$(FONT_PURPLE)✨ \"Because magic shouldn't be complicated\"$(FONT_RESET)"; \
		echo ""; \
	} || true
endef

define check_pm2
	@if ! command -v pm2 >/dev/null 2>&1; then \
		$(call print_error,PM2 not found. Install with: npm install -g pm2); \
		exit 1; \
	fi
endef

define check_docker
	@if ! command -v docker >/dev/null 2>&1; then \
		$(call print_error,Docker not found); \
		echo -e "$(FONT_YELLOW)💡 Install Docker: https://docs.docker.com/get-docker/$(FONT_RESET)"; \
		exit 1; \
	fi
	@if ! docker info >/dev/null 2>&1; then \
		$(call print_error,Docker daemon not running); \
		echo -e "$(FONT_YELLOW)💡 Start Docker service$(FONT_RESET)"; \
		exit 1; \
	fi
endef

define ensure_env_file
	@if [ ! -f ".env" ]; then \
		if [ -f ".env.example" ]; then \
			cp .env.example .env; \
			$(call print_info,.env created from .env.example); \
		else \
			touch .env; \
			$(call print_info,.env file created); \
		fi; \
		echo -e "$(FONT_YELLOW)💡 Edit .env and configure your settings$(FONT_RESET)"; \
	fi
endef

define check_prerequisites
	@if ! command -v python3 >/dev/null 2>&1; then \
		echo -e "$(FONT_RED)$(ERROR) Python 3 not found$(FONT_RESET)"; \
		exit 1; \
	fi
	@if ! command -v uv >/dev/null 2>&1; then \
		if [ -f "$$HOME/.local/bin/uv" ]; then \
			export PATH="$$HOME/.local/bin:$$PATH"; \
			echo -e "$(FONT_PURPLE)$(AUTOMAGIK) Found uv in $$HOME/.local/bin$(FONT_RESET)"; \
		else \
			echo -e "$(FONT_PURPLE)$(AUTOMAGIK) Installing uv...$(FONT_RESET)"; \
			curl -LsSf https://astral.sh/uv/install.sh | sh; \
			export PATH="$$HOME/.local/bin:$$PATH"; \
			echo -e "$(FONT_GREEN)$(CHECKMARK) uv installed successfully$(FONT_RESET)"; \
		fi; \
	fi
endef

define setup_python_env
	@echo -e "$(FONT_PURPLE)$(AUTOMAGIK) Installing dependencies with uv...$(FONT_RESET)"
	@if command -v uv >/dev/null 2>&1; then \
		if ! uv sync 2>/dev/null; then \
			echo -e "$(FONT_YELLOW)$(WARNING) Installation failed - clearing UV cache and retrying...$(FONT_RESET)"; \
			uv cache clean; \
			uv sync; \
		fi; \
	elif [ -f "$$HOME/.local/bin/uv" ]; then \
		if ! $$HOME/.local/bin/uv sync 2>/dev/null; then \
			echo -e "$(FONT_YELLOW)$(WARNING) Installation failed - clearing UV cache and retrying...$(FONT_RESET)"; \
			$$HOME/.local/bin/uv cache clean; \
			$$HOME/.local/bin/uv sync; \
		fi; \
	else \
		echo -e "$(FONT_RED)$(ERROR) uv not found - please install uv first$(FONT_RESET)"; \
		exit 1; \
	fi
endef

define install_docker_if_needed
	@if ! command -v docker >/dev/null 2>&1; then \
		if command -v apt-get >/dev/null 2>&1; then \
			$(call print_status,Installing Docker on Ubuntu/Debian...); \
			sudo apt-get update; \
			sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release; \
			curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg; \
			echo "deb [arch=$$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null; \
			sudo apt-get update; \
			sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin; \
			sudo usermod -aG docker $$USER; \
			$(call print_success,Docker installed! Please log out and back in to use Docker); \
		else \
			$(call print_error,Please install Docker manually: https://docs.docker.com/get-docker/); \
			exit 1; \
		fi; \
	fi
endef


# Function removed - now using PM2 for service management

# ===========================================
# 📋 Help System
# ===========================================
.PHONY: help
help: ## Show this help message
	@$(call show_automagik_logo)
	@echo -e "$(FONT_BOLD)$(FONT_CYAN)Welcome to AutoMagik Spark$(FONT_RESET) - $(FONT_GRAY)Automagion Engine$(FONT_RESET)"
	@echo ""
	@echo -e "$(FONT_PURPLE)$(AUTOMAGIK) AutoMagik Spark Development & Deployment Commands$(FONT_RESET)"
	@echo ""
	@echo -e "$(FONT_CYAN)🚀 Installation & Setup:$(FONT_RESET)"
	@echo -e "  $(FONT_PURPLE)install        $(FONT_RESET) Install AutoMagik Spark environment (uv sync + setup)"
	@echo -e "  $(FONT_PURPLE)install-deps   $(FONT_RESET) Install optional dependencies (PostgreSQL, Redis)"
	@echo -e "  $(FONT_PURPLE)install-docker $(FONT_RESET) Install with Docker for development"
	@echo -e "  $(FONT_PURPLE)install-prod   $(FONT_RESET) Install production Docker environment"
	@echo -e "  $(FONT_PURPLE)setup-local    $(FONT_RESET) Run local production setup script"
	@echo -e "  $(FONT_PURPLE)setup-dev      $(FONT_RESET) Run development setup script"
	@echo ""
	@echo -e "$(FONT_CYAN)🎛️ Service Management:$(FONT_RESET)"
	@echo -e "  $(FONT_PURPLE)dev            $(FONT_RESET) Start development mode (local Python)"
	@echo -e "  $(FONT_PURPLE)api            $(FONT_RESET) Start API server with auto-reload"
	@echo -e "  $(FONT_PURPLE)worker         $(FONT_RESET) Start Celery worker"
	@echo -e "  $(FONT_PURPLE)scheduler      $(FONT_RESET) Start Celery scheduler"
	@echo -e "  $(FONT_PURPLE)docker         $(FONT_RESET) Start Docker development stack"
	@echo -e "  $(FONT_PURPLE)prod           $(FONT_RESET) Start production Docker stack"
	@echo -e "  $(FONT_PURPLE)stop           $(FONT_RESET) Stop development services"
	@echo -e "  $(FONT_PURPLE)stop-all       $(FONT_RESET) Stop all services and containers"
	@echo -e "  $(FONT_RED)purge-containers$(FONT_RESET) $(WARNING) PURGE AutoMagik containers, images & volumes"
	@echo ""
	@echo -e "$(FONT_CYAN)🔧 Development Tools:$(FONT_RESET)"
	@echo -e "  $(FONT_PURPLE)test           $(FONT_RESET) Run the test suite"
	@echo -e "  $(FONT_PURPLE)test-coverage  $(FONT_RESET) Run tests with coverage report"
	@echo -e "  $(FONT_PURPLE)lint           $(FONT_RESET) Run code linting with ruff"
	@echo -e "  $(FONT_PURPLE)lint-fix       $(FONT_RESET) Fix auto-fixable linting issues"
	@echo -e "  $(FONT_PURPLE)format         $(FONT_RESET) Format code with black"
	@echo -e "  $(FONT_PURPLE)typecheck      $(FONT_RESET) Run type checking with mypy"
	@echo -e "  $(FONT_PURPLE)quality        $(FONT_RESET) Run all code quality checks"
	@echo ""
	@echo -e "$(FONT_CYAN)🗃️ Database & Migrations:$(FONT_RESET)"
	@echo -e "  $(FONT_YELLOW)db-init        $(FONT_RESET) Initialize database with migrations"
	@echo -e "  $(FONT_YELLOW)db-migrate     $(FONT_RESET) Run database migrations"
	@echo -e "  $(FONT_YELLOW)db-reset       $(FONT_RESET) Reset database (WARNING: destroys data)"
	@echo -e "  $(FONT_YELLOW)db-revision    $(FONT_RESET) Create new migration revision"
	@echo ""
	@echo -e "$(FONT_CYAN)📋 CLI Commands:$(FONT_RESET)"
	@echo -e "  $(FONT_CYAN)cli-workflows  $(FONT_RESET) List workflows via CLI"
	@echo -e "  $(FONT_CYAN)cli-sources    $(FONT_RESET) List sources via CLI"
	@echo -e "  $(FONT_CYAN)cli-tasks      $(FONT_RESET) List tasks via CLI"
	@echo -e "  $(FONT_CYAN)cli-schedules  $(FONT_RESET) List schedules via CLI"
	@echo ""
	@echo -e "$(FONT_CYAN)🔧 System Service:$(FONT_RESET)"
	@echo -e "  $(FONT_GREEN)install-service$(FONT_RESET) Install systemd service"
	@echo -e "  $(FONT_GREEN)start-service  $(FONT_RESET) Start the systemd service"
	@echo -e "  $(FONT_GREEN)stop-service   $(FONT_RESET) Stop the systemd service"
	@echo -e "  $(FONT_GREEN)restart-service$(FONT_RESET) Restart the systemd service"
	@echo -e "  $(FONT_GREEN)service-status $(FONT_RESET) Check service status"
	@echo -e "  $(FONT_GREEN)logs           $(FONT_RESET) Show service logs (follow)"
	@echo -e "  $(FONT_GREEN)logs-tail      $(FONT_RESET) Show recent service logs"
	@echo ""
	@echo -e "$(FONT_CYAN)📦 Publishing & Release:$(FONT_RESET)"
	@echo -e "  $(FONT_PURPLE)build          $(FONT_RESET) Build the project"
	@echo -e "  $(FONT_PURPLE)check-dist     $(FONT_RESET) Check package quality"
	@echo -e "  $(FONT_PURPLE)check-release  $(FONT_RESET) Check if ready for release"
	@echo -e "  $(FONT_PURPLE)publish-test   $(FONT_RESET) Publish to Test PyPI"
	@echo -e "  $(FONT_PURPLE)publish        $(FONT_RESET) Publish to PyPI + GitHub release"
	@echo -e "  $(FONT_PURPLE)publish-docker $(FONT_RESET) Build and publish Docker images"
	@echo -e "  $(FONT_PURPLE)publish-all    $(FONT_RESET) Full publish: PyPI + Docker images"
	@echo -e "  $(FONT_PURPLE)release        $(FONT_RESET) Full release process (quality + test + build)"
	@echo ""
	@echo -e "$(FONT_CYAN)🏷️ Version & Git Automation:$(FONT_RESET)"
	@echo -e "  $(FONT_GREEN)bump-patch     $(FONT_RESET) Bump patch version (0.1.0 → 0.1.1)"
	@echo -e "  $(FONT_GREEN)bump-minor     $(FONT_RESET) Bump minor version (0.1.0 → 0.2.0)"
	@echo -e "  $(FONT_GREEN)bump-major     $(FONT_RESET) Bump major version (0.1.0 → 1.0.0)"
	@echo -e "  $(FONT_YELLOW)bump-dev       $(FONT_RESET) Create dev pre-release (0.1.0 → 0.1.0pre1)"
	@echo -e "  $(FONT_CYAN)tag-current    $(FONT_RESET) Create git tag for current version"
	@echo -e "  $(FONT_CYAN)commit-version $(FONT_RESET) Commit version changes"
	@echo -e "  $(FONT_CYAN)push-tags      $(FONT_RESET) Push tags to remote"
	@echo ""
	@echo -e "$(FONT_CYAN)🚀 Automated Release Workflows:$(FONT_RESET)"
	@echo -e "  $(FONT_GREEN)release-patch  $(FONT_RESET) Full patch release (bump + commit + tag + test + build)"
	@echo -e "  $(FONT_GREEN)release-minor  $(FONT_RESET) Full minor release (bump + commit + tag + test + build)"
	@echo -e "  $(FONT_GREEN)release-major  $(FONT_RESET) Full major release (bump + commit + tag + test + build)"
	@echo -e "  $(FONT_YELLOW)release-dev    $(FONT_RESET) Dev pre-release (bump + commit + tag + build)"
	@echo -e "  $(FONT_PURPLE)deploy-release $(FONT_RESET) Deploy release (push tags + publish-all + auto GitHub release)"
	@echo -e "  $(FONT_YELLOW)deploy-dev     $(FONT_RESET) Deploy dev release (push tags + Test PyPI + auto GitHub release)"
	@echo ""
	@echo -e "$(FONT_CYAN)🚀 Quick Commands:$(FONT_RESET)"
	@echo -e "  $(FONT_CYAN)up             $(FONT_RESET) Quick start: install + dev services"
	@echo -e "  $(FONT_CYAN)check          $(FONT_RESET) Quick check: quality + tests"
	@echo -e "  $(FONT_GREEN)deploy-service $(FONT_RESET) Deploy as service: install + service + start"
	@echo ""
	@echo -e "$(FONT_YELLOW)💡 First time? Try: make setup-local or make setup-dev$(FONT_RESET)"
	@echo ""

# ===========================================
# 🏗️ Installation & Setup Commands
# ===========================================
.PHONY: install setup-local setup-dev install-deps install-docker install-prod
install: ## Install AutoMagik Spark environment
	@$(call print_status,Installing AutoMagik Spark environment...)
	@$(call check_prerequisites)
	@$(call setup_python_env)
	@$(call ensure_env_file)
	@$(call print_success_with_logo,AutoMagik Spark installed successfully!)

setup-local: ## Run local production setup script
	@$(call print_status,Running local production setup...)
	@if [ -f "scripts/setup_local.sh" ]; then \
		bash scripts/setup_local.sh; \
	else \
		$(call print_error,scripts/setup_local.sh not found); \
		exit 1; \
	fi
	@$(call print_success_with_logo,Local production setup complete!)

setup-dev: ## Run development setup script
	@$(call print_status,Running development setup...)
	@if [ -f "scripts/setup_dev.sh" ]; then \
		bash scripts/setup_dev.sh; \
	else \
		$(call print_error,scripts/setup_dev.sh not found); \
		exit 1; \
	fi
	@$(call print_success_with_logo,Development setup complete!)

install-deps: ## Install optional dependencies (PostgreSQL, Redis)
	@$(call print_status,Installing optional dependencies...)
	@$(call install_docker_if_needed)
	@$(call check_docker)
	@$(call ensure_env_file)
	@$(call print_status,Starting PostgreSQL and Redis containers...)
	@if [ -f "$(DOCKER_COMPOSE_DEV)" ]; then \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) up -d postgres redis; \
		$(call print_success,PostgreSQL and Redis containers started); \
	else \
		$(call print_warning,Docker compose file not found - using docker-compose.yml); \
		$(DOCKER_COMPOSE) up -d postgres redis || $(DOCKER_COMPOSE) up -d db redis; \
	fi
	@$(call print_success_with_logo,Dependencies installed successfully!)

install-docker: ## Install with Docker for development
	@$(call print_status,Installing Docker development environment...)
	@$(call install_docker_if_needed)
	@$(call check_docker)
	@$(call ensure_env_file)
	@if [ -f "$(DOCKER_COMPOSE_DEV)" ]; then \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) build; \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) up -d; \
	else \
		$(DOCKER_COMPOSE) build; \
		$(DOCKER_COMPOSE) up -d; \
	fi
	@$(call print_success_with_logo,Docker development environment ready!)

install-prod: ## Install production Docker environment
	@$(call print_status,Installing production Docker environment...)
	@$(call install_docker_if_needed)
	@$(call check_docker)
	@if [ ! -f ".env.prod" ] && [ ! -f ".env" ]; then \
		$(call print_error,.env.prod or .env file required for production); \
		exit 1; \
	fi
	@if [ -f "$(DOCKER_COMPOSE_PROD)" ]; then \
		env_file=".env.prod"; \
		[ ! -f "$$env_file" ] && env_file=".env"; \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_PROD) --env-file $$env_file build; \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_PROD) --env-file $$env_file up -d; \
	else \
		$(call print_error,$(DOCKER_COMPOSE_PROD) not found); \
		exit 1; \
	fi
	@$(call print_success_with_logo,Production Docker environment ready!)

# ===========================================
# 🎛️ Service Management Commands
# ===========================================
.PHONY: dev api worker scheduler docker prod stop stop-all purge-containers

dev: ## Start development mode (local Python)
	@$(call check_prerequisites)
	@$(call ensure_env_file)
	@$(call print_status,Starting AutoMagik Spark development mode...)
	@if [ ! -d "$(VENV_PATH)" ]; then \
		$(call print_error,Virtual environment not found); \
		echo -e "$(FONT_YELLOW)💡 Run 'make install' first$(FONT_RESET)"; \
		exit 1; \
	fi
	@$(call print_status,Starting API server with auto-reload...)
	@$(UV) run uvicorn automagik_spark.api.app:app --host $(HOST) --port $(PORT) --reload --log-level $(shell echo "$(LOG_LEVEL)" | tr '[:upper:]' '[:lower:]')

api: ## Start API server with auto-reload
	@$(call check_prerequisites)
	@$(call ensure_env_file)
	@$(call print_status,Starting AutoMagik Spark API server...)
	@$(UV) run uvicorn automagik_spark.api.app:app --host $(HOST) --port $(PORT) --reload --log-level $(shell echo "$(LOG_LEVEL)" | tr '[:upper:]' '[:lower:]')

worker: ## Start Celery worker
	@$(call check_prerequisites)
	@$(call print_status,Starting Celery worker...)
	@$(UV) run celery -A automagik_spark.core.celery.celery_app worker --loglevel=$(LOG_LEVEL)

scheduler: ## Start Celery scheduler
	@$(call check_prerequisites)
	@$(call print_status,Starting Celery scheduler...)
	@$(UV) run celery -A automagik_spark.core.celery.celery_app beat --loglevel=$(LOG_LEVEL)

docker: ## Start Docker development stack
	@$(call print_status,Starting Docker development stack...)
	@$(call check_docker)
	@$(call ensure_env_file)
	@if [ -f "$(DOCKER_COMPOSE_DEV)" ]; then \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) up -d; \
	else \
		$(DOCKER_COMPOSE) up -d; \
	fi
	@$(call print_success_with_logo,Docker development stack started!)

prod: ## Start production Docker stack
	@$(call print_status,Starting production Docker stack...)
	@$(call check_docker)
	@if [ -f "$(DOCKER_COMPOSE_PROD)" ]; then \
		env_file=".env.prod"; \
		[ ! -f "$$env_file" ] && env_file=".env"; \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_PROD) --env-file $$env_file up -d; \
	else \
		$(call print_error,$(DOCKER_COMPOSE_PROD) not found); \
		exit 1; \
	fi
	@$(call print_success_with_logo,Production Docker stack started!)

stop: ## Stop development services
	@$(call print_status,Stopping development services...)
	@pkill -f "celery.*automagik" 2>/dev/null || true
	@pkill -f "uvicorn.*automagik" 2>/dev/null || true
	@if [ -f "$(DOCKER_COMPOSE_DEV)" ]; then \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) stop automagik-api automagik-worker 2>/dev/null || true; \
	fi
	@$(call print_success,Development services stopped!)

stop-all: ## Stop all services and containers
	@$(call print_status,Stopping all AutoMagik Spark services...)
	@pkill -f "celery.*automagik" 2>/dev/null || true
	@pkill -f "uvicorn.*automagik" 2>/dev/null || true
	@pm2 stop automagik-spark 2>/dev/null || true
	@if [ -f "$(DOCKER_COMPOSE_DEV)" ]; then \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) down 2>/dev/null || true; \
	fi
	@if [ -f "$(DOCKER_COMPOSE_PROD)" ]; then \
		env_file=".env.prod"; \
		[ ! -f "$$env_file" ] && env_file=".env"; \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_PROD) --env-file $$env_file down 2>/dev/null || true; \
	fi
	@$(DOCKER_COMPOSE) down 2>/dev/null || true
	@$(call print_success_with_logo,All services stopped!)

purge-containers: ## ⚠️ PURGE AutoMagik Spark containers, images and volumes
	@$(call print_status,WARNING: This will delete AutoMagik Spark Docker containers, images, and volumes!)
	@echo -e "$(FONT_RED)$(WARNING) This action will remove:$(FONT_RESET)"
	@echo -e "  - Stop and remove AutoMagik containers (automagik-*)"
	@echo -e "  - Remove AutoMagik Docker images"
	@echo -e "  - Remove AutoMagik Docker volumes"
	@echo -e "  - Remove AutoMagik Docker networks"
	@echo -e "  - Keep other Docker resources intact"
	@echo ""
	@echo -n "$(FONT_RED)Continue with AutoMagik cleanup? (yes/no): $(FONT_RESET)"; \
	read confirm; \
	if [ "$$confirm" = "yes" ]; then \
		echo -e "$(FONT_GREEN)[+]$(FONT_RESET) Purging AutoMagik Spark Docker resources..."; \
		echo "Stopping AutoMagik containers..."; \
		$(DOCKER_COMPOSE) -p automagik -f docker/docker-compose.yml down --volumes --remove-orphans 2>/dev/null || true; \
		docker stop $$(docker ps -q --filter "name=automagik") 2>/dev/null || true; \
		echo "Removing AutoMagik containers..."; \
		docker rm $$(docker ps -aq --filter "name=automagik") 2>/dev/null || true; \
		echo "Removing AutoMagik images..."; \
		docker rmi $$(docker images -q --filter "reference=automagik*") 2>/dev/null || true; \
		docker rmi $$(docker images -q --filter "reference=*automagik*") 2>/dev/null || true; \
		docker rmi automagik_automagik-api:latest automagik_automagik-worker:latest 2>/dev/null || true; \
		echo "Removing AutoMagik volumes..."; \
		docker volume rm $$(docker volume ls -q --filter "name=automagik") 2>/dev/null || true; \
		echo "Removing AutoMagik networks..."; \
		docker network rm automagik-network 2>/dev/null || true; \
		echo "Cleaning up dangling AutoMagik resources..."; \
		docker system prune -f --filter "label=com.docker.compose.project=automagik" 2>/dev/null || true; \
		echo -e "$(FONT_GREEN)$(CHECKMARK) AutoMagik Spark Docker resources purged!$(FONT_RESET)"; \
	else \
		echo -e "$(FONT_BLUE)$(INFO) Operation cancelled.$(FONT_RESET)"; \
	fi

.PHONY: test
test: ## Run the test suite
	$(call check_prerequisites)
	$(call print_status,Running test suite)
	@$(UV) run pytest tests/ -v --tb=short
	$(call print_success,Tests completed)

.PHONY: test-coverage
test-coverage: ## Run tests with detailed coverage report (HTML + terminal)
	$(call check_prerequisites)
	$(call print_status,Running tests with coverage)
	@$(UV) run pytest tests/ --cov=automagik_spark --cov-report=html --cov-report=term-missing --cov-report=term:skip-covered
	$(call print_info,Coverage report generated in htmlcov/)
	$(call print_info,Open htmlcov/index.html in browser to view detailed report)

.PHONY: lint
lint: ## Run code linting with ruff
	$(call check_prerequisites)
	$(call print_status,Running ruff linter)
	@$(UV) run ruff check automagik_spark/ tests/
	$(call print_success,Linting completed)

.PHONY: lint-fix
lint-fix: ## Fix auto-fixable linting issues
	$(call check_prerequisites)
	$(call print_status,Fixing linting issues with ruff)
	@$(UV) run ruff check automagik_spark/ tests/ --fix
	$(call print_success,Auto-fixable issues resolved)

.PHONY: format
format: ## Format code with black
	$(call check_prerequisites)
	$(call print_status,Formatting code with black)
	@$(UV) run black automagik_spark/ tests/
	$(call print_success,Code formatted)

.PHONY: typecheck
typecheck: ## Run type checking with mypy
	$(call check_prerequisites)
	$(call print_status,Running type checks with mypy)
	@$(UV) run mypy automagik_spark/
	$(call print_success,Type checking completed)

.PHONY: quality
quality: lint typecheck ## Run all code quality checks
	$(call print_success,All quality checks completed)

# ===========================================
# 🗃️ Database & Migrations
# ===========================================
.PHONY: db-init
db-init: ## Initialize database with migrations
	$(call check_prerequisites)
	$(call print_status,Initializing database)
	@$(UV) run alembic upgrade head
	$(call print_success,Database initialized)

.PHONY: db-migrate
db-migrate: ## Run database migrations
	$(call check_prerequisites)
	$(call print_status,Running database migrations)
	@$(UV) run alembic upgrade head
	$(call print_success,Migrations completed)

.PHONY: db-reset
db-reset: ## Reset database (WARNING: destroys data)
	$(call print_warning,This will destroy all data in the database!)
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(call print_status,Resetting database); \
		bash scripts/reset_db.sh; \
		$(call print_success,Database reset completed); \
	else \
		$(call print_info,Database reset cancelled); \
	fi

.PHONY: db-revision
db-revision: ## Create new migration revision
	$(call check_prerequisites)
	$(call print_status,Creating new migration revision)
	@read -p "Enter migration message: " MESSAGE; \
	$(UV) run alembic revision --autogenerate -m "$$MESSAGE"
	$(call print_success,Migration revision created)

# ===========================================
# 🔧 CLI Commands
# ===========================================
.PHONY: cli-workflows
cli-workflows: ## List workflows via CLI
	$(call check_prerequisites)
	$(call print_status,Listing workflows)
	@$(UV) run automagik-spark workflow list

.PHONY: cli-sources
cli-sources: ## List sources via CLI
	$(call check_prerequisites)
	$(call print_status,Listing sources)
	@$(UV) run automagik-spark source list

.PHONY: cli-tasks
cli-tasks: ## List tasks via CLI
	$(call check_prerequisites)
	$(call print_status,Listing tasks)
	@$(UV) run automagik-spark task list

.PHONY: cli-schedules
cli-schedules: ## List schedules via CLI
	$(call check_prerequisites)
	$(call print_status,Listing schedules)
	@$(UV) run automagik-spark schedule list

# ===========================================
# 🐳 Docker Commands
# ===========================================
.PHONY: docker-build
docker-build: ## Build Docker images
	$(call print_status,Building Docker images)
	@docker-compose -f docker/docker-compose.yml build
	$(call print_success,Docker images built)

.PHONY: docker-up
docker-up: ## Start Docker services
	$(call print_status,Starting Docker services)
	@docker-compose -f docker/docker-compose.yml up -d
	$(call print_success,Docker services started)

.PHONY: docker-down
docker-down: ## Stop Docker services
	$(call print_status,Stopping Docker services)
	@docker-compose -f docker/docker-compose.yml down
	$(call print_success,Docker services stopped)

.PHONY: docker-logs
docker-logs: ## Show Docker container logs (N=lines FOLLOW=1 for follow mode)
	$(eval N := $(or $(N),30))
	$(call print_status,Showing Docker logs)
	@if [ "$(FOLLOW)" = "1" ]; then \
		echo -e "$(FONT_YELLOW)Press Ctrl+C to stop following logs$(FONT_RESET)"; \
		docker-compose -f docker/docker-compose.yml logs -f --tail=$(N); \
	else \
		docker-compose -f docker/docker-compose.yml logs --tail=$(N); \
	fi

# ===========================================
# 🔧 Service Management
# ===========================================
.PHONY: restart-service install-service start-service stop-service uninstall-service service-status logs-follow
uninstall-service: ## Uninstall PM2 service
	$(call print_status,Uninstalling PM2 service)
	@$(call check_pm2)
	@pm2 delete automagik-spark 2>/dev/null || true
	@pm2 save --force
	@echo -e "$(FONT_GREEN)$(CHECKMARK) PM2 service uninstalled!$(FONT_RESET)"

install-service: ## Install local PM2 service
	@$(call print_status,Installing AutoMagik Spark as local PM2 service...)
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo -e "$(FONT_YELLOW)$(WARNING) Virtual environment not found - creating it now...$(FONT_RESET)"; \
		$(MAKE) install; \
	fi
	@$(call ensure_env_file)
	@$(MAKE) setup-pm2
	@$(MAKE) start-local
	@$(call print_success_with_logo,Local PM2 service installed!)
	@$(call print_info,💡 Service is now managed by local PM2)

.PHONY: start-service
start-service: ## Start local PM2 service
	@$(MAKE) start-local

.PHONY: stop-service
stop-service: ## Stop local PM2 service
	@$(MAKE) stop-local

.PHONY: restart-service
restart-service: ## Restart local PM2 service
	@$(MAKE) restart-local

.PHONY: service-status
service-status: ## Check local PM2 service status
	$(call print_status,Checking AutoMagik Spark service status)
	@$(call check_pm2)
	@pm2 show automagik-spark 2>/dev/null || echo "Service not found"

.PHONY: logs
logs: ## Show service logs (N=lines)
	$(eval N := $(or $(N),30))
	$(call print_status,Recent $(SERVICE_NAME) logs)
	@pm2 logs automagik-spark --lines $(N) --nostream 2>/dev/null || echo -e "$(FONT_YELLOW)⚠️ Service not found or not running$(FONT_RESET)"

.PHONY: logs-tail
logs-follow: ## Follow service logs in real-time
	$(call print_status,Following $(SERVICE_NAME) logs)
	@echo -e "$(FONT_YELLOW)Press Ctrl+C to stop following logs$(FONT_RESET)"
	@pm2 logs automagik-spark 2>/dev/null || echo -e "$(FONT_YELLOW)⚠️ Service not found or not running$(FONT_RESET)"

# ===========================================
# 🔧 Local PM2 Management (Standalone Mode)
# ===========================================
.PHONY: setup-pm2 start-local stop-local restart-local
setup-pm2: ## 📦 Setup local PM2 ecosystem
	$(call print_status,Setting up local PM2 ecosystem...)
	@$(call check_pm2)
	@echo -e "$(FONT_CYAN)$(INFO) Installing PM2 log rotation...$(FONT_RESET)"
	@if ! pm2 list | grep -q pm2-logrotate; then \
		pm2 install pm2-logrotate; \
	else \
		echo -e "$(FONT_GREEN)✓ PM2 logrotate already installed$(FONT_RESET)"; \
	fi
	@pm2 set pm2-logrotate:max_size 100M
	@pm2 set pm2-logrotate:retain 7
	@echo -e "$(FONT_CYAN)$(INFO) Setting up PM2 startup...$(FONT_RESET)"
	@if ! pm2 startup -s 2>/dev/null; then \
		echo -e "$(FONT_YELLOW)Warning: PM2 startup may already be configured$(FONT_RESET)"; \
	fi
	@$(call print_success,Local PM2 ecosystem configured!)

start-local: ## 🚀 Start service using local PM2 ecosystem
	$(call print_status,Starting automagik-spark with local PM2...)
	@$(call check_pm2)
	@if [ ! -d "$(VENV_PATH)" ]; then \
		$(call print_error,Virtual environment not found); \
		echo -e "$(FONT_YELLOW)💡 Run 'make install' first$(FONT_RESET)"; \
		exit 1; \
	fi
	@$(call ensure_env_file)
	@pm2 start ecosystem.config.js
	@$(call print_success,Service started with local PM2!)

stop-local: ## 🛑 Stop service using local PM2 ecosystem
	$(call print_status,Stopping automagik-spark with local PM2...)
	@$(call check_pm2)
	@pm2 stop automagik-spark 2>/dev/null || true
	@$(call print_success,Service stopped!)

restart-local: ## 🔄 Restart service using local PM2 ecosystem
	$(call print_status,Restarting automagik-spark with local PM2...)
	@$(call check_pm2)
	@pm2 restart automagik-spark 2>/dev/null || pm2 start ecosystem.config.js
	@$(call print_success,Service restarted!)

# ===========================================
# 📦 Publishing & Release
# ===========================================
.PHONY: build check-dist check-release
build: clean ## 📦 Build package
	$(call check_prerequisites)
	$(call print_status,Building package...)
	@$(UV) build
	$(call print_success,Package built!)

check-dist: ## 🔍 Check package quality
	$(call print_status,Checking package quality...)
	@$(UV) run twine check dist/*

check-release: ## 🔍 Check if ready for release (clean working directory)
	$(call print_status,Checking release readiness...)
	@# Check for uncommitted changes
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo -e "$(FONT_RED)$(ERROR) Uncommitted changes detected!$(FONT_RESET)"; \
		echo -e "$(FONT_YELLOW)Please commit or stash your changes before publishing.$(FONT_RESET)"; \
		echo -e "$(FONT_CYAN)Run: git status$(FONT_RESET)"; \
		exit 1; \
	fi
	@# Check if on main branch
	@CURRENT_BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	if [ "$$CURRENT_BRANCH" != "main" ]; then \
		echo -e "$(FONT_YELLOW)$(WARNING) Not on main branch (current: $$CURRENT_BRANCH)$(FONT_RESET)"; \
		echo -e "$(FONT_YELLOW)It's recommended to publish from the main branch.$(FONT_RESET)"; \
		read -p "Continue anyway? [y/N] " -n 1 -r; \
		echo; \
		if [[ ! $$REPLY =~ ^[Yy]$$ ]]; then \
			exit 1; \
		fi; \
	fi
	@# Check if main branch is up to date with origin
	@git fetch origin >/dev/null 2>&1 || true
	@LOCAL=$$(git rev-parse HEAD); \
	REMOTE=$$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null || echo ""); \
	if [ -n "$$REMOTE" ] && [ "$$LOCAL" != "$$REMOTE" ]; then \
		echo -e "$(FONT_YELLOW)$(WARNING) Local branch is not up to date with origin$(FONT_RESET)"; \
		echo -e "$(FONT_YELLOW)Consider running: git pull origin main$(FONT_RESET)"; \
		read -p "Continue anyway? [y/N] " -n 1 -r; \
		echo; \
		if [[ ! $$REPLY =~ ^[Yy]$$ ]]; then \
			exit 1; \
		fi; \
	fi
	$(call print_success,Ready for release!)

.PHONY: publish-test
publish-test: build check-dist ## 🧪 Upload to TestPyPI
	$(call print_status,Publishing to TestPyPI...)
	@if [ -z "$$TESTPYPI_TOKEN" ]; then \
		$(call print_error,TESTPYPI_TOKEN not set); \
		echo -e "$(FONT_YELLOW)💡 Get your TestPyPI token at: https://test.pypi.org/manage/account/token/$(FONT_RESET)"; \
		echo -e "$(FONT_CYAN)💡 Set with: export TESTPYPI_TOKEN=pypi-xxxxx$(FONT_RESET)"; \
		exit 1; \
	fi
	@$(UV) run twine upload --repository testpypi dist/* -u __token__ -p "$$TESTPYPI_TOKEN"
	$(call print_success,Published to TestPyPI!)

.PHONY: publish-pypi publish
publish-pypi: publish ## Legacy alias for publish

publish: check-release build check-dist ## $(ROCKET) Upload to PyPI and create GitHub release
	$(call print_status,Publishing to PyPI and GitHub...)
	@if [ -z "$$PYPI_TOKEN" ]; then \
		echo -e "$(FONT_RED)$(ERROR) PYPI_TOKEN environment variable not set$(FONT_RESET)"; \
		echo -e "$(FONT_YELLOW)💡 Get your PyPI token at: https://pypi.org/manage/account/token/$(FONT_RESET)"; \
		echo -e "$(FONT_CYAN)💡 Set with: export PYPI_TOKEN=pypi-xxxxx$(FONT_RESET)"; \
		exit 1; \
	fi
	@# Get version from version.py
	@VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	echo -e "$(FONT_CYAN)$(INFO) Publishing version: v$$VERSION$(FONT_RESET)"; \
	$(UV) run twine upload dist/* -u __token__ -p "$$PYPI_TOKEN"; \
	if ! git tag | grep -q "^v$$VERSION$$"; then \
		echo -e "$(FONT_CYAN)$(INFO) Creating git tag v$$VERSION$(FONT_RESET)"; \
		git tag -a "v$$VERSION" -m "Release v$$VERSION" \
			-m "" \
			-m "Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>"; \
	fi; \
	echo -e "$(FONT_CYAN)$(INFO) Pushing tag to GitHub$(FONT_RESET)"; \
	git push origin "v$$VERSION"; \
	if command -v gh >/dev/null 2>&1; then \
		echo -e "$(FONT_CYAN)$(INFO) Creating GitHub release$(FONT_RESET)"; \
		gh release create "v$$VERSION" \
			--title "automagik-spark v$$VERSION" \
			--notes "Release v$$VERSION - See commit history for details" \
			--latest; \
	else \
		echo -e "$(FONT_YELLOW)$(WARNING) gh CLI not found - skipping GitHub release$(FONT_RESET)"; \
	fi; \
	$(call print_success,Published to PyPI and GitHub!)

.PHONY: publish-docker
publish-docker: ## Build and publish Docker images
	$(call check_prerequisites)
	$(call print_status,Building and publishing Docker images)
	@$(call print_info,Building automagik-spark-api image...)
	@docker build -f docker/Dockerfile.api -t namastexlabs/automagik-spark-api:latest -t namastexlabs/automagik-spark-api:v$(shell grep "^version" pyproject.toml | cut -d'"' -f2) .
	@$(call print_info,Building automagik-spark-worker image...)
	@docker build -f docker/Dockerfile.worker -t namastexlabs/automagik-spark-worker:latest -t namastexlabs/automagik-spark-worker:v$(shell grep "^version" pyproject.toml | cut -d'"' -f2) .
	@$(call print_info,Pushing automagik-spark-api images...)
	@docker push namastexlabs/automagik-spark-api:latest
	@docker push namastexlabs/automagik-spark-api:v$(shell grep "^version" pyproject.toml | cut -d'"' -f2)
	@$(call print_info,Pushing automagik-spark-worker images...)
	@docker push namastexlabs/automagik-spark-worker:latest
	@docker push namastexlabs/automagik-spark-worker:v$(shell grep "^version" pyproject.toml | cut -d'"' -f2)
	$(call print_success,Docker images published successfully)

.PHONY: publish-all
publish-all: publish publish-docker ## Full publish: PyPI + Docker images
	$(call print_success_with_logo,Successfully published automagik-spark!)
	@$(call print_info,PyPI: pip install automagik-spark)
	@$(call print_info,Docker: docker pull namastexlabs/automagik-spark-api:latest)
	@$(call print_info,Docker: docker pull namastexlabs/automagik-spark-worker:latest)

.PHONY: release
release: quality test build ## Full release process (quality + test + build)
	$(call print_success_with_logo,Release build ready)
	$(call print_info,Run 'make publish-test', 'make publish', 'make publish-docker', or 'make publish-all' to deploy)

# ===========================================
# 🧹 Cleanup & Maintenance
# ===========================================
.PHONY: clean
clean: ## Clean build artifacts and cache
	$(call print_status,Cleaning build artifacts)
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info/
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	$(call print_success,Cleanup completed)


# ===========================================
# 🚀 Quick Commands
# ===========================================
.PHONY: up
up: install dev ## Quick start: install + dev services

.PHONY: check
check: quality test ## Quick check: quality + tests

.PHONY: deploy-service
deploy-service: install install-service start-service ## Deploy as service: install + service + start
	$(call print_success_with_logo,AutoMagik Spark deployed as service and ready!)

# ===========================================
# 📊 Status & Info
# ===========================================
.PHONY: info
info: ## Show project information
	@echo ""
	@echo -e "$(FONT_PURPLE)$(AUTOMAGIK) AutoMagik Spark Project Information$(FONT_RESET)"
	@echo -e "$(FONT_CYAN)Project Root:$(FONT_RESET) $(PROJECT_ROOT)"
	@echo -e "$(FONT_CYAN)Python:$(FONT_RESET) $(shell python3 --version 2>/dev/null || echo 'Not found')"
	@echo -e "$(FONT_CYAN)UV:$(FONT_RESET) $(shell uv --version 2>/dev/null || echo 'Not found')"
	@echo -e "$(FONT_CYAN)Service:$(FONT_RESET) $(SERVICE_NAME)"
	@echo ""
	$(call check_service_status)
	@echo ""

# ===========================================
# 📈 Version Management & Git Automation
# ===========================================
.PHONY: bump-patch bump-minor bump-major bump-dev finalize-version tag-current release-patch release-minor release-major release-dev

bump-patch: ## 📈 Bump patch version (0.1.0 -> 0.1.1)
	$(call print_status,Bumping patch version...)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	NEW_VERSION=$$(echo $$CURRENT_VERSION | awk -F. '{$$NF = $$NF + 1;} 1' | sed 's/ /./g'); \
	sed -i "s/version = \"$$CURRENT_VERSION\"/version = \"$$NEW_VERSION\"/" pyproject.toml; \
	echo -e "$(FONT_GREEN)✅ Version bumped from $$CURRENT_VERSION to $$NEW_VERSION$(FONT_RESET)"

bump-minor: ## 📈 Bump minor version (0.1.0 -> 0.2.0)
	$(call print_status,Bumping minor version...)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	NEW_VERSION=$$(echo $$CURRENT_VERSION | awk -F. '{$$2 = $$2 + 1; $$3 = 0;} 1' | sed 's/ /./g'); \
	sed -i "s/version = \"$$CURRENT_VERSION\"/version = \"$$NEW_VERSION\"/" pyproject.toml; \
	echo -e "$(FONT_GREEN)✅ Version bumped from $$CURRENT_VERSION to $$NEW_VERSION$(FONT_RESET)"

bump-major: ## 📈 Bump major version (0.1.0 -> 1.0.0)
	$(call print_status,Bumping major version...)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	NEW_VERSION=$$(echo $$CURRENT_VERSION | awk -F. '{$$1 = $$1 + 1; $$2 = 0; $$3 = 0;} 1' | sed 's/ /./g'); \
	sed -i "s/version = \"$$CURRENT_VERSION\"/version = \"$$NEW_VERSION\"/" pyproject.toml; \
	echo -e "$(FONT_GREEN)✅ Version bumped from $$CURRENT_VERSION to $$NEW_VERSION$(FONT_RESET)"

bump-dev: ## 🧪 Create dev version (0.1.2 -> 0.1.2pre1, 0.1.2pre1 -> 0.1.2pre2)
	$(call print_status,Creating dev pre-release version...)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	if echo "$$CURRENT_VERSION" | grep -q "pre"; then \
		BASE_VERSION=$$(echo "$$CURRENT_VERSION" | cut -d'p' -f1); \
		PRE_NUM=$$(echo "$$CURRENT_VERSION" | sed 's/.*pre\([0-9]*\)/\1/'); \
		NEW_PRE_NUM=$$((PRE_NUM + 1)); \
		NEW_VERSION="$${BASE_VERSION}pre$${NEW_PRE_NUM}"; \
	else \
		NEW_VERSION="$${CURRENT_VERSION}pre1"; \
	fi; \
	sed -i "s/version = \"$$CURRENT_VERSION\"/version = \"$$NEW_VERSION\"/" pyproject.toml; \
	echo -e "$(FONT_GREEN)✅ Dev version created: $$CURRENT_VERSION → $$NEW_VERSION$(FONT_RESET)"; \
	echo -e "$(FONT_CYAN)💡 Ready for: make publish-test$(FONT_RESET)"

finalize-version: ## ✅ Remove 'pre' from version (0.1.2pre3 -> 0.1.2)
	$(call print_status,Finalizing version for release...)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	if ! echo "$$CURRENT_VERSION" | grep -q "pre"; then \
		$(call print_error,Not a pre-release version!); \
		echo -e "$(FONT_GRAY)Current version: $$CURRENT_VERSION$(FONT_RESET)"; \
		exit 1; \
	fi; \
	FINAL_VERSION=$$(echo "$$CURRENT_VERSION" | cut -d'p' -f1); \
	sed -i "s/version = \"$$CURRENT_VERSION\"/version = \"$$FINAL_VERSION\"/" pyproject.toml; \
	echo -e "$(FONT_GREEN)✅ Version finalized: $$CURRENT_VERSION → $$FINAL_VERSION$(FONT_RESET)"; \
	echo -e "$(FONT_CYAN)💡 Ready for: make publish$(FONT_RESET)"

# ===========================================
# 🏷️ Git Tagging & Release Automation
# ===========================================

tag-current: ## 🏷️ Create git tag for current version
	$(call print_status,Creating git tag for current version...)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	if git tag -l | grep -q "^v$$CURRENT_VERSION$$"; then \
		$(call print_warning,Tag v$$CURRENT_VERSION already exists); \
	else \
		git tag -a "v$$CURRENT_VERSION" -m "feat: release v$$CURRENT_VERSION"; \
		echo -e "$(FONT_GREEN)✅ Created tag: v$$CURRENT_VERSION$(FONT_RESET)"; \
	fi

commit-version: ## 📝 Commit version change with co-author
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	if git diff --quiet pyproject.toml; then \
		$(call print_info,No version changes to commit); \
	else \
		git add pyproject.toml; \
		git commit -m "chore: bump version to v$$CURRENT_VERSION" \
			-m "" \
			-m "Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>"; \
		echo -e "$(FONT_GREEN)✅ Committed version change: v$$CURRENT_VERSION$(FONT_RESET)"; \
	fi

push-tags: ## 🚀 Push tags to remote
	$(call print_status,Pushing tags to remote...)
	@git push origin --tags
	$(call print_success,Tags pushed to remote!)

create-github-release: ## 🎉 Create GitHub release for current version
	$(call print_status,Creating GitHub release...)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	if gh release view "v$$CURRENT_VERSION" >/dev/null 2>&1; then \
		$(call print_warning,Release v$$CURRENT_VERSION already exists); \
	else \
		gh release create "v$$CURRENT_VERSION" \
			--title "automagik-spark v$$CURRENT_VERSION" \
			--notes "## automagik-spark v$$CURRENT_VERSION" \
			--latest; \
		echo -e "$(FONT_GREEN)✅ GitHub release v$$CURRENT_VERSION created$(FONT_RESET)"; \
	fi

# ===========================================
# 🚀 Automated Release Workflows
# ===========================================

release-patch: bump-patch commit-version tag-current quality test build ## 🚀 Full patch release
	$(call print_success_with_logo,Patch release ready!)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	echo -e "$(FONT_CYAN)📦 Release v$$CURRENT_VERSION is ready$(FONT_RESET)"; \
	echo -e "$(FONT_YELLOW)💡 Next steps:$(FONT_RESET)"; \
	echo -e "  • make push-tags (push to remote)"; \
	echo -e "  • make publish (deploy to PyPI + GitHub release)"; \
	echo -e "  • make publish-all (deploy to PyPI + Docker)"; \
	echo -e "  • Or run: make deploy-release (push + publish)"

release-minor: bump-minor commit-version tag-current quality test build ## 🚀 Full minor release
	$(call print_success_with_logo,Minor release ready!)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	echo -e "$(FONT_CYAN)📦 Release v$$CURRENT_VERSION is ready$(FONT_RESET)"; \
	echo -e "$(FONT_YELLOW)💡 Next steps:$(FONT_RESET)"; \
	echo -e "  • make push-tags (push to remote)"; \
	echo -e "  • make publish (deploy to PyPI + GitHub release)"; \
	echo -e "  • make publish-all (deploy to PyPI + Docker)"; \
	echo -e "  • Or run: make deploy-release (push + publish)"

release-major: bump-major commit-version tag-current quality test build ## 🚀 Full major release
	$(call print_success_with_logo,Major release ready!)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	echo -e "$(FONT_CYAN)📦 Release v$$CURRENT_VERSION is ready$(FONT_RESET)"; \
	echo -e "$(FONT_YELLOW)💡 Next steps:$(FONT_RESET)"; \
	echo -e "  • make push-tags (push to remote)"; \
	echo -e "  • make publish (deploy to PyPI + GitHub release)"; \
	echo -e "  • make publish-all (deploy to PyPI + Docker)"; \
	echo -e "  • Or run: make deploy-release (push + publish)"

release-dev: bump-dev commit-version tag-current build ## 🧪 Dev pre-release
	$(call print_success_with_logo,Dev pre-release ready!)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	echo -e "$(FONT_CYAN)📦 Dev release v$$CURRENT_VERSION is ready$(FONT_RESET)"; \
	echo -e "$(FONT_YELLOW)💡 Next steps:$(FONT_RESET)"; \
	echo -e "  • make push-tags (push to remote)"; \
	echo -e "  • make publish-test (deploy to Test PyPI)"; \
	echo -e "  • Or run: make deploy-dev"

deploy-release: push-tags publish ## 🚀 Deploy release (push tags + publish to production)
	$(call print_success_with_logo,Release deployed successfully!)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	echo -e "$(FONT_GREEN)🎉 automagik-spark v$$CURRENT_VERSION is now live!$(FONT_RESET)"; \
	echo -e "$(FONT_CYAN)📦 PyPI: pip install automagik-spark==$$CURRENT_VERSION$(FONT_RESET)"; \
	echo -e "$(FONT_CYAN)🐳 Docker: docker pull namastexlabs/automagik-spark-api:v$$CURRENT_VERSION$(FONT_RESET)"; \
	echo -e "$(FONT_CYAN)🐳 Docker: docker pull namastexlabs/automagik-spark-worker:v$$CURRENT_VERSION$(FONT_RESET)"; \
	echo -e "$(FONT_YELLOW)🤖 GitHub release will be auto-generated by workflow$(FONT_RESET)"

deploy-dev: push-tags publish-test ## 🧪 Deploy dev release (push tags + test PyPI)
	$(call print_success_with_logo,Dev release deployed!)
	@CURRENT_VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	echo -e "$(FONT_GREEN)🧪 automagik-spark v$$CURRENT_VERSION deployed to Test PyPI$(FONT_RESET)"; \
	echo -e "$(FONT_CYAN)📦 Test: pip install -i https://test.pypi.org/simple/ automagik-spark==$$CURRENT_VERSION$(FONT_RESET)"
