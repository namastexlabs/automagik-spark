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
SERVICE_FILE := /etc/systemd/system/$(SERVICE_NAME).service
SYSTEMCTL := systemctl
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
	@$(call show_automagik_logo)
endef

define show_automagik_logo
	@echo ""
	@echo -e "$(FONT_PURPLE)                                                                                            $(FONT_RESET)"
	@echo -e "$(FONT_PURPLE)                                                                                            $(FONT_RESET)"
	@echo -e "$(FONT_PURPLE)     -+*         -=@%*@@@@@@*  -#@@@%*  =@@*      -%@#+   -*       +%@@@@*-%@*-@@*  -+@@*   $(FONT_RESET)"
	@echo -e "$(FONT_PURPLE)     =@#*  -@@*  -=@%+@@@@@@*-%@@#%*%@@+=@@@*    -+@@#+  -@@*   -#@@%%@@@*-%@+-@@* -@@#*    $(FONT_RESET)"
	@echo -e "$(FONT_PURPLE)    -%@@#* -@@*  -=@@* -@%* -@@**   --@@=@@@@*  -+@@@#+ -#@@%* -*@%*-@@@@*-%@+:@@+#@@*      $(FONT_RESET)"
	@echo -e "$(FONT_PURPLE)   -#@+%@* -@@*  -=@@* -@%* -@@*-+@#*-%@+@@=@@* +@%#@#+ =@##@* -%@#*-@@@@*-%@+-@@@@@*       $(FONT_RESET)"
	@echo -e "$(FONT_PURPLE)  -*@#==@@*-@@*  -+@%* -@%* -%@#*   -+@@=@@++@%-@@=*@#=-@@*-@@*:+@@*  -%@*-%@+-@@#*@@**     $(FONT_RESET)"
	@echo -e "$(FONT_PURPLE)  -@@* -+@%-+@@@@@@@*  -@%*  -#@@@@%@@%+=@@+-=@@@*    -%@*  -@@*-*@@@@%@@*#@@#=%*  -%@@*    $(FONT_RESET)"
	@echo -e "$(FONT_PURPLE) -@@*+  -%@*  -#@%+    -@%+     =#@@*   =@@+          +@%+  -#@#   -*%@@@*@@@@%+     =@@+   $(FONT_RESET)"
	@echo ""
	@echo -e "$(FONT_CYAN)🏢 Built by$(FONT_RESET) $(FONT_BOLD)Namastex Labs$(FONT_RESET) | $(FONT_YELLOW)📄 MIT Licensed$(FONT_RESET) | $(FONT_YELLOW)🌟 Open Source Forever$(FONT_RESET)"
	@echo -e "$(FONT_PURPLE)✨ \"Because magic shouldn't be complicated\"$(FONT_RESET)"
	@echo ""
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
		@echo -e "$(FONT_YELLOW)💡 Edit .env and configure your settings$(FONT_RESET)"; \
	fi
endef

define check_prerequisites
	@if ! command -v python3 >/dev/null 2>&1; then \
		$(call print_error,Python 3 not found); \
		exit 1; \
	fi
	@if ! command -v uv >/dev/null 2>&1; then \
		if [ -f "$$HOME/.local/bin/uv" ]; then \
			export PATH="$$HOME/.local/bin:$$PATH"; \
			$(call print_status,Found uv in $$HOME/.local/bin); \
		else \
			$(call print_status,Installing uv...); \
			curl -LsSf https://astral.sh/uv/install.sh | sh; \
			export PATH="$$HOME/.local/bin:$$PATH"; \
			$(call print_success,uv installed successfully); \
		fi; \
	fi
endef

define setup_python_env
	@$(call print_status,Installing dependencies with uv...)
	@if command -v uv >/dev/null 2>&1; then \
		uv sync; \
	elif [ -f "$$HOME/.local/bin/uv" ]; then \
		$$HOME/.local/bin/uv sync; \
	else \
		$(call print_error,uv not found - please install uv first); \
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


define check_service_status
	@if systemctl is-active --quiet $(SERVICE_NAME); then \
		echo -e "$(FONT_GREEN)$(CHECKMARK) Service $(SERVICE_NAME) is running$(FONT_RESET)"; \
		echo -e "$(FONT_CYAN)   Status: $$(systemctl is-active $(SERVICE_NAME))$(FONT_RESET)"; \
		echo -e "$(FONT_CYAN)   Since:  $$(systemctl show $(SERVICE_NAME) --property=ActiveEnterTimestamp --value | cut -d' ' -f2-3)$(FONT_RESET)"; \
	elif systemctl is-enabled --quiet $(SERVICE_NAME); then \
		echo -e "$(FONT_YELLOW)$(WARNING) Service $(SERVICE_NAME) is enabled but not running$(FONT_RESET)"; \
	else \
		echo -e "$(FONT_RED)$(ERROR) Service $(SERVICE_NAME) is not installed or enabled$(FONT_RESET)"; \
	fi
endef

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
	@echo -e "  $(FONT_PURPLE)install        $(FONT_RESET) Install development environment (uv sync + setup)"
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
	@echo -e "  $(FONT_PURPLE)publish-test   $(FONT_RESET) Publish to Test PyPI"
	@echo -e "  $(FONT_PURPLE)publish-pypi   $(FONT_RESET) Publish to PyPI"
	@echo -e "  $(FONT_PURPLE)publish-docker $(FONT_RESET) Build and publish Docker images"
	@echo -e "  $(FONT_PURPLE)publish        $(FONT_RESET) Full publish: PyPI + Docker images"
	@echo -e "  $(FONT_PURPLE)release        $(FONT_RESET) Full release process (quality + test + build)"
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
install: ## Install development environment
	@$(call print_status,Installing AutoMagik Spark development environment...)
	@$(call check_prerequisites)
	@$(call setup_python_env)
	@$(call ensure_env_file)
	@$(call print_success_with_logo,Development environment ready!)

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
	@$(UV) run uvicorn automagik.api.app:app --host $(HOST) --port $(PORT) --reload --log-level $(shell echo "$(LOG_LEVEL)" | tr '[:upper:]' '[:lower:]')

api: ## Start API server with auto-reload
	@$(call check_prerequisites)
	@$(call ensure_env_file)
	@$(call print_status,Starting AutoMagik Spark API server...)
	@$(UV) run uvicorn automagik.api.app:app --host $(HOST) --port $(PORT) --reload --log-level $(shell echo "$(LOG_LEVEL)" | tr '[:upper:]' '[:lower:]')

worker: ## Start Celery worker
	@$(call check_prerequisites)
	@$(call print_status,Starting Celery worker...)
	@$(UV) run celery -A automagik.core.celery.celery_app worker --loglevel=$(LOG_LEVEL)

scheduler: ## Start Celery scheduler
	@$(call check_prerequisites)
	@$(call print_status,Starting Celery scheduler...)
	@$(UV) run celery -A automagik.core.celery.celery_app beat --loglevel=$(LOG_LEVEL)

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
	@sudo systemctl stop $(SERVICE_NAME) 2>/dev/null || true
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
	@$(UV) run pytest tests/ --cov=automagik --cov-report=html --cov-report=term-missing --cov-report=term:skip-covered
	$(call print_info,Coverage report generated in htmlcov/)
	$(call print_info,Open htmlcov/index.html in browser to view detailed report)

.PHONY: lint
lint: ## Run code linting with ruff
	$(call check_prerequisites)
	$(call print_status,Running ruff linter)
	@$(UV) run ruff check automagik/ tests/
	$(call print_success,Linting completed)

.PHONY: lint-fix
lint-fix: ## Fix auto-fixable linting issues
	$(call check_prerequisites)
	$(call print_status,Fixing linting issues with ruff)
	@$(UV) run ruff check automagik/ tests/ --fix
	$(call print_success,Auto-fixable issues resolved)

.PHONY: format
format: ## Format code with black
	$(call check_prerequisites)
	$(call print_status,Formatting code with black)
	@$(UV) run black automagik/ tests/
	$(call print_success,Code formatted)

.PHONY: typecheck
typecheck: ## Run type checking with mypy
	$(call check_prerequisites)
	$(call print_status,Running type checks with mypy)
	@$(UV) run mypy automagik/
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
docker-logs: ## Show Docker container logs
	$(call print_status,Showing Docker logs)
	@docker-compose -f docker/docker-compose.yml logs -f

# ===========================================
# 🔧 Service Management
# ===========================================
.PHONY: restart-service install-service
restart-service: ## Update systemd service (removes and recreates)
	$(call print_status,Updating systemd service)
	@sudo systemctl stop $(SERVICE_NAME) 2>/dev/null || true
	@sudo rm -f $(SERVICE_FILE)
	@$(MAKE) install-service

install-service: ## Install systemd service
	@$(call print_status,Installing AutoMagik Spark systemd service...)
	@if [ ! -d "$(VENV_PATH)" ]; then \
		$(call print_warning,Virtual environment not found - creating it now...); \
		$(MAKE) install; \
	fi
	@$(call ensure_env_file)
	@if [ ! -f "$(SERVICE_FILE)" ]; then \
		TMP_FILE=$$(mktemp); \
		printf "[Unit]\n" > $$TMP_FILE; \
		printf "Description=AutoMagik Spark Workflow Management Service\n" >> $$TMP_FILE; \
		printf "After=network.target postgresql.service redis.service\n" >> $$TMP_FILE; \
		printf "Wants=network.target\n" >> $$TMP_FILE; \
		printf "\n" >> $$TMP_FILE; \
		printf "[Service]\n" >> $$TMP_FILE; \
		printf "Type=simple\n" >> $$TMP_FILE; \
		printf "User=%s\n" "$(shell whoami)" >> $$TMP_FILE; \
		printf "WorkingDirectory=%s\n" "$(PROJECT_ROOT)" >> $$TMP_FILE; \
		printf "Environment=PATH=%s/bin:%s/.local/bin:/usr/local/bin:/usr/bin:/bin\n" "$(VENV_PATH)" "$(HOME)" >> $$TMP_FILE; \
		printf "EnvironmentFile=%s/.env\n" "$(PROJECT_ROOT)" >> $$TMP_FILE; \
		printf "ExecStart=%s/bin/uvicorn automagik.api.app:app --host $${HOST:-0.0.0.0} --port $${PORT:-8883}\n" "$(VENV_PATH)" >> $$TMP_FILE; \
		printf "Restart=always\n" >> $$TMP_FILE; \
		printf "RestartSec=10\n" >> $$TMP_FILE; \
		printf "StandardOutput=journal\n" >> $$TMP_FILE; \
		printf "StandardError=journal\n" >> $$TMP_FILE; \
		printf "\n" >> $$TMP_FILE; \
		printf "[Install]\n" >> $$TMP_FILE; \
		printf "WantedBy=multi-user.target\n" >> $$TMP_FILE; \
		sudo cp $$TMP_FILE $(SERVICE_FILE); \
		rm $$TMP_FILE; \
		sudo systemctl daemon-reload; \
		sudo systemctl enable $(SERVICE_NAME); \
		$(call print_success,Service installed and enabled); \
	else \
		$(call print_warning,Service already installed); \
	fi
	@$(call print_success_with_logo,AutoMagik Spark systemd service ready!)
	@echo -e "$(FONT_CYAN)💡 Start with: sudo systemctl start $(SERVICE_NAME)$(FONT_RESET)"

.PHONY: start-service
start-service: ## Start the systemd service
	$(call print_status,Starting $(SERVICE_NAME) service)
	@sudo systemctl start $(SERVICE_NAME)
	@sleep 2
	$(call check_service_status)

.PHONY: stop-service
stop-service: ## Stop the systemd service
	$(call print_status,Stopping $(SERVICE_NAME) service)
	@sudo systemctl stop $(SERVICE_NAME)
	$(call print_success,Service stopped)

.PHONY: restart-service-simple
restart-service-simple: ## Restart the systemd service
	$(call print_status,Restarting $(SERVICE_NAME) service)
	@sudo systemctl restart $(SERVICE_NAME)
	@sleep 2
	$(call check_service_status)

.PHONY: service-status
service-status: ## Check service status
	$(call print_status,Checking $(SERVICE_NAME) service status)
	$(call check_service_status)

.PHONY: logs
logs: ## Show service logs (follow)
	$(call print_status,Following $(SERVICE_NAME) logs)
	@journalctl -u $(SERVICE_NAME) -f --no-pager 2>/dev/null || \
	{ echo "Note: Trying with sudo (password required)"; sudo journalctl -u $(SERVICE_NAME) -f --no-pager; }

.PHONY: logs-tail
logs-tail: ## Show recent service logs
	$(call print_status,Recent $(SERVICE_NAME) logs)
	@journalctl -u $(SERVICE_NAME) -n 50 --no-pager 2>/dev/null || \
	{ echo "Note: Trying with sudo (password required)"; sudo journalctl -u $(SERVICE_NAME) -n 50 --no-pager; }

# ===========================================
# 📦 Publishing & Release
# ===========================================
.PHONY: build
build: ## Build the project
	$(call check_prerequisites)
	$(call print_status,Building project)
	@$(UV) build
	$(call print_success,Build completed)

.PHONY: publish-test
publish-test: ## Publish to Test PyPI
	$(call check_prerequisites)
	$(call print_status,Publishing to Test PyPI)
	@if [ -n "$$PYPI_TOKEN" ]; then \
		$(UV) publish --repository testpypi --token "$$PYPI_TOKEN"; \
	else \
		$(UV) publish --repository testpypi; \
	fi
	$(call print_success,Published to Test PyPI)

.PHONY: publish-pypi
publish-pypi: ## Publish to PyPI
	$(call check_prerequisites)
	$(call print_status,Publishing to PyPI)
	@if [ -n "$$PYPI_TOKEN" ]; then \
		$(UV) publish --token "$$PYPI_TOKEN"; \
	else \
		$(UV) publish; \
	fi
	$(call print_success,Published to PyPI)

.PHONY: publish-docker
publish-docker: ## Build and publish Docker images
	$(call check_prerequisites)
	$(call print_status,Building and publishing Docker images)
	@$(call print_info,Building automagik-spark-api image...)
	@docker build -f docker/Dockerfile.api -t namastexlabs/automagik-spark-api:latest -t namastexlabs/automagik-spark-api:v$(shell $(UV) run python -c "from automagik.version import __version__; print(__version__)") .
	@$(call print_info,Building automagik-spark-worker image...)
	@docker build -f docker/Dockerfile.worker -t namastexlabs/automagik-spark-worker:latest -t namastexlabs/automagik-spark-worker:v$(shell $(UV) run python -c "from automagik.version import __version__; print(__version__)") .
	@$(call print_info,Pushing automagik-spark-api images...)
	@docker push namastexlabs/automagik-spark-api:latest
	@docker push namastexlabs/automagik-spark-api:v$(shell $(UV) run python -c "from automagik.version import __version__; print(__version__)")
	@$(call print_info,Pushing automagik-spark-worker images...)
	@docker push namastexlabs/automagik-spark-worker:latest
	@docker push namastexlabs/automagik-spark-worker:v$(shell $(UV) run python -c "from automagik.version import __version__; print(__version__)")
	$(call print_success,Docker images published successfully)

.PHONY: publish
publish: build publish-pypi publish-docker ## Full publish: PyPI + Docker images
	$(call print_success_with_logo,Successfully published automagik-spark!)
	@$(call print_info,PyPI: pip install automagik-spark)
	@$(call print_info,Docker: docker pull namastexlabs/automagik-spark-api:latest)
	@$(call print_info,Docker: docker pull namastexlabs/automagik-spark-worker:latest)

.PHONY: release
release: quality test build ## Full release process (quality + test + build)
	$(call print_success_with_logo,Release build ready)
	$(call print_info,Run 'make publish-test', 'make publish-pypi', 'make publish-docker', or 'make publish' to deploy)

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

.PHONY: uninstall-service
uninstall-service: ## Uninstall systemd service
	$(call print_status,Uninstalling systemd service)
	@if [ -f "$(SERVICE_FILE)" ]; then \
		sudo systemctl stop $(SERVICE_NAME) 2>/dev/null || true; \
		sudo systemctl disable $(SERVICE_NAME) 2>/dev/null || true; \
		sudo rm -f $(SERVICE_FILE); \
		sudo systemctl daemon-reload; \
		$(call print_success,Service uninstalled); \
	else \
		$(call print_warning,Service not found); \
	fi

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