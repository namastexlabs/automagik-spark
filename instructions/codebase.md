# .aidigestignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
docker/
postgres_data/
redis_data/

# windsurf rules
.windsurfrules

# Test artifacts
.coverage
htmlcov/
.pytest_cache/
.tox/
coverage.xml
*.cover

# Documentation artifacts
docs/_build/
docs/api/
*.md
!README.md
!CONTRIBUTING.md
!docs/*.md
instructions/codebase.md 

# Include only core Python files
!automagik/core/**/*.py
!automagik/cli/**/*.py
!automagik/api/**/*.py
!tests/**/*.py

# Large files and binaries
*.pkl
*.h5
*.bin
*.model
*.tar.gz
*.zip

```

# .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
docker/
postgres_data/
redis_data/

# windsurf rules
.windsurfrules

```

# alembic.ini

```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# timezone =

# max length of characters to apply to the
# "slug" field
#truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:alembic/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or colons.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = 

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

```

# alembic/env.py

```py
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import MetaData

from alembic import context

import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from automagik.core.database.models import Base
from automagik.core.database.base import Base as SharedBase

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def combine_metadata(*args):
    """Combine multiple MetaData objects."""
    m = MetaData()
    for metadata in args:
        for t in metadata.tables.values():
            t.tometadata(m)
    return m

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = combine_metadata(Base.metadata)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = os.getenv('DATABASE_URL')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.getenv('DATABASE_URL')
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```

# alembic/README

```
Generic single-database configuration.
```

# alembic/script.py.mako

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}

```

# alembic/versions/3af7c6f910c2_add_flow_components_table.py

```py
"""add flow components table

Revision ID: 3af7c6f910c2
Revises: 
Create Date: 2025-01-07 14:20:26.770083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3af7c6f910c2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def check_constraint_exists(conn, table_name, constraint_name):
    """Check if a constraint exists in the database."""
    result = conn.execute(
        sa.text(
            """
            SELECT constraint_name FROM information_schema.table_constraints
            WHERE table_name = :table_name
            AND constraint_name = :constraint_name
            """
        ),
        {"table_name": table_name, "constraint_name": constraint_name}
    )
    return bool(result.scalar())


def check_table_exists(conn, table_name):
    """Check if a table exists in the database."""
    result = conn.execute(
        sa.text(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = :table_name
            )
            """
        ),
        {"table_name": table_name}
    )
    return bool(result.scalar())


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    
    # Drop unused tables if they exist
    if check_table_exists(conn, 'memory'):
        op.drop_table('memory')
    if check_table_exists(conn, 'agents'):
        op.drop_table('agents')
    
    # Create flows table if it doesn't exist
    if not check_table_exists(conn, 'flows'):
        op.create_table('flows',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('data', sa.JSON(), nullable=True),
            sa.Column('source', sa.String(), nullable=False),
            sa.Column('source_id', sa.String(), nullable=False),
            sa.Column('flow_version', sa.Integer(), nullable=True),
            sa.Column('is_component', sa.Boolean(), nullable=True),
            sa.Column('folder_id', sa.String(), nullable=True),
            sa.Column('folder_name', sa.String(), nullable=True),
            sa.Column('icon', sa.String(), nullable=True),
            sa.Column('icon_bg_color', sa.String(), nullable=True),
            sa.Column('gradient', sa.String(), nullable=True),
            sa.Column('liked', sa.Boolean(), nullable=True),
            sa.Column('tags', sa.JSON(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Create tasks table if it doesn't exist
    if not check_table_exists(conn, 'tasks'):
        op.create_table('tasks',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('status', sa.String(), nullable=False),
            sa.Column('input_data', sa.JSON(), nullable=True),
            sa.Column('output_data', sa.JSON(), nullable=True),
            sa.Column('tries', sa.Integer(), nullable=True),
            sa.Column('max_retries', sa.Integer(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Create logs table if it doesn't exist
    if not check_table_exists(conn, 'logs'):
        op.create_table('logs',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('task_id', sa.UUID(), nullable=False),
            sa.Column('level', sa.String(), nullable=False),
            sa.Column('message', sa.String(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Create schedules table if it doesn't exist
    if not check_table_exists(conn, 'schedules'):
        op.create_table('schedules',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('schedule_type', sa.String(), nullable=False),
            sa.Column('schedule_expr', sa.String(), nullable=False),
            sa.Column('flow_params', sa.JSON(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('next_run_at', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Now clean up existing data if tables exist
    tables_to_truncate = ['logs', 'tasks', 'schedules', 'flows']
    for table in tables_to_truncate:
        if check_table_exists(conn, table):
            conn.execute(sa.text(f'TRUNCATE TABLE {table} CASCADE'))
    
    # Create flow_components table
    op.create_table('flow_components',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('flow_id', sa.UUID(), nullable=False),
        sa.Column('component_id', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('template', sa.JSON(), nullable=True),
        sa.Column('tweakable_params', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('is_input', sa.Boolean(), nullable=True),
        sa.Column('is_output', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['flow_id'], ['flows.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add input/output component columns to flows
    op.add_column('flows', sa.Column('input_component', sa.String(), nullable=True))
    op.add_column('flows', sa.Column('output_component', sa.String(), nullable=True))
    
    # Update tasks to reference flows directly
    op.add_column('tasks', sa.Column('flow_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'flows', ['flow_id'], ['id'])
    
    # Drop agent-related constraints if they exist
    if check_constraint_exists(conn, 'tasks', 'tasks_agent_id_fkey'):
        op.drop_constraint('tasks_agent_id_fkey', 'tasks', type_='foreignkey')
    if check_constraint_exists(conn, 'schedules', 'schedules_agent_id_fkey'):
        op.drop_constraint('schedules_agent_id_fkey', 'schedules', type_='foreignkey')
    
    # Drop agent-related columns
    if 'agent_id' in [col['name'] for col in sa.inspect(conn).get_columns('tasks')]:
        op.drop_column('tasks', 'agent_id')
    if 'agent_id' in [col['name'] for col in sa.inspect(conn).get_columns('schedules')]:
        op.drop_column('schedules', 'agent_id')
    
    # Make task fields nullable for flexibility
    op.alter_column('tasks', 'input_data',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('tasks', 'output_data',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('tasks', 'tries',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('tasks', 'max_retries',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('tasks', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('tasks', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    
    # Make timestamps nullable
    op.alter_column('schedules', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('schedules', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Drop new columns from flows
    op.drop_column('flows', 'input_component')
    op.drop_column('flows', 'output_component')
    
    # Add back old columns to flows
    op.add_column('flows', sa.Column('user_id', sa.String(), nullable=True))
    op.add_column('flows', sa.Column('folder_id', sa.String(), nullable=True))
    op.add_column('flows', sa.Column('folder_name', sa.String(), nullable=True))
    
    # Recreate agents table
    op.create_table('agents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('flow_id', sa.UUID(), nullable=False),
        sa.Column('input_component', sa.String(), nullable=False),
        sa.Column('output_component', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['flow_id'], ['flows.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Restore agent references in tasks and schedules
    op.add_column('tasks', sa.Column('agent_id', sa.UUID(), nullable=True))
    op.create_foreign_key('tasks_agent_id_fkey', 'tasks', 'agents', ['agent_id'], ['id'])
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'flow_id')
    
    op.add_column('schedules', sa.Column('agent_id', sa.UUID(), nullable=True))
    op.create_foreign_key('schedules_agent_id_fkey', 'schedules', 'agents', ['agent_id'], ['id'])
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_column('schedules', 'flow_id')
    
    # Drop flow components table
    op.drop_table('flow_components')
    
    # Recreate memory table
    op.create_table('memory',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('value', sa.TEXT(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

```

# alembic/versions/6bf8b3bc2375_add_flow_id_to_schedules.py

```py
"""add_flow_id_to_schedules

Revision ID: 6bf8b3bc2375
Revises: 3af7c6f910c2
Create Date: 2025-01-07 14:37:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6bf8b3bc2375'
down_revision: Union[str, None] = '3af7c6f910c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add flow_id column
    op.add_column('schedules', sa.Column('flow_id', sa.UUID(), nullable=True))
    
    # Add foreign key constraint
    op.create_foreign_key(
        'schedules_flow_id_fkey',
        'schedules', 'flows',
        ['flow_id'], ['id']
    )
    
    # Make flow_id not nullable after adding the constraint
    op.alter_column('schedules', 'flow_id',
               existing_type=sa.UUID(),
               nullable=False)


def downgrade() -> None:
    # Drop the foreign key constraint first
    op.drop_constraint('schedules_flow_id_fkey', 'schedules', type_='foreignkey')
    
    # Drop the column
    op.drop_column('schedules', 'flow_id')

```

# alembic/versions/14d1c29e0c79_add_flow_params_to_schedules.py

```py
"""add_flow_params_to_schedules

Revision ID: 14d1c29e0c79
Revises: 6bf8b3bc2375
Create Date: 2025-01-07 15:09:49.899856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '14d1c29e0c79'
down_revision: Union[str, None] = '6bf8b3bc2375'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def check_constraint_exists(conn, table_name, constraint_name):
    """Check if a constraint exists in the database."""
    result = conn.execute(
        sa.text(
            """
            SELECT constraint_name FROM information_schema.table_constraints
            WHERE table_name = :table_name
            AND constraint_name = :constraint_name
            """
        ),
        {"table_name": table_name, "constraint_name": constraint_name}
    )
    return bool(result.scalar())


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Check if user_id column exists before dropping
    if 'user_id' in [col['name'] for col in inspector.get_columns('flows')]:
        op.drop_column('flows', 'user_id')
    
    op.alter_column('logs', 'message',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('logs', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    
    # Check if constraint exists before dropping
    if check_constraint_exists(conn, 'logs', 'logs_task_id_fkey'):
        op.drop_constraint('logs_task_id_fkey', 'logs', type_='foreignkey')
    
    op.create_foreign_key(None, 'logs', 'tasks', ['task_id'], ['id'])
    
    # Check if flow_params column exists before adding
    if 'flow_params' not in [col['name'] for col in inspector.get_columns('schedules')]:
        op.add_column('schedules', sa.Column('flow_params', sa.JSON(), nullable=True))
    
    op.alter_column('tasks', 'flow_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'flow_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_column('schedules', 'flow_params')
    op.drop_constraint(None, 'logs', type_='foreignkey')
    op.create_foreign_key('logs_task_id_fkey', 'logs', 'tasks', ['task_id'], ['id'], ondelete='CASCADE')
    op.alter_column('logs', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('logs', 'message',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.add_column('flows', sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

```

# automagik/__init__.py

```py

```

# automagik/api/__init__.py

```py

```

# automagik/api/automagik-api.service

```service
[Unit]
Description=AutoMagik API Service
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/automagik
Environment=PYTHONPATH=/root/automagik
Environment=LANGFLOW_API_URL=http://localhost:7860
Environment=TIMEZONE=UTC
EnvironmentFile=/root/automagik/.env
ExecStart=/root/automagik/.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

```

# automagik/api/dependencies.py

```py
from fastapi import Depends
from sqlalchemy.orm import Session
import os

from core.database import get_db_session
from core.flows import FlowManager
from core.scheduler import SchedulerService

def get_flow_manager(db: Session = Depends(get_db_session)):
    """Dependency for FlowManager"""
    api_url = os.getenv('LANGFLOW_API_URL')
    api_key = os.getenv('LANGFLOW_API_KEY')
    return FlowManager(db, api_url, api_key)

def get_scheduler(db: Session = Depends(get_db_session)):
    """Dependency for SchedulerService"""
    return SchedulerService(db)

```

# automagik/api/install_api_service.sh

```sh
#!/bin/bash

# Make script executable
chmod +x "$0"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "Error: .env file not found in $PROJECT_ROOT"
    echo "Please create a .env file by copying .env.example and configuring the required environment variables:"
    echo "cp .env.example .env"
    echo "Then configure the environment variables in the .env file"
    exit 1
fi

# Check required environment variables
REQUIRED_VARS=(
    "AUTOMAGIK_API_KEY"
    "DATABASE_URL"
    "CELERY_BROKER_URL"
    "CELERY_RESULT_BACKEND"
)

for var in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "^${var}=" "$PROJECT_ROOT/.env"; then
        echo "Error: ${var} not found in .env file"
        echo "Please configure ${var} in your .env file"
        exit 1
    fi
done

# Install dependencies
echo "Installing dependencies..."
python3 -m venv "$PROJECT_ROOT/.venv"
source "$PROJECT_ROOT/.venv/bin/activate"
pip install -e "$PROJECT_ROOT"

# Copy service file
echo "Installing service file..."
cp "$SCRIPT_DIR/automagik-api.service" /etc/systemd/system/

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

# Enable and start service
echo "Enabling and starting service..."
systemctl enable automagik-api
systemctl restart automagik-api

echo "Installation complete."
echo "Check service status with: systemctl status automagik-api"
echo "Check logs with: journalctl -u automagik-api"

```

# automagik/api/main.py

```py
"""
API Module for AutoMagik
"""

from fastapi import FastAPI, HTTPException, Depends, Query, Security, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List, Optional
import logging
import sys
import traceback
import uvicorn
from sqlalchemy import text
from uuid import UUID

from automagik.core.database.session import get_db_session
from automagik.core.database.models import FlowDB, Schedule, Task, Log
from automagik.core.services.flow_manager import FlowManager
from automagik.api.security import get_api_key
from automagik.core.services.langflow_client import LangflowClient
from automagik.api import schemas
from automagik.core.scheduler import SchedulerService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AutoMagik API",
    description="API for managing LangFlow workflows and schedules",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for all unhandled exceptions"""
    error_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    error_detail = {
        'error_id': error_id,
        'type': exc.__class__.__name__,
        'detail': str(exc)
    }
    
    # Log the full error with stack trace
    logger.error(f"Error ID: {error_id}")
    logger.error(f"Request: {request.method} {request.url}")
    logger.error("Exception occurred:", exc_info=True)
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_detail
        )
    elif isinstance(exc, SQLAlchemyError):
        logger.error("Database error:", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                **error_detail,
                'detail': 'Database error occurred. Please try again later.'
            }
        )
    
    return JSONResponse(
        status_code=500,
        content=error_detail
    )

# Health check endpoint
@app.get("/health")
def health_check():
    """Check service health including database connection."""
    try:
        # Test database connection
        with get_db_session() as db:
            # Try a simple query
            db.execute(text("SELECT 1"))
            
        # Test Redis connection if used
        # redis_client.ping()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("Health check failed:", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

# Flow endpoints
@app.get("/flows", response_model=schemas.FlowList)
async def list_flows(
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List all flows"""
    try:
        logger.info("Fetching all flows")
        flows = db.query(FlowDB).all()
        flow_responses = [schemas.FlowResponse.from_db(flow) for flow in flows]
        logger.info(f"Successfully fetched {len(flow_responses)} flows")
        return {"flows": flow_responses}
        
    except SQLAlchemyError as e:
        logger.error("Database error while fetching flows:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching flows"
        )
    except Exception as e:
        logger.error("Unexpected error while fetching flows:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/flows/{flow_id}", response_model=schemas.FlowResponse)
async def get_flow(
    flow_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get flow details"""
    try:
        logger.info(f"Fetching flow {flow_id}")
        try:
            flow_uuid = UUID(flow_id)
        except ValueError:
            logger.error(f"Invalid UUID format for flow_id: {flow_id}")
            raise HTTPException(status_code=422, detail="Invalid UUID format")
            
        flow = db.query(FlowDB).filter(FlowDB.id == flow_uuid).first()
        if not flow:
            logger.error(f"Flow {flow_id} not found")
            raise HTTPException(status_code=404, detail="Flow not found")
        
        logger.info(f"Successfully fetched flow {flow_id}")
        return schemas.FlowResponse.from_db(flow)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching flow {flow_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching flow"
        )
    except Exception as e:
        logger.error(f"Unexpected error while fetching flow {flow_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

# Schedule endpoints
@app.get("/schedules", response_model=schemas.ScheduleList)
async def list_schedules(
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List all schedules"""
    try:
        logger.info("Fetching all schedules")
        schedules = db.query(Schedule).all()
        schedule_responses = [schemas.ScheduleResponse.from_db(schedule) for schedule in schedules]
        logger.info(f"Successfully fetched {len(schedule_responses)} schedules")
        return {"schedules": schedule_responses}
        
    except SQLAlchemyError as e:
        logger.error("Database error while fetching schedules:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching schedules"
        )
    except Exception as e:
        logger.error("Unexpected error while fetching schedules:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/schedules/{schedule_id}", response_model=schemas.ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get schedule details"""
    try:
        logger.info(f"Fetching schedule {schedule_id}")
        try:
            schedule_uuid = UUID(schedule_id)
        except ValueError:
            logger.error(f"Invalid UUID format for schedule_id: {schedule_id}")
            raise HTTPException(status_code=422, detail="Invalid UUID format")
            
        schedule = db.query(Schedule).filter(Schedule.id == schedule_uuid).first()
        if not schedule:
            logger.error(f"Schedule {schedule_id} not found")
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        logger.info(f"Successfully fetched schedule {schedule_id}")
        return schemas.ScheduleResponse.from_db(schedule)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching schedule {schedule_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching schedule"
        )
    except Exception as e:
        logger.error(f"Unexpected error while fetching schedule {schedule_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

# Task endpoints
@app.get("/tasks", response_model=schemas.TaskList)
async def list_tasks(
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """List all tasks"""
    try:
        logger.info("Fetching all tasks")
        tasks = db.query(Task).all()
        task_responses = [schemas.TaskResponse.from_db(task) for task in tasks]
        logger.info(f"Successfully fetched {len(task_responses)} tasks")
        return {"tasks": task_responses}
        
    except SQLAlchemyError as e:
        logger.error("Database error while fetching tasks:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching tasks"
        )
    except Exception as e:
        logger.error("Unexpected error while fetching tasks:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task(
    task_id: str,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db_session)
):
    """Get task details"""
    try:
        logger.info(f"Fetching task {task_id}")
        try:
            task_uuid = UUID(task_id)
        except ValueError:
            logger.error(f"Invalid UUID format for task_id: {task_id}")
            raise HTTPException(status_code=422, detail="Invalid UUID format")
            
        task = db.query(Task).filter(Task.id == task_uuid).first()
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail="Task not found")
        
        logger.info(f"Successfully fetched task {task_id}")
        return schemas.TaskResponse.from_db(task)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching task {task_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching task"
        )
    except Exception as e:
        logger.error(f"Unexpected error while fetching task {task_id}:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

```

# automagik/api/schemas.py

```py
from pydantic import BaseModel, Field, UUID4, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class HealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    status: str = Field(..., description="Current health status of the API")
    timestamp: datetime = Field(..., description="Current server timestamp")

class FlowBase(BaseModel):
    name: str
    description: Optional[str] = None
    folder_name: Optional[str] = None
    source: str = "local"
    source_id: Optional[str] = None
    flow_version: Optional[int] = 1
    input_component: Optional[str] = None
    output_component: Optional[str] = None
    data: Dict[str, Any]

class FlowCreate(FlowBase):
    pass

class Flow(FlowBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime

class FlowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(..., description="Unique identifier of the flow")
    name: str = Field(..., description="Name of the flow")
    description: Optional[str] = Field(None, description="Description of the flow")
    source: str = Field(..., description="Source of the flow (e.g., langflow)")
    source_id: str = Field(..., description="ID of the flow in the source system")
    data: Dict[str, Any] = Field(..., description="Flow configuration data")
    created_at: datetime = Field(..., description="Flow creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Flow last update timestamp")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the flow")

    @classmethod
    def from_db(cls, flow):
        return cls(
            id=str(flow.id),
            name=flow.name,
            description=flow.description,
            source=flow.source,
            source_id=str(flow.source_id) if flow.source_id else None,
            data=flow.data,
            created_at=flow.created_at,
            updated_at=flow.updated_at,
            tags=flow.tags or []
        )

class FlowList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    flows: List[FlowResponse]

class ScheduleBase(BaseModel):
    flow_id: UUID
    schedule_type: str = Field(..., description="Type of schedule (e.g., cron, interval)")
    schedule_expr: str = Field(..., description="Schedule expression (e.g., cron expression or interval)")
    flow_params: Dict[str, Any] = Field(default_factory=dict, description="Parameters to pass to the flow")
    status: str = Field(..., description="Schedule status (e.g., active, paused)")
    next_run_at: Optional[datetime] = Field(None, description="Next scheduled run time")

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None

    @classmethod
    def from_db(cls, db_schedule):
        """Convert database model to API model."""
        return cls(
            id=db_schedule.id,
            flow_id=db_schedule.flow_id,
            schedule_type=db_schedule.schedule_type,
            schedule_expr=db_schedule.schedule_expr,
            flow_params=db_schedule.flow_params,
            status=db_schedule.status,
            next_run_at=db_schedule.next_run_at,
            created_at=db_schedule.created_at,
            updated_at=db_schedule.updated_at
        )

class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    flow_id: str
    schedule_type: str
    schedule_expr: str
    flow_params: Optional[Dict[str, Any]] = None
    status: str
    next_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_db(cls, schedule):
        return cls(
            id=str(schedule.id),
            flow_id=str(schedule.flow_id),
            schedule_type=schedule.schedule_type,
            schedule_expr=schedule.schedule_expr,
            flow_params=schedule.flow_params,
            status=schedule.status,
            next_run_at=schedule.next_run_at,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at
        )

class ScheduleList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    schedules: List[ScheduleResponse]

class TaskBase(BaseModel):
    flow_id: UUID
    schedule_id: Optional[UUID] = None
    input_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    status: str = "pending"
    tries: int = 0
    max_tries: int = 3
    retry_delay: int = 60

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    logs: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    flow_id: str
    status: str
    input_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tries: int = Field(default=0)
    max_retries: int = Field(default=3)
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_db(cls, task):
        return cls(
            id=str(task.id),
            flow_id=str(task.flow_id),
            status=task.status,
            input_data=task.input_data,
            output_data=task.output_data,
            tries=task.tries,
            max_retries=task.max_retries,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

class TaskList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    tasks: List[TaskResponse]

```

# automagik/api/security.py

```py
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
import os

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: Optional[str] = Security(api_key_header)) -> str:
    """Validate API key from header."""
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": API_KEY_NAME},
        )
    
    api_key = os.getenv("AUTOMAGIK_API_KEY")
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key is not configured",
        )
        
    if api_key_header != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": API_KEY_NAME},
        )
        
    return api_key_header

```

# automagik/cli/__init__.py

```py
from .cli import cli

__all__ = ['cli'] 

# Empty file to make the directory a Python package 
```

# automagik/cli/__main__.py

```py
from .cli import cli

if __name__ == '__main__':
    cli()

```

# automagik/cli/cli.py

```py
#!/usr/bin/env python3

import click
from dotenv import load_dotenv
import os
import sys
import logging
import subprocess
import grp

from automagik.core.logger import get_logger
from automagik.cli.commands.run import run
from automagik.cli.commands.flows import flows
from automagik.cli.commands.tasks import tasks
from automagik.cli.commands.schedules import schedules
from automagik.cli.commands.db import db

# Add parent directory to Python path to find shared package
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

def set_log_level(ctx, param, value):
    if value:
        logger = get_logger(level=value.upper())
        logger.debug(f"Log level set to {value.upper()}")
    return value

# CLI Commands
@click.group()
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warning', 'error'], case_sensitive=False), 
              callback=set_log_level, help='Set the logging level')
def cli(log_level):
    """AutoMagik CLI - Unified command-line interface for AutoMagik"""
    pass

# Register commands
cli.add_command(run)
cli.add_command(flows)
cli.add_command(tasks)
cli.add_command(schedules)
cli.add_command(db)

@cli.command()
def install_service():
    """Install AutoMagik as a system service"""
    try:
        # Get current user
        user = os.getenv('USER')
        if not user:
            click.echo("Error: Could not determine current user", err=True)
            return

        # Get user's primary group
        gid = os.getgid()
        group = grp.getgrgid(gid).gr_name

        # Get virtual environment path
        venv_path = os.path.dirname(os.path.dirname(sys.executable))
        if not os.path.exists(os.path.join(venv_path, 'bin', 'python')):
            click.echo("Error: Not running in a valid virtual environment", err=True)
            return

        # Get template path
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'service.template')
        if not os.path.exists(template_path):
            click.echo("Error: Service template not found", err=True)
            return

        # Read template
        with open(template_path, 'r') as f:
            service_content = f.read()

        # Get project root directory (where .env is located)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_file = os.path.join(project_root, '.env')

        # Replace placeholders
        service_content = service_content.format(
            user=user,
            group=group,
            working_dir=project_root,
            venv_path=venv_path,
            env_file=env_file
        )

        # Write to temporary file
        temp_service_path = '/tmp/automagik.service'
        with open(temp_service_path, 'w') as f:
            f.write(service_content)

        # Copy to systemd directory
        systemd_path = '/etc/systemd/system/automagik.service'
        if os.path.exists(systemd_path):
            click.echo("Service file already exists. Updating...", err=True)
        
        # Use sudo to copy file
        result = subprocess.run(['sudo', 'cp', temp_service_path, systemd_path], capture_output=True, text=True)
        if result.returncode != 0:
            click.echo(f"Error installing service: {result.stderr}", err=True)
            return

        # Set permissions
        subprocess.run(['sudo', 'chmod', '644', systemd_path], capture_output=True, text=True)

        # Reload systemd
        result = subprocess.run(['sudo', 'systemctl', 'daemon-reload'], capture_output=True, text=True)
        if result.returncode != 0:
            click.echo(f"Error reloading systemd: {result.stderr}", err=True)
            return

        # Enable and start service
        result = subprocess.run(['sudo', 'systemctl', 'enable', 'automagik'], capture_output=True, text=True)
        if result.returncode != 0:
            click.echo(f"Error enabling service: {result.stderr}", err=True)
            return

        result = subprocess.run(['sudo', 'systemctl', 'start', 'automagik'], capture_output=True, text=True)
        if result.returncode != 0:
            click.echo(f"Error starting service: {result.stderr}", err=True)
            return

        click.echo("AutoMagik service installed and started successfully!")

    except Exception as e:
        click.echo(f"Error installing service: {str(e)}", err=True)
        return

if __name__ == '__main__':
    cli()
```

# automagik/cli/commands/__init__.py

```py
# Empty file to make the directory a Python package 
```

# automagik/cli/commands/agents.py

```py
import click

@click.group()
def agents():
    """Manage agents"""
    pass 
```

# automagik/cli/commands/db.py

```py
import click
from alembic.config import Config
from alembic import command
import os
import sys

@click.group()
def db():
    """Database management commands"""
    pass

@db.command()
def init():
    """Initialize the database with all tables"""
    try:
        # Get the absolute path to alembic.ini in root directory
        alembic_ini = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'alembic.ini')
        
        if not os.path.exists(alembic_ini):
            click.echo(f"Error: Could not find alembic.ini at {alembic_ini}")
            sys.exit(1)
            
        # Create Alembic configuration
        alembic_cfg = Config(alembic_ini)
        
        # Run all migrations
        command.upgrade(alembic_cfg, "head")
        
        click.echo("Database initialized successfully!")
    except Exception as e:
        click.echo(f"Error initializing database: {str(e)}")
        sys.exit(1)

```

# automagik/cli/commands/flows.py

```py
import click
import json
from tabulate import tabulate
from dotenv import load_dotenv
import os

from automagik.core.services.flow_manager import FlowManager
from automagik.core.database.session import get_db_session
from automagik.core.database.models import FlowDB

@click.group()
def flows():
    """Manage flows"""
    pass

@flows.command()
def sync():
    """Sync flows from Langflow server"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get environment variables
        api_url = os.getenv('LANGFLOW_API_URL')
        api_key = os.getenv('LANGFLOW_API_KEY')
        
        click.echo("\nEnvironment Configuration:")
        click.echo(f"LANGFLOW_API_URL: {api_url}")
        if api_key:
            click.echo(f"LANGFLOW_API_KEY: {api_key[:8]}... (truncated)")
        else:
            click.echo("LANGFLOW_API_KEY: Not set")
        
        if not api_url or not api_key:
            click.echo("\nError: LANGFLOW_API_URL and LANGFLOW_API_KEY must be set", err=True)
            click.echo("Please check your .env file or environment variables")
            return
        
        # Initialize flow manager
        db_session = get_db_session()
        flow_manager = FlowManager(db_session, api_url, api_key)
        
        # Get remote flows
        click.echo("\nFetching flows from Langflow server...")
        remote_flows = flow_manager.get_available_flows()
        
        if not remote_flows:
            click.echo("\nNo flows found on the server or error occurred")
            return
            
        # Display available flows
        click.echo("\nAvailable flows:")
        for i, flow in enumerate(remote_flows):
            click.echo(f"{i}: {flow['name']} (ID: {flow['id']})")
        
        # Get user selection
        while True:
            try:
                selection = click.prompt("\nSelect a flow by index", type=int)
                if 0 <= selection < len(remote_flows):
                    selected_flow = remote_flows[selection]
                    break
                else:
                    click.echo("Please select a valid index.")
            except ValueError:
                click.echo("Please enter a valid number.")
        
        # Get detailed flow information
        click.echo(f"\nFetching details for flow {selected_flow['name']}...")
        flow_details = flow_manager.get_flow_details(selected_flow['id'])
        
        if not flow_details:
            click.echo("Could not get flow details")
            return
            
        # Sync the flow to the database
        flow_id = flow_manager.sync_flow(flow_details)
        if not flow_id:
            click.echo("Failed to sync flow")
            return
            
        click.echo("\nFlow synced successfully!")
        click.echo(f"Flow ID: {flow_id}")
        click.echo(f"Name: {flow_details.get('name', 'Unnamed')}")
        
        # Analyze components
        components = flow_manager.analyze_flow_components(flow_details)
        if components:
            click.echo("\nFlow Components:")
            for comp in components:
                role = []
                if comp['is_input']:
                    role.append("Input")
                if comp['is_output']:
                    role.append("Output")
                role_str = " & ".join(role) if role else "Processing"
                
                click.echo(f"- {comp['name']} ({role_str})")
                if comp['tweakable_params']:
                    click.echo(f"  Tweakable parameters: {', '.join(comp['tweakable_params'])}")
    
    except Exception as e:
        click.echo(f"\nError during sync: {str(e)}", err=True)

@flows.command()
def list():
    """List all flows"""
    try:
        db_session = get_db_session()
        flow_manager = FlowManager(db_session)
        
        flows = db_session.query(FlowDB).all()
        
        if not flows:
            click.echo("No flows found")
            return
            
        rows = []
        for flow in flows:
            rows.append([
                str(flow.id),
                flow.name,
                flow.folder_name or '',
                'Yes' if flow.input_component else 'No',
                'Yes' if flow.output_component else 'No',
                flow.flow_version
            ])
            
        headers = ['ID', 'Name', 'Folder', 'Has Input', 'Has Output', 'Version']
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.echo(f"Error listing flows: {str(e)}", err=True)

```

# automagik/cli/commands/run.py

```py
import click
import os
import sys
import json
from typing import Dict, Any
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from automagik.core.services.task_runner import TaskRunner
from automagik.core.scheduler.scheduler import SchedulerService
from automagik.core.database.session import get_db_session
from automagik.core.services.langflow_client import LangflowClient
from automagik.core.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger()

@click.group()
def run():
    """Run tasks and schedules"""
    pass

@run.command()
@click.option('--daemon', is_flag=True, help='Run in daemon mode')
@click.option('--log-level', default='INFO', help='Set logging level (DEBUG, INFO, WARNING, ERROR)')
def start(daemon, log_level):
    """Start the task and schedule processor"""
    # Set up logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('automagik')
    
    # Log startup information
    logger.info("Starting AutoMagik service")
    logger.debug(f"Working directory: {os.getcwd()}")
    logger.debug(f"Python path: {os.getenv('PYTHONPATH')}")
    logger.debug(f"Environment variables: {dict(os.environ)}")
    
    db = get_db_session()
    langflow_client = LangflowClient()
    runner = TaskRunner(db, langflow_client)
    scheduler = SchedulerService(db)
    
    if daemon:
        logger.info("Starting schedule processor...")
        logger.info("Running in daemon mode")
    
    async def process_schedules():
        while True:
            try:
                # Get due schedules
                due_schedules = scheduler.get_due_schedules()
                if due_schedules:
                    logger.info(f"Found {len(due_schedules)} due schedules")
                    
                # Process each schedule
                for schedule in due_schedules:
                    logger.info(f"Processing schedule {schedule.id} for flow {schedule.flow.name}")
                    
                    # Create task from schedule
                    task = await runner.create_task(
                        flow_id=schedule.flow_id,
                        input_data=schedule.flow_params
                    )
                    logger.debug(f"Created task {task.id}")
                    
                    # Run the task
                    await runner.run_task(task.id)
                    
                    # Update next run time
                    next_run = scheduler._calculate_next_run(
                        schedule.schedule_type,
                        schedule.schedule_expr
                    )
                    schedule.next_run_at = next_run
                    db.commit()
                    logger.info(f"Next run scheduled for: {next_run}")
                    
            except Exception as e:
                logger.error(f"Error processing schedules: {str(e)}", exc_info=True)
                
            if not daemon:
                break
                
            # Wait 1 minute before checking again
            await asyncio.sleep(60)
    
    # Run the processor
    asyncio.run(process_schedules())

@run.command()
@click.argument('schedule_id')
def test(schedule_id):
    """Test run a schedule immediately"""
    try:
        db = get_db_session()
        langflow_client = LangflowClient()
        runner = TaskRunner(db, langflow_client)
        scheduler = SchedulerService(db)
        
        # Get the schedule
        schedule = scheduler.get_schedule(schedule_id)
        if not schedule:
            logger.error(f"Schedule {schedule_id} not found")
            return
            
        logger.info(f"\nTesting schedule {schedule.id} for flow {schedule.flow.name}")
        logger.info(f"Type: {schedule.schedule_type}")
        logger.info(f"Expression: {schedule.schedule_expr}")
        if schedule.flow_params:
            logger.info(f"Input: {schedule.flow_params.get('input')}")
            
        async def run_test():
            # Create task from schedule
            task = await runner.create_task(
                flow_id=schedule.flow_id,
                input_data=schedule.flow_params
            )
            logger.info(f"\nCreated task {task.id}")
            
            # Run the task
            await runner.run_task(task.id)
            logger.info("\nTask completed")
            
        asyncio.run(run_test())
        
    except Exception as e:
        logger.error(f"Error testing schedule: {str(e)}", exc_info=True)
```

# automagik/cli/commands/schedules.py

```py
import click
from typing import Optional
from datetime import datetime
import uuid
from tabulate import tabulate
from sqlalchemy import text

from automagik.core.scheduler.scheduler import SchedulerService
from automagik.core.database.session import get_db_session
from automagik.core.scheduler.exceptions import (
    SchedulerError,
    InvalidScheduleError,
    ScheduleNotFoundError,
    FlowNotFoundError
)
from automagik.core.database.models import Schedule, FlowDB

@click.group()
def schedules():
    """Manage flow schedules"""
    pass

@schedules.command()
def create():
    """Create a new schedule for a flow"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        # Get flows with schedule count
        flows = db_session.execute(text("""
            SELECT f.*, COUNT(s.id) as schedule_count
            FROM flows f
            LEFT JOIN schedules s ON f.id = s.flow_id
            GROUP BY f.id
        """)).fetchall()
        
        if not flows:
            click.secho("No flows found", fg='red')
            return
            
        # Show available flows
        click.secho("\nAvailable flows:", bold=True)
        for i, flow in enumerate(flows):
            schedule_text = f"({flow.schedule_count} schedules)" if flow.schedule_count else "(no schedules)"
            click.echo(f"  {i}: {click.style(flow.name, fg='green')} {click.style(schedule_text, fg='blue')}")
            
        # Get flow selection
        flow_idx = click.prompt("\nSelect a flow", type=int, prompt_suffix=' → ')
        if flow_idx < 0 or flow_idx >= len(flows):
            click.secho("Invalid flow index", fg='red')
            return
            
        selected_flow = flows[flow_idx]
        
        # Show schedule types
        click.secho("\nSchedule Type:", bold=True)
        click.echo(f"  0: {click.style('Interval', fg='green')} (e.g., every 30 minutes)")
        click.echo(f"  1: {click.style('Cron', fg='green')} (e.g., every day at 8 AM)")
        
        # Get schedule type
        schedule_type_idx = click.prompt("\nSelect schedule type", type=int, prompt_suffix=' → ')
        if schedule_type_idx not in [0, 1]:
            click.secho("Invalid schedule type", fg='red')
            return
            
        schedule_type = 'interval' if schedule_type_idx == 0 else 'cron'
        
        # Get schedule expression
        if schedule_type == 'interval':
            click.secho("\nInterval Examples:", bold=True)
            click.echo("  5m  - Every 5 minutes")
            click.echo("  30m - Every 30 minutes")
            click.echo("  1h  - Every hour")
            click.echo("  4h  - Every 4 hours")
            click.echo("  1d  - Every day")
            schedule_expr = click.prompt("\nEnter interval", prompt_suffix=' → ')
        else:
            click.secho("\nCron Examples:", bold=True)
            click.echo("  */30 * * * * - Every 30 minutes")
            click.echo("  0 * * * *   - Every hour")
            click.echo("  0 8 * * *   - Every day at 8 AM")
            click.echo("  0 8 * * 1-5 - Every weekday at 8 AM")
            schedule_expr = click.prompt("\nEnter cron expression", prompt_suffix=' → ')
            
        # Get input value
        if click.confirm("\nDo you want to set an input value?", prompt_suffix=' → '):
            input_value = click.prompt("Enter input value", prompt_suffix=' → ')
            flow_params = {"input": input_value}
        else:
            flow_params = {}
            
        try:
            # Create schedule
            schedule = scheduler.create_schedule(
                flow_name=selected_flow.name,
                schedule_type=schedule_type,
                schedule_expr=schedule_expr,
                flow_params=flow_params
            )
            
            # Show success message
            click.secho("\nSchedule created successfully!", fg='green', bold=True)
            click.echo(f"\nDetails:")
            click.echo(f"  ID: {click.style(str(schedule.id), fg='blue')}")
            click.echo(f"  Flow: {click.style(selected_flow.name, fg='blue')}")
            click.echo(f"  Type: {click.style(schedule_type, fg='blue')}")
            click.echo(f"  Expression: {click.style(schedule_expr, fg='blue')}")
            click.echo(f"  Next Run: {click.style(str(schedule.next_run_at), fg='blue')}")
            if flow_params:
                click.echo(f"  Input: {click.style(str(flow_params), fg='blue')}")
                
        except InvalidScheduleError as e:
            click.secho(f"\nInvalid schedule: {str(e)}", fg='red')
        except FlowNotFoundError as e:
            click.secho(f"\nFlow not found: {str(e)}", fg='red')
        except ComponentNotConfiguredError as e:
            click.secho(f"\nComponent not configured: {str(e)}", fg='red')
        except SchedulerError as e:
            click.secho(f"\nScheduler error: {str(e)}", fg='red')
            
    except Exception as e:
        click.secho(f"\nError creating schedule: {str(e)}", fg='red')

@schedules.command()
@click.argument('schedule_id')
def delete(schedule_id: str):
    """Delete a schedule"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        try:
            schedule_uuid = uuid.UUID(schedule_id)
        except ValueError:
            click.secho("Invalid schedule ID format", fg='red')
            return
            
        if scheduler.delete_schedule(schedule_uuid):
            click.secho("Schedule deleted successfully", fg='green')
        else:
            click.secho("Schedule not found", fg='red')
            
    except Exception as e:
        click.secho(f"Error deleting schedule: {str(e)}", fg='red')

@schedules.command()
@click.option('--flow', help='Filter schedules by flow name')
@click.option('--status', help='Filter schedules by status (active/paused)')
def list(flow: Optional[str] = None, status: Optional[str] = None):
    """List all schedules"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        schedules = scheduler.list_schedules(flow_name=flow, status=status)
        
        if not schedules:
            click.echo("No schedules found")
            return
            
        rows = []
        for schedule in schedules:
            next_run = schedule.next_run_at.strftime('%Y-%m-%d %H:%M:%S') if schedule.next_run_at else 'N/A'
            rows.append([
                str(schedule.id),
                schedule.flow.name,
                schedule.schedule_type,
                schedule.schedule_expr,
                schedule.status,
                next_run
            ])
            
        headers = ['ID', 'Flow', 'Type', 'Expression', 'Status', 'Next Run']
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.secho(f"Error listing schedules: {str(e)}", fg='red')

```

# automagik/cli/commands/tasks.py

```py
import click
from tabulate import tabulate
import json
import os
import pytz
import uuid
from datetime import datetime
from sqlalchemy import desc

from automagik.core.database.session import get_db_session
from automagik.core.database.models import Task, FlowDB, Log
from automagik.core.scheduler import TaskRunner
from automagik.core.scheduler.exceptions import TaskExecutionError

@click.group()
def tasks():
    """Manage tasks"""
    pass

def get_local_timezone():
    """Get configured timezone from .env or default to UTC"""
    return pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

def format_datetime(dt):
    """Format datetime in local timezone"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    local_tz = get_local_timezone()
    local_dt = dt.astimezone(local_tz)
    return local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')

@tasks.command()
@click.option('--flow', help='Filter tasks by flow name')
@click.option('--status', help='Filter tasks by status')
@click.option('--limit', type=int, default=50, help='Limit number of tasks shown')
def list(flow: str = None, status: str = None, limit: int = 50):
    """List all tasks"""
    try:
        db_session = get_db_session()
        
        # Build query
        query = db_session.query(Task).order_by(desc(Task.created_at))
        
        if flow:
            query = query.join(Task.flow).filter(FlowDB.name == flow)
        if status:
            query = query.filter(Task.status == status)
            
        tasks = query.limit(limit).all()
        
        if not tasks:
            click.echo("No tasks found")
            return
        
        rows = []
        for task in tasks:
            flow_name = task.flow.name if task.flow else "N/A"
            rows.append([
                str(task.id),
                flow_name,
                task.status,
                task.tries,
                format_datetime(task.created_at),
                format_datetime(task.updated_at)
            ])
        
        headers = ['ID', 'Flow', 'Status', 'Tries', 'Created', 'Updated']
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.secho(f"Error listing tasks: {str(e)}", fg='red')

@tasks.command()
@click.argument('task_id')
def logs(task_id: str):
    """Show logs for a specific task"""
    try:
        db_session = get_db_session()
        
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            click.secho("Invalid task ID format", fg='red')
            return
        
        task = db_session.query(Task).filter(Task.id == task_uuid).first()
        if not task:
            click.secho(f"Task {task_id} not found", fg='red')
            return
        
        if not task.logs:
            click.echo("No logs found for this task")
            return
        
        rows = []
        for log in task.logs:
            rows.append([
                format_datetime(log.created_at),
                log.level.upper(),
                log.message
            ])
        
        headers = ['Timestamp', 'Level', 'Message']
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.secho(f"Error retrieving logs: {str(e)}", fg='red')

@tasks.command()
@click.argument('task_id')
def output(task_id: str):
    """Show output data for a specific task"""
    try:
        db_session = get_db_session()
        
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            click.secho("Invalid task ID format", fg='red')
            return
        
        task = db_session.query(Task).filter(Task.id == task_uuid).first()
        if not task:
            click.secho(f"Task {task_id} not found", fg='red')
            return
            
        click.echo("\nTask Details:")
        click.echo(f"Flow: {click.style(task.flow.name, fg='blue')}")
        click.echo(f"Status: {click.style(task.status, fg='green' if task.status == 'completed' else 'yellow')}")
        click.echo(f"Tries: {task.tries}/{task.max_retries}")
        click.echo(f"Created: {format_datetime(task.created_at)}")
        click.echo(f"Updated: {format_datetime(task.updated_at)}")
        
        if task.input_data:
            click.echo("\nInput Data:")
            click.echo(json.dumps(task.input_data, indent=2))
        
        if task.output_data:
            click.echo("\nOutput Data:")
            click.echo(json.dumps(task.output_data, indent=2))
        
        if task.logs:
            click.echo("\nTask Logs:")
            for log in task.logs:
                level_color = {
                    'debug': 'blue',
                    'info': 'green',
                    'warning': 'yellow',
                    'error': 'red'
                }.get(log.level.lower(), 'white')
                
                click.echo(
                    f"[{click.style(log.level.upper(), fg=level_color)}] "
                    f"{format_datetime(log.created_at)}: {log.message}"
                )
        
    except Exception as e:
        click.secho(f"Error retrieving task output: {str(e)}", fg='red')
```

# automagik/cli/commands/test_setup.py

```py
import uuid
import click
from sqlalchemy.orm import Session
from core.database.models import Task, FlowDB
from core.database import get_db_session

@click.command()
def setup_test_tasks():
    """Create test tasks for development"""
    session = get_db_session()
    
    # Create a test flow
    flow = FlowDB(
        id=uuid.uuid4(),
        name="Test Flow",
        description="A test flow for development",
        source="local",
        source_id="test",
        input_component="input-123",
        output_component="output-456",
        data={"nodes": [], "edges": []}
    )
    session.add(flow)
    session.commit()
    
    # Create test tasks
    for i in range(3):
        task = Task(
            flow_id=flow.id,
            input_data={"test": f"input {i}"},
            status="pending"
        )
        session.add(task)
    
    session.commit()
    click.echo("Created test flow and tasks")
```

# automagik/cli/db.py

```py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from .services.models import Base

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Get a new database session."""
    init_db()  # Ensure tables exist
    return SessionLocal()
```

# automagik/cli/flow_sync.py

```py
import os
import httpx
import click
import uuid
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from automagik.core.database.models import FlowDB, FlowComponent

# Load environment variables
load_dotenv()

def analyze_component(node: Dict[str, Any]) -> Tuple[bool, bool, List[str]]:
    """Analyze a component node to determine if it's input/output and its tweakable params."""
    is_input = False
    is_output = False
    tweakable_params = []
    
    # Check if it's an input/output component
    component_type = node.get("data", {}).get("node", {}).get("template", {}).get("_type", "").lower()
    if "chatinput" in component_type or "chatmessages" in component_type:
        is_input = True
    elif "chatoutput" in component_type or "chatmessagehistory" in component_type:
        is_output = True
    
    # Identify tweakable parameters
    template = node.get("data", {}).get("node", {}).get("template", {})
    for param_name, param_data in template.items():
        # Skip internal parameters and code/password fields
        if (not param_name.startswith("_") and 
            not param_data.get("code") and 
            not param_data.get("password") and
            param_data.get("show", True)):
            tweakable_params.append(param_name)
    
    return is_input, is_output, tweakable_params

def get_remote_flows(langflow_api_url: str, langflow_api_key: str) -> List[Dict[str, Any]]:
    """Fetch flows from Langflow server."""
    if not langflow_api_url or not langflow_api_key:
        click.echo("Error: API URL and API key are required")
        return []
        
    headers = {
        "x-api-key": langflow_api_key,
        "accept": "application/json"
    }
    
    params = {
        "remove_example_flows": "false",
        "components_only": "false",
        "get_all": "true",
        "header_flows": "false",
        "page": "1",
        "size": "50"
    }
    
    # Ensure URL has v1 prefix
    api_url = langflow_api_url.rstrip('/')
    if not api_url.endswith('/api/v1'):
        api_url = f"{api_url}/api/v1"
    
    click.echo(f"Connecting to Langflow server at: {api_url}")
    
    try:
        with httpx.Client(verify=False) as client:
            url = f"{api_url}/flows/"
            response = client.get(url, headers=headers, params=params)
            
            if response.status_code == 401:
                click.echo("Error: Invalid API key or unauthorized access")
                return []
            elif response.status_code == 404:
                click.echo("Error: API endpoint not found. Please check the API URL")
                return []
                
            response.raise_for_status()
            data = response.json()
            
            if not data:
                click.echo("No flows found on the server")
                return []
                
            return data
            
    except httpx.HTTPError as e:
        click.echo(f"HTTP Error: {str(e)}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response: {e.response.text}")
        return []
    except Exception as e:
        click.echo(f"Error fetching flows: {str(e)}")
        click.echo(f"Error type: {type(e)}")
        return []

def get_flow_details(langflow_api_url: str, langflow_api_key: str, flow_id: str) -> Dict[str, Any]:
    """Fetch detailed information about a specific flow."""
    headers = {
        "x-api-key": langflow_api_key,
        "accept": "application/json"
    }
    
    # Ensure URL has v1 prefix
    api_url = langflow_api_url.rstrip('/')
    if not api_url.endswith('/api/v1'):
        api_url = f"{api_url}/api/v1"
    
    try:
        with httpx.Client(verify=False) as client:
            url = f"{api_url}/flows/{flow_id}"
            click.echo(f"Making request to: {url}")
            click.echo(f"With headers: {headers}")
            
            response = client.get(url, headers=headers)
            click.echo(f"Response status code: {response.status_code}")
            click.echo(f"Response text: {response.text[:200]}...")  # Show first 200 chars
            
            response.raise_for_status()
            return response.json()
    except Exception as e:
        click.echo(f"Error fetching flow details: {str(e)}")
        click.echo(f"Error type: {type(e)}")
        if isinstance(e, httpx.HTTPError):
            click.echo(f"HTTP Status code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            click.echo(f"Response text: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        return {}

def get_folder_name(langflow_api_url: str, langflow_api_key: str, folder_id: str) -> Optional[str]:
    """Fetch folder name from the API."""
    if not folder_id:
        return None
        
    api_url = langflow_api_url.rstrip('/')
    if not api_url.endswith('/api/v1'):
        api_url = f"{api_url}/api/v1"
        
    url = f"{api_url}/folders/{folder_id}"
    headers = {
        "x-api-key": langflow_api_key,
        "accept": "application/json"
    }
    
    click.echo(f"\nFetching folder name for ID: {folder_id}")
    click.echo(f"Making request to: {url}")
    
    try:
        with httpx.Client(verify=False) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            folder_data = response.json()
            click.echo(f"Folder API response: {folder_data}")
            return folder_data.get('name')
    except Exception as e:
        click.echo(f"Error fetching folder name: {str(e)}")
    return None

def select_components(flow_data: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """Let user select input and output components."""
    nodes = flow_data.get("data", {}).get("nodes", [])
    if not nodes:
        return None, None
        
    click.echo("\nAvailable components:")
    for i, node in enumerate(nodes):
        node_id = node.get("id", "")
        node_type = node.get("data", {}).get("node", {}).get("template", {}).get("type", "unknown")
        node_name = node.get("data", {}).get("node", {}).get("template", {}).get("display_name", node_id)
        click.echo(f"{i}: {node_name} (ID: {node_id}, Type: {node_type})")
    
    input_component = None
    output_component = None
    
    # Select input component
    while True:
        try:
            selection = click.prompt("\nSelect input component by index (or -1 to skip)", type=int)
            if selection == -1:
                break
            if 0 <= selection < len(nodes):
                input_component = nodes[selection]["id"]
                break
            click.echo("Please select a valid index.")
        except ValueError:
            click.echo("Please enter a valid number.")
    
    # Select output component
    while True:
        try:
            selection = click.prompt("\nSelect output component by index (or -1 to skip)", type=int)
            if selection == -1:
                break
            if 0 <= selection < len(nodes):
                output_component = nodes[selection]["id"]
                break
            click.echo("Please select a valid index.")
        except ValueError:
            click.echo("Please enter a valid number.")
    
    return input_component, output_component

def sync_flow(db_session: Session, flow_data: Dict[str, Any], langflow_api_url: str = None, langflow_api_key: str = None) -> FlowDB:
    """Sync a flow to the local database and analyze its components."""
    source = "langflow"
    source_id = str(flow_data["id"])
    
    # Try to get folder name if we have API access
    folder_name = None
    if langflow_api_url and langflow_api_key and flow_data.get('folder_id'):
        folder_name = get_folder_name(langflow_api_url, langflow_api_key, flow_data['folder_id'])
        click.echo(f"\nFolder name from API: {folder_name}")
    
    # Let user select input/output components
    input_component, output_component = select_components(flow_data)
    
    flow_dict = {
        "id": source_id,
        "name": flow_data["name"],
        "description": flow_data.get("description", ""),
        "data": flow_data.get("data", {}),
        "source": source,
        "source_id": source_id,
        "folder_id": flow_data.get("folder_id"),
        "folder_name": folder_name,
        "is_component": flow_data.get("is_component", False),
        "icon": flow_data.get("icon"),
        "icon_bg_color": flow_data.get("icon_bg_color"),
        "gradient": flow_data.get("gradient"),
        "liked": flow_data.get("liked", False),
        "tags": flow_data.get("tags", []),
        "input_component": input_component,
        "output_component": output_component
    }
    
    # Check if flow already exists
    existing = db_session.query(FlowDB).filter_by(
        source=source,
        source_id=source_id
    ).first()
    
    if existing:
        # Update existing flow
        for key, value in flow_dict.items():
            setattr(existing, key, value)
        flow = existing
        flow.flow_version += 1
    else:
        # Create new flow
        flow = FlowDB(**flow_dict)
        flow.flow_version = 1
        db_session.add(flow)
    
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    
    return flow
```

# automagik/cli/langflow.py

```py
 
```

# automagik/cli/logger.py

```py
import logging
import click
from datetime import datetime
import pytz

class ColoredFormatter(logging.Formatter):
    """Custom formatter adding colors and timestamps to log messages"""
    
    COLORS = {
        'DEBUG': lambda x: click.style(x, fg='blue'),
        'INFO': lambda x: click.style(x, fg='green'),
        'WARNING': lambda x: click.style(x, fg='yellow'),
        'ERROR': lambda x: click.style(x, fg='red'),
        'CRITICAL': lambda x: click.style(x, fg='red', bold=True),
    }

    def format(self, record):
        # Add timezone info
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz)
        
        # Format the message
        level_color = self.COLORS.get(record.levelname, lambda x: x)
        record.levelname = level_color(f"[{record.levelname}]")
        record.msg = f"{now.strftime('%Y-%m-%d %H:%M:%S %Z')} {record.msg}"
        
        return super().format(record)

def setup_logger(name='automagik', level=logging.INFO):
    """Setup and return a logger with colored output"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler with colored formatter
    ch = logging.StreamHandler()
    ch.setLevel(level)
    
    formatter = ColoredFormatter('%(levelname)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger

```

# automagik/cli/requirements.txt

```txt
click>=8.0.0
python-dotenv>=1.0.0
sqlalchemy>=1.4.0
tabulate>=0.8.0
httpx>=0.24.0
inquirer>=3.1.3
celery>=5.3.0
redis>=4.5.0
pytest>=7.0.0 
```

# automagik/cli/scheduler_service.py

```py
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from croniter import croniter
from datetime import timedelta
import pytz
import os

from automagik.core.database.models import Schedule, FlowDB, Task, Log, Base
from automagik.core.logger import setup_logger

logger = setup_logger()

class SchedulerService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.timezone = pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

    def _get_current_time(self) -> datetime:
        """Get current time in local timezone."""
        return datetime.now(self.timezone)

    def _calculate_next_run(self, schedule_type: str, schedule_expr: str, from_time=None) -> datetime:
        """Calculate the next run time based on schedule type and expression."""
        if from_time is None:
            from_time = self._get_current_time()
        else:
            # Ensure from_time has timezone
            if from_time.tzinfo is None:
                from_time = self.timezone.localize(from_time)

        if schedule_type == 'interval':
            # Parse interval expression (e.g., '30m', '1h', '1d')
            value = int(schedule_expr[:-1])
            unit = schedule_expr[-1]
            
            logger.debug(f"Calculating next run for interval schedule: {value}{unit}")
            
            if unit == 'm':
                next_run = from_time + timedelta(minutes=value)
            elif unit == 'h':
                next_run = from_time + timedelta(hours=value)
            elif unit == 'd':
                next_run = from_time + timedelta(days=value)
            else:
                raise ValueError(f"Invalid interval unit: {unit}")
            
            logger.debug(f"Next run calculated: {next_run}")
            return next_run
        elif schedule_type == 'cron':
            # Use croniter to calculate next run time
            cron = croniter(schedule_expr, from_time)
            next_time = cron.get_next(datetime)
            return self.timezone.localize(next_time)
        else:
            raise ValueError(f"Unsupported schedule type: {schedule_type}")

    def create_schedule(self, flow_name: str, schedule_type: str, schedule_expr: str, flow_params: dict = None) -> Schedule:
        """Create a new schedule for a flow."""
        # Get the flow
        flow = self.db_session.query(FlowDB).filter(FlowDB.name == flow_name).first()
        if not flow:
            raise ValueError(f"Flow with name {flow_name} not found")

        # Verify flow has input component
        if not flow.input_component:
            raise ValueError(f"Flow {flow_name} does not have an input component configured")

        # Create schedule
        next_run = self._calculate_next_run(schedule_type, schedule_expr)
        schedule = Schedule(
            flow_id=flow.id,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            flow_params=flow_params or {},
            next_run_at=next_run,
            status='active'
        )
        
        self.db_session.add(schedule)
        self.db_session.commit()
        return schedule

    def get_schedule(self, schedule_id: uuid.UUID) -> Optional[Schedule]:
        """Get a schedule by ID."""
        return self.db_session.query(Schedule).filter(Schedule.id == schedule_id).first()

    def list_schedules(self, flow_name: Optional[str] = None) -> List[Schedule]:
        """List all schedules, optionally filtered by flow name."""
        query = self.db_session.query(Schedule)
        
        if flow_name:
            query = query.join(Schedule.flow).filter(FlowDB.name == flow_name)
        
        return query.all()

    def delete_schedule(self, schedule_id: uuid.UUID) -> bool:
        """Delete a schedule."""
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            return False

        self.db_session.delete(schedule)
        self.db_session.commit()
        return True

    def get_due_schedules(self) -> List[Schedule]:
        """Get all active schedules that are due to run."""
        now = self._get_current_time()
        
        # Find active schedules that are due
        due_schedules = self.db_session.query(Schedule).filter(
            Schedule.status == 'active',
            Schedule.next_run_at <= now
        ).all()
        
        if due_schedules:
            logger.debug(f"Found {len(due_schedules)} due schedules")
            for schedule in due_schedules:
                logger.debug(f"Schedule {schedule.id} is due:")
                logger.debug(f"    Next run was: {schedule.next_run_at}")
        
        return due_schedules

    def update_schedule_next_run(self, schedule):
        """Update the next run time for a schedule"""
        now = datetime.utcnow()
        
        if schedule.schedule_type == 'cron':
            # For cron schedules, calculate next run using croniter
            cron = croniter(schedule.schedule_expr, now)
            next_run = cron.get_next(datetime)
        else:
            # For interval schedules, add the interval to now
            # TODO: Implement interval scheduling
            next_run = now
        
        schedule.last_run = now
        schedule.next_run_at = next_run
        self.db_session.commit()

    def create_task_from_schedule(self, schedule):
        """Create a task from a schedule"""
        task = Task(
            flow_id=schedule.flow_id,
            name=f"Scheduled task for {schedule.flow.name}",
            description=f"Task created from schedule {schedule.id}",
            parameters=schedule.flow_params
        )
        self.db_session.add(task)
        self.db_session.commit()
        return task

```

# automagik/cli/services/models.py

```py
from datetime import datetime
import uuid
import os
from sqlalchemy import Column, String, JSON, DateTime, Integer, ForeignKey, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from ..shared.base import Base

def get_db_session():
    """Get a database session"""
    db_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(db_dir, 'automagik.db')
    
    # Ensure database directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Create database URL with absolute path
    db_url = f'sqlite:///{os.path.abspath(db_path)}'
    
    # Create engine with echo for debugging
    engine = create_engine(db_url, echo=os.getenv('AUTOMAGIK_DEBUG') == '1')
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    return Session()

class FlowComponent(Base):
    __tablename__ = "flow_components"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    component_id = Column(String, nullable=False)  # e.g., "CustomComponent-88JDQ"
    type = Column(String, nullable=False)  # e.g., "genericNode"
    template = Column(JSON)  # Component parameters
    tweakable_params = Column(ARRAY(String))  # List of parameters that can be tweaked
    is_input = Column(Boolean, default=False)
    is_output = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    flow = relationship("FlowDB", back_populates="components")

class FlowDB(Base):
    __tablename__ = "flows"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    data = Column(JSON)
    source = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    flow_version = Column(Integer, default=1)
    input_component = Column(String)  # ID of the input component
    output_component = Column(String)  # ID of the output component
    is_component = Column(Boolean, default=False)
    folder_id = Column(String)  # ID of the folder in Langflow
    folder_name = Column(String)  # Name of the folder in Langflow
    icon = Column(String)
    icon_bg_color = Column(String)
    gradient = Column(String)
    liked = Column(Boolean, default=False)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    components = relationship("FlowComponent", back_populates="flow", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="flow", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="flow", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    status = Column(String, nullable=False, default='pending')
    input_data = Column(JSON, default={})
    output_data = Column(JSON, default={})
    tries = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    flow = relationship("FlowDB", back_populates="tasks")
    logs = relationship("Log", back_populates="task", cascade="all, delete-orphan")

class Log(Base):
    __tablename__ = "logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    task = relationship("Task", back_populates="logs")

class Schedule(Base):
    __tablename__ = "schedules"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    schedule_type = Column(String, nullable=False)  # 'interval' or 'cron'
    schedule_expr = Column(String, nullable=False)  # '30m' for interval, '0 * * * *' for cron
    flow_params = Column(JSON, default={})  # Parameters to pass to the flow
    status = Column(String, default='active')
    next_run_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    flow = relationship("FlowDB", back_populates="schedules")
```

# automagik/cli/shared/__init__.py

```py


```

# automagik/cli/shared/base.py

```py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

```

# automagik/cli/templates/automagik.service

```service
[Unit]
Description=AutoMagik Service
After=network.target postgresql.service redis.service
Wants=network-online.target

[Service]
Type=simple
User=%USER%
Group=%USER%
WorkingDirectory=%WORKDIR%
Environment=PYTHONUNBUFFERED=1
Environment=AUTOMAGIK_DEBUG=1
Environment=AUTOMAGIK_LOG_LEVEL=DEBUG
EnvironmentFile=%WORKDIR%/.env

# Start both the scheduler and Celery worker
ExecStart=/bin/bash -c '\
    %VENV_PATH%/bin/celery -A core.celery worker --loglevel=info & \
    %VENV_PATH%/bin/automagik run start --daemon'

# Ensure both processes are stopped
ExecStop=/bin/bash -c 'pkill -f "celery worker" || true'

StandardOutput=journal
StandardError=journal
SyslogIdentifier=automagik
Restart=on-failure
RestartSec=5
StartLimitInterval=60
StartLimitBurst=3

[Install]
WantedBy=multi-user.target

```

# automagik/cli/templates/service.template

```template
[Unit]
Description=AutoMagik Service
After=network.target postgresql.service redis.service

[Service]
Type=simple
User={user}
Group={group}
WorkingDirectory={working_dir}
Environment=PATH={venv_path}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONPATH={working_dir}
EnvironmentFile={env_file}
ExecStart={venv_path}/bin/uvicorn automagik.api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

```

# automagik/cli/tests/__init__.py

```py


```

# automagik/cli/tests/test_langflow.py

```py
import asyncio
import pytest
from automagik_cli.langflow_client import LangflowClient, FlowBuilder

@pytest.mark.asyncio
async def test_flow_execution():
    """Test running a flow with specific configuration."""
    client = LangflowClient()
    
    # Build flow configuration for audio to message automation
    builder = FlowBuilder()
    
    # Add components with minimal configuration (empty tweaks)
    components = [
        "CustomComponent-88JDQ",
        "CustomComponent-8IQeG",
        "CurrentDate-BKLgt",
        "CustomComponent-QYtaC",
        "ParseData-Vfknv",
        "ChatOutput-0cetX",
        "ChatInput-fiBS9"
    ]
    
    for component_id in components:
        builder.add_component(component_id, component_id.split('-')[0])
    
    # Run the flow with the configured components
    result = await client.run_flow(
        flow_name="audio_to_messages_1d",
        input_value="message",
        input_type="chat",
        output_type="chat",
        tweaks=builder.get_tweaks(),
        stream=False
    )
    
    assert result is not None
    assert "session_id" in result
    assert "outputs" in result
    
    print("\nFlow execution result:", result)

@pytest.mark.asyncio
async def test_flow_execution_with_full_config():
    """Test running a flow with full component configuration."""
    client = LangflowClient()
    
    # Build flow configuration
    builder = FlowBuilder()
    
    # Add components with their full configurations
    builder.add_component(
        "CustomComponent-88JDQ", 
        "CustomComponent",
        api_key="audio_trans",
        connection_string="postgresql://evolution_user:Duassenha2024@192.168.112.131:5432/evolution_db",
        instance_id="felipe_evo_instance",
        language="",
        server_url="http://192.168.112.131:4040",
        transcription_delay=1500
    )
    
    builder.add_component(
        "CustomComponent-8IQeG",
        "CustomComponent",
        connection_string="postgresql://evolution_user:Duassenha2024@192.168.112.131:5432/evolution_db",
        instance_id="felipe_evo_instance",
        page=1,
        page_size=100,
        sort_direction="DESC"
    )
    
    builder.add_component(
        "CurrentDate-BKLgt",
        "CurrentDate",
        interval="1 day",
        timezone="America/Sao_Paulo"
    )
    
    builder.add_component(
        "CustomComponent-QYtaC",
        "CustomComponent",
        connection_string="postgresql://evolution_user:Duassenha2024@192.168.112.131:5432/evolution_db",
        query="SELECT * FROM pg_stat_activity;"
    )
    
    builder.add_component(
        "ParseData-Vfknv",
        "ParseData",
        sep="\n",
        template="SELECT pg_terminate_backend(pid) FROM pg_stat_activity  WHERE datname = 'evolution_db'   AND state = 'idle'   AND pid <> pg_backend_pid();"
    )
    
    builder.add_component(
        "ChatOutput-0cetX",
        "ChatOutput",
        sender="Machine",
        sender_name="AI",
        should_store_message=True,
        data_template="{text}"
    )
    
    builder.add_component(
        "ChatInput-fiBS9",
        "ChatInput",
        sender="User",
        sender_name="User",
        should_store_message=False
    )
    
    # Run the flow with the configured components
    result = await client.run_flow(
        flow_name="audio_to_messages_1d",
        input_value="message",
        input_type="chat",
        output_type="chat",
        tweaks=builder.get_tweaks(),
        stream=False
    )
    
    assert result is not None
    assert "session_id" in result
    assert "outputs" in result
    
    print("\nFlow execution result with full config:", result)

if __name__ == "__main__":
    asyncio.run(test_flow_execution())
    asyncio.run(test_flow_execution_with_full_config())

```

# automagik/core/__init__.py

```py
"""
AutoMagik Core Package

This package contains the core business logic for AutoMagik, independent of any specific interface (CLI or API).
"""

__version__ = "0.1.0"

```

# automagik/core/database/__init__.py

```py
"""
Database Package

This package handles all database-related functionality including models and session management.
"""

from .session import get_db_session
from .models import Base, FlowDB, FlowComponent, Task, Log, Schedule

__all__ = [
    'get_db_session',
    'Base',
    'FlowDB',
    'FlowComponent',
    'Task',
    'Log',
    'Schedule'
]

```

# automagik/core/database/base.py

```py
"""
Database Base Module

This module defines the base class for all database models.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

```

# automagik/core/database/models.py

```py
"""
Database Models Module

This module defines all database models used in the application.
"""

from datetime import datetime
import uuid
from sqlalchemy import Column, String, JSON, DateTime, Integer, ForeignKey, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class FlowComponent(Base):
    """
    Represents a component within a flow, such as input/output nodes or processing steps.
    """
    __tablename__ = "flow_components"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    component_id = Column(String, nullable=False)  # e.g., "CustomComponent-88JDQ"
    type = Column(String, nullable=False)  # e.g., "genericNode"
    template = Column(JSON)  # Component parameters
    tweakable_params = Column(JSON)  # List of parameters that can be tweaked
    is_input = Column(Boolean, default=False)
    is_output = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flow = relationship("FlowDB", back_populates="components")


class FlowDB(Base):
    """
    Represents a flow, which is a collection of components and their connections.
    """
    __tablename__ = "flows"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    data = Column(JSON)  # Full flow data including connections
    source = Column(String, nullable=False)  # e.g., 'langflow'
    source_id = Column(String, nullable=False)  # Original ID in the source system
    flow_version = Column(Integer, default=1)
    input_component = Column(String)  # ID of the input component
    output_component = Column(String)  # ID of the output component
    is_component = Column(Boolean, default=False)
    folder_id = Column(String)  # ID of the folder in source system
    folder_name = Column(String)  # Name of the folder in source system
    icon = Column(String)
    icon_bg_color = Column(String)
    gradient = Column(String)
    liked = Column(Boolean, default=False)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    components = relationship("FlowComponent", back_populates="flow", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="flow", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="flow", cascade="all, delete-orphan")


class Task(Base):
    """
    Represents a task, which is an execution instance of a flow.
    """
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    status = Column(String, nullable=False, default='pending')  # pending, running, completed, failed
    input_data = Column(JSON, default={})
    output_data = Column(JSON, default={})
    tries = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flow = relationship("FlowDB", back_populates="tasks")
    logs = relationship("Log", back_populates="task", cascade="all, delete-orphan")


class Log(Base):
    """
    Represents a log entry associated with a task execution.
    """
    __tablename__ = "logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
    level = Column(String, nullable=False)  # debug, info, warning, error
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    task = relationship("Task", back_populates="logs")


class Schedule(Base):
    """
    Represents a schedule for automated flow execution.
    """
    __tablename__ = "schedules"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    schedule_type = Column(String, nullable=False)  # 'interval' or 'cron'
    schedule_expr = Column(String, nullable=False)  # '30m' for interval, '0 * * * *' for cron
    flow_params = Column(JSON, default={})  # Parameters to pass to the flow
    status = Column(String, default='active')  # active, paused, deleted
    next_run_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flow = relationship("FlowDB", back_populates="schedules")

```

# automagik/core/database/session.py

```py
"""
Database Session Management Module

This module handles database connection and session management.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
import logging
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add console handler if not already present
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Get database URL from environment or use default
database_url = os.getenv('DATABASE_URL')
logger.debug(f"Raw DATABASE_URL from environment: {database_url}")

if database_url and ('postgresql://' in database_url or 'postgresql+psycopg2://' in database_url):
    # Use the provided PostgreSQL URL
    db_url = database_url
    logger.info(f"Using PostgreSQL database at {database_url}")
else:
    # Default to SQLite if no PostgreSQL URL is provided
    db_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(db_dir, 'automagik.db')
    
    # Ensure database directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Create database URL with absolute path
    db_url = f'sqlite:///{os.path.abspath(db_path)}'
    logger.warning(f"No valid PostgreSQL URL found in DATABASE_URL environment variable. Falling back to SQLite at {db_path}")

# Create engine with echo for debugging
engine = create_engine(
    db_url,
    echo=os.getenv('AUTOMAGIK_DEBUG') == '1',
    pool_pre_ping=True  # Enable automatic reconnection
)

def get_db_session():
    """
    Create and return a new database session.
    
    The function will:
    1. Create the database directory if it doesn't exist
    2. Initialize the database if it's not already initialized
    3. Create and return a new session
    
    Returns:
        SQLAlchemy Session object
    """
    try:
        # Create all tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create and return new session
        return SessionLocal()
        
    except Exception as e:
        logger.error(f"Error creating database session: {str(e)}")
        raise

```

# automagik/core/flows/__init__.py

```py
"""
Flow Management Package

This package handles all flow-related operations including flow analysis,
synchronization with LangFlow, and flow management.
"""

from .flow_manager import FlowManager
from .flow_analyzer import FlowAnalyzer
from .flow_sync import FlowSync

__all__ = ['FlowManager', 'FlowAnalyzer', 'FlowSync']

```

# automagik/core/logger.py

```py
import logging
import click
from datetime import datetime
import pytz

class ColoredFormatter(logging.Formatter):
    """Custom formatter adding colors and timestamps to log messages"""
    
    COLORS = {
        'DEBUG': lambda x: click.style(x, fg='blue'),
        'INFO': lambda x: click.style(x, fg='green'),
        'WARNING': lambda x: click.style(x, fg='yellow'),
        'ERROR': lambda x: click.style(x, fg='red'),
        'CRITICAL': lambda x: click.style(x, fg='red', bold=True),
    }

    def format(self, record):
        # Add timezone info
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz)
        
        # Format the message
        level_color = self.COLORS.get(record.levelname, lambda x: x)
        record.levelname = level_color(f"[{record.levelname}]")
        record.msg = f"{now.strftime('%Y-%m-%d %H:%M:%S %Z')} {record.msg}"
        
        return super().format(record)

def setup_logger(name='automagik', level=logging.INFO):
    """Setup and return a logger with colored output"""
    if isinstance(level, str):
        level = getattr(logging, level.upper())
        
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler with colored formatter
    ch = logging.StreamHandler()
    ch.setLevel(level)
    
    formatter = ColoredFormatter('%(levelname)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger

def get_logger(name='automagik', level=logging.INFO):
    """Get or create a logger with the given name and level"""
    return setup_logger(name=name, level=level)

```

# automagik/core/scheduler/__init__.py

```py
"""
Scheduler Package

This package handles task scheduling and execution for flows.
"""

from .scheduler import SchedulerService
from .task_runner import TaskRunner
from .exceptions import SchedulerError, TaskExecutionError

__all__ = ['SchedulerService', 'TaskRunner', 'SchedulerError', 'TaskExecutionError']

```

# automagik/core/scheduler/exceptions.py

```py
"""
Scheduler Exception Classes

This module defines custom exceptions for the scheduler package.
"""

class SchedulerError(Exception):
    """Base exception for scheduler-related errors."""
    pass

class TaskExecutionError(SchedulerError):
    """Raised when there's an error executing a task."""
    def __init__(self, message: str, task_id: str = None, response: dict = None):
        super().__init__(message)
        self.task_id = task_id
        self.response = response

class InvalidScheduleError(SchedulerError):
    """Raised when a schedule configuration is invalid."""
    pass

class ComponentNotConfiguredError(SchedulerError):
    """Raised when required flow components are not configured."""
    pass

class ScheduleNotFoundError(SchedulerError):
    """Raised when a requested schedule is not found."""
    pass

class FlowNotFoundError(SchedulerError):
    """Raised when a requested flow is not found."""
    pass

```

# automagik/core/scheduler/scheduler.py

```py
"""
Scheduler Service Module

This module provides the core scheduling functionality for flow execution.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid
import pytz
import os
import logging
from croniter import croniter
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..database.models import Schedule, FlowDB, Task
from .exceptions import (
    SchedulerError,
    InvalidScheduleError,
    FlowNotFoundError,
    ComponentNotConfiguredError
)

logger = logging.getLogger(__name__)

class SchedulerService:
    """
    Service for managing flow execution schedules.
    
    This service handles:
    - Creating and managing schedules
    - Calculating next run times
    - Finding due schedules
    - Creating tasks from schedules
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize the scheduler service.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db_session = db_session
        self.timezone = pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

    def _get_current_time(self) -> datetime:
        """Get current time in configured timezone."""
        return datetime.now(self.timezone)

    def _calculate_next_run(self, schedule_type: str, schedule_expr: str, from_time: Optional[datetime] = None) -> datetime:
        """
        Calculate the next run time based on schedule type and expression.
        
        Args:
            schedule_type: Type of schedule ('interval' or 'cron')
            schedule_expr: Schedule expression (e.g., '30m' for interval, '* * * * *' for cron)
            from_time: Optional base time for calculation
            
        Returns:
            datetime: Next scheduled run time
            
        Raises:
            InvalidScheduleError: If schedule type or expression is invalid
        """
        if from_time is None:
            from_time = self._get_current_time()
        elif from_time.tzinfo is None:
            from_time = self.timezone.localize(from_time)

        try:
            if schedule_type == 'interval':
                # Parse interval expression (e.g., '30m', '1h', '1d')
                value = int(schedule_expr[:-1])
                unit = schedule_expr[-1].lower()
                
                if unit == 'm':
                    delta = timedelta(minutes=value)
                elif unit == 'h':
                    delta = timedelta(hours=value)
                elif unit == 'd':
                    delta = timedelta(days=value)
                else:
                    raise InvalidScheduleError(f"Invalid interval unit: {unit}")
                
                return from_time + delta
                
            elif schedule_type == 'cron':
                try:
                    cron = croniter(schedule_expr, from_time)
                    next_time = cron.get_next(datetime)
                    return self.timezone.localize(next_time)
                except ValueError as e:
                    raise InvalidScheduleError(f"Invalid cron expression: {str(e)}")
            else:
                raise InvalidScheduleError(f"Unsupported schedule type: {schedule_type}")
                
        except Exception as e:
            raise InvalidScheduleError(f"Error calculating next run: {str(e)}")

    def create_schedule(
        self,
        flow_name: str,
        schedule_type: str,
        schedule_expr: str,
        flow_params: Dict[str, Any] = None
    ) -> Schedule:
        """
        Create a new schedule for a flow.
        
        Args:
            flow_name: Name of the flow to schedule
            schedule_type: Type of schedule ('interval' or 'cron')
            schedule_expr: Schedule expression
            flow_params: Optional parameters to pass to the flow
            
        Returns:
            Schedule: Created schedule object
            
        Raises:
            FlowNotFoundError: If flow doesn't exist
            ComponentNotConfiguredError: If flow components aren't configured
            InvalidScheduleError: If schedule configuration is invalid
        """
        # Validate flow
        flow = self.db_session.query(FlowDB).filter(FlowDB.name == flow_name).first()
        if not flow:
            raise FlowNotFoundError(f"Flow '{flow_name}' not found")

        if not flow.input_component:
            raise ComponentNotConfiguredError(
                f"Flow '{flow_name}' does not have an input component configured"
            )

        # Calculate next run time
        try:
            next_run = self._calculate_next_run(schedule_type, schedule_expr)
        except InvalidScheduleError as e:
            raise InvalidScheduleError(f"Invalid schedule for flow '{flow_name}': {str(e)}")

        # Create schedule
        schedule = Schedule(
            flow_id=flow.id,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            flow_params=flow_params or {},
            next_run_at=next_run,
            status='active'
        )
        
        try:
            self.db_session.add(schedule)
            self.db_session.commit()
            logger.info(f"Created schedule for flow '{flow_name}', next run at {next_run}")
            return schedule
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error creating schedule: {str(e)}")

    def get_schedule(self, schedule_id: uuid.UUID) -> Optional[Schedule]:
        """Get a schedule by ID."""
        return self.db_session.query(Schedule).filter(Schedule.id == schedule_id).first()

    def list_schedules(
        self,
        flow_name: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Schedule]:
        """
        List schedules with optional filtering.
        
        Args:
            flow_name: Optional flow name to filter by
            status: Optional status to filter by
            
        Returns:
            List of matching schedules
        """
        query = self.db_session.query(Schedule)
        
        if flow_name:
            query = query.join(Schedule.flow).filter(FlowDB.name == flow_name)
        
        if status:
            query = query.filter(Schedule.status == status)
        
        return query.all()

    def update_schedule(
        self,
        schedule_id: uuid.UUID,
        status: Optional[str] = None,
        flow_params: Optional[Dict[str, Any]] = None
    ) -> Optional[Schedule]:
        """
        Update a schedule's status or parameters.
        
        Args:
            schedule_id: ID of schedule to update
            status: Optional new status
            flow_params: Optional new flow parameters
            
        Returns:
            Updated schedule or None if not found
        """
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            return None

        if status:
            schedule.status = status
        if flow_params is not None:
            schedule.flow_params = flow_params

        try:
            self.db_session.commit()
            return schedule
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error updating schedule: {str(e)}")

    def delete_schedule(self, schedule_id: uuid.UUID) -> bool:
        """
        Delete a schedule.
        
        Args:
            schedule_id: ID of schedule to delete
            
        Returns:
            True if deleted, False if not found
        """
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            return False

        try:
            self.db_session.delete(schedule)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error deleting schedule: {str(e)}")

    def get_due_schedules(self) -> List[Schedule]:
        """
        Get all active schedules that are due to run.
        
        Returns:
            List of schedules that should be executed
        """
        now = self._get_current_time()
        
        try:
            due_schedules = self.db_session.query(Schedule).filter(
                and_(
                    Schedule.status == 'active',
                    Schedule.next_run_at <= now
                )
            ).all()
            
            if due_schedules:
                logger.debug(f"Found {len(due_schedules)} due schedules")
                for schedule in due_schedules:
                    logger.debug(f"Schedule {schedule.id} due at {schedule.next_run_at}")
            
            return due_schedules
        except Exception as e:
            raise SchedulerError(f"Error fetching due schedules: {str(e)}")

    def update_schedule_next_run(self, schedule: Schedule) -> None:
        """
        Update the next run time for a schedule.
        
        Args:
            schedule: Schedule to update
        """
        try:
            next_run = self._calculate_next_run(
                schedule.schedule_type,
                schedule.schedule_expr,
                self._get_current_time()
            )
            
            schedule.next_run_at = next_run
            self.db_session.commit()
            
            logger.debug(f"Updated schedule {schedule.id} next run to {next_run}")
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error updating schedule next run: {str(e)}")

    def create_task_from_schedule(self, schedule: Schedule) -> Task:
        """
        Create a task from a schedule.
        
        Args:
            schedule: Schedule to create task from
            
        Returns:
            Created task
            
        Raises:
            SchedulerError: If task creation fails
        """
        try:
            task = Task(
                flow_id=schedule.flow_id,
                input_data=schedule.flow_params,
                status="pending"
            )
            
            self.db_session.add(task)
            self.db_session.commit()
            
            logger.info(f"Created task {task.id} from schedule {schedule.id}")
            return task
            
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error creating task from schedule: {str(e)}")

```

# automagik/core/scheduler/task_runner.py

```py
"""
Task Runner Module

This module handles the execution of flow tasks, including running flows
and managing their execution state.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
import uuid

from sqlalchemy.orm import Session
from ..database.models import Task, Log, FlowDB
from .exceptions import TaskExecutionError, FlowNotFoundError, ComponentNotConfiguredError

logger = logging.getLogger(__name__)

class TaskRunner:
    """
    Handles the execution of flow tasks.
    
    This class is responsible for:
    - Creating and managing tasks
    - Executing flows via LangFlow
    - Managing task state and logging
    - Processing flow results
    """
    
    def __init__(self, session: Session, langflow_client: Any):
        """
        Initialize TaskRunner.
        
        Args:
            session: SQLAlchemy database session
            langflow_client: Client for interacting with LangFlow API
        """
        self.session = session
        self.langflow_client = langflow_client

    async def create_task(
        self,
        flow_id: uuid.UUID,
        input_data: Dict[str, Any] = None
    ) -> Task:
        """
        Create a new task for a flow.
        
        Args:
            flow_id: ID of the flow to create task for
            input_data: Optional input data for the flow
            
        Returns:
            Created task
            
        Raises:
            FlowNotFoundError: If flow doesn't exist
        """
        flow = self.session.query(FlowDB).filter(FlowDB.id == flow_id).first()
        if not flow:
            raise FlowNotFoundError(f"Flow {flow_id} not found")
        
        try:
            task = Task(
                flow_id=flow_id,
                input_data=input_data or {},
                status="pending"
            )
            self.session.add(task)
            self.session.commit()
            
            logger.info(f"Created task {task.id} for flow {flow_id}")
            return task
            
        except Exception as e:
            self.session.rollback()
            raise TaskExecutionError(f"Error creating task: {str(e)}")

    def _extract_output_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract useful information from the LangFlow response.
        
        Args:
            response: Raw response from LangFlow API
            
        Returns:
            Processed output data
        """
        output_data = {
            "session_id": response.get("session_id"),
            "messages": [],
            "artifacts": [],
            "logs": []
        }
        
        # Extract messages and outputs
        for output in response.get("outputs", []):
            for result in output.get("outputs", []):
                # Get messages
                messages = result.get("messages", [])
                output_data["messages"].extend(messages)
                
                # Get artifacts
                if "artifacts" in result:
                    output_data["artifacts"].append(result["artifacts"])
                    
                # Get logs
                if "logs" in result:
                    for component_logs in result["logs"].values():
                        output_data["logs"].extend(component_logs)
        
        return output_data

    def _log_message(self, task_id: uuid.UUID, level: str, message: str) -> None:
        """
        Add a log message for a task.
        
        Args:
            task_id: ID of the task
            level: Log level
            message: Log message
        """
        try:
            log = Log(
                task_id=task_id,
                level=level,
                message=message
            )
            self.session.add(log)
            self.session.commit()
        except Exception as e:
            logger.error(f"Error adding log message: {str(e)}")
            self.session.rollback()

    async def run_task(self, task_id: uuid.UUID) -> Task:
        """
        Run a task.
        
        Args:
            task_id: ID of the task to run
            
        Returns:
            Updated task
            
        Raises:
            TaskExecutionError: If task execution fails
        """
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskExecutionError(f"Task {task_id} not found")

        flow = task.flow
        if not flow:
            raise FlowNotFoundError(f"Flow for task {task_id} not found")

        if not flow.input_component:
            raise ComponentNotConfiguredError(
                f"Flow {flow.id} does not have input component configured"
            )

        # Update task status
        task.status = "running"
        task.tries += 1
        self.session.commit()

        try:
            # Get flow tweaks
            tweaks = flow.data.get('tweaks', {}) if flow.data else {}
            
            # Log execution details
            logger.info(f"Running flow: {flow.name}")
            logger.info(f"Input: {task.input_data.get('input', '')}")
            logger.debug(f"Flow ID: {flow.id}")
            logger.debug(f"Input component: {flow.input_component}")
            logger.debug(f"Output component: {flow.output_component}")
            logger.debug(f"Input data: {json.dumps(task.input_data, indent=2)}")
            logger.debug(f"Tweaks: {json.dumps(tweaks, indent=2)}")
            
            # Execute flow
            result = await self.langflow_client.process_flow(
                flow_id=str(flow.id),
                input_data=task.input_data,
                tweaks=tweaks
            )
            
            # Process results
            logger.debug(f"API Response: {json.dumps(result, indent=2)}")
            output_data = self._extract_output_data(result)
            
            # Log results
            for msg in output_data["messages"]:
                text = msg.get("text", msg.get("message", ""))
                logger.info(f'Response: {text}')
            
            if output_data.get("artifacts"):
                logger.debug(f'Artifacts: {json.dumps(output_data["artifacts"], indent=2)}')
            
            # Update task
            task.status = "completed"
            task.output_data = output_data
            self.session.commit()
            
            logger.info(f"Task {task_id} completed successfully")
            return task
            
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response'):
                error_msg += f"\nResponse status: {e.response.status_code}"
                error_msg += f"\nResponse text: {e.response.text}"
            
            logger.error(error_msg)
            self._log_message(task_id, "error", error_msg)
            
            task.status = "failed"
            self.session.commit()
            
            raise TaskExecutionError(
                message=f"Task execution failed: {error_msg}",
                task_id=str(task_id),
                response=getattr(e, 'response', None)
            )

```

# automagik/core/services/flow_analyzer.py

```py
"""
Flow Analyzer Module

This module provides functionality for analyzing LangFlow components and their properties.
"""

from typing import Dict, Any, Tuple, List


class FlowAnalyzer:
    @staticmethod
    def analyze_component(node: Dict[str, Any]) -> Tuple[bool, bool, List[str]]:
        """
        Analyze a component node to determine if it's input/output and its tweakable params.
        
        Args:
            node: The node data from the flow
            
        Returns:
            Tuple containing:
            - is_input (bool): Whether the component is an input component
            - is_output (bool): Whether the component is an output component
            - tweakable_params (List[str]): List of parameters that can be modified
        """
        is_input = False
        is_output = False
        tweakable_params = []
        
        # Check if it's an input/output component
        component_type = node.get("data", {}).get("node", {}).get("template", {}).get("_type", "").lower()
        if "chatinput" in component_type or "chatmessages" in component_type:
            is_input = True
        elif "chatoutput" in component_type or "chatmessagehistory" in component_type:
            is_output = True
        
        # Identify tweakable parameters
        template = node.get("data", {}).get("node", {}).get("template", {})
        for param_name, param_data in template.items():
            # Skip internal parameters and code/password fields
            if (not param_name.startswith("_") and 
                not param_data.get("code") and 
                not param_data.get("password") and
                param_data.get("show", True)):
                tweakable_params.append(param_name)
        
        return is_input, is_output, tweakable_params

    @staticmethod
    def get_component_info(node: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant information from a component node.
        
        Args:
            node: The node data from the flow
            
        Returns:
            Dict containing component information including id, type, and name
        """
        return {
            "id": node.get("id", ""),
            "type": node.get("data", {}).get("node", {}).get("template", {}).get("type", "unknown"),
            "name": node.get("data", {}).get("node", {}).get("template", {}).get("display_name", node.get("id", ""))
        }

```

# automagik/core/services/flow_manager.py

```py
"""
Flow Manager Module

This module provides the main interface for managing flows, combining functionality
from flow_analyzer and flow_sync.
"""

from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
import uuid
import logging
import json

from automagik.core.database.models import FlowDB, FlowComponent
from .flow_analyzer import FlowAnalyzer
from .flow_sync import FlowSync

logger = logging.getLogger(__name__)

class FlowManager:
    def __init__(self, db_session: Session, langflow_api_url: str = None, langflow_api_key: str = None):
        """
        Initialize FlowManager with database session and optional API credentials.
        
        Args:
            db_session: SQLAlchemy database session
            langflow_api_url: Optional URL for LangFlow API
            langflow_api_key: Optional API key for authentication
        """
        self.db_session = db_session
        self.flow_sync = None
        if langflow_api_url and langflow_api_key:
            self.flow_sync = FlowSync(langflow_api_url, langflow_api_key)
        self.flow_analyzer = FlowAnalyzer()

    def sync_flow(self, flow_data: Dict[str, Any]) -> Optional[str]:
        """
        Sync a flow to the local database and analyze its components.
        
        Args:
            flow_data: Flow data from LangFlow
            
        Returns:
            ID of the synced flow if successful, None otherwise
        """
        try:
            # Generate a new UUID for the flow
            flow_id = str(uuid.uuid4())
            
            # Extract basic flow information
            name = flow_data.get("name", "Unnamed Flow")
            description = flow_data.get("description", "")
            folder_id = flow_data.get("folder_id")
            
            # Get folder name if available
            folder_name = None
            if self.flow_sync and folder_id:
                folder_name = self.flow_sync.get_folder_name(folder_id)
            
            # Extract and parse the data field
            data = {}
            raw_data = flow_data.get("data", {})
            if isinstance(raw_data, str):
                try:
                    data = json.loads(raw_data)
                except json.JSONDecodeError:
                    logger.error("Failed to parse flow data as JSON")
                    data = {}
            elif isinstance(raw_data, dict):
                data = raw_data
            
            # Analyze flow components
            components = []
            input_component = None
            output_component = None
            for node in data.get("nodes", []):
                is_input, is_output, tweakable_params = self.flow_analyzer.analyze_component(node)
                
                component_info = self.flow_analyzer.get_component_info(node)
                components.append({
                    "node_id": component_info["id"],
                    "name": component_info["name"],
                    "type": component_info["type"],
                    "is_input": is_input,
                    "is_output": is_output,
                    "tweakable_params": tweakable_params
                })
                
                if is_input:
                    input_component = component_info["name"]
                if is_output:
                    output_component = component_info["name"]
            
            # Store flow data in database
            flow = FlowDB(
                id=uuid.UUID(flow_id),
                name=name,
                description=description,
                data=data,
                source="langflow",
                source_id=flow_data.get("id"),
                folder_id=folder_id,
                folder_name=folder_name,
                flow_version=1,
                input_component=input_component,
                output_component=output_component
            )
            self.db_session.add(flow)
            self.db_session.commit()
            
            return flow_id
            
        except Exception as e:
            logger.error(f"Error syncing flow: {str(e)}")
            return None

    def get_available_flows(self) -> List[Dict[str, Any]]:
        """
        Get list of available flows from LangFlow server.
        
        Returns:
            List of flow dictionaries
        """
        if not self.flow_sync:
            logger.error("LangFlow API credentials not configured")
            return []
        
        return self.flow_sync.get_remote_flows()

    def get_flow_details(self, flow_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific flow.
        
        Args:
            flow_id: ID of the flow
            
        Returns:
            Flow details dictionary
        """
        if not self.flow_sync:
            logger.error("LangFlow API credentials not configured")
            return {}
        
        return self.flow_sync.get_flow_details(flow_id)

    def analyze_flow_components(self, flow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze all components in a flow.
        
        Args:
            flow_data: Flow data from LangFlow
            
        Returns:
            List of component information dictionaries
        """
        components = []
        for node in flow_data.get("data", {}).get("nodes", []):
            is_input, is_output, tweakable_params = self.flow_analyzer.analyze_component(node)
            component_info = self.flow_analyzer.get_component_info(node)
            components.append({
                "id": component_info["id"],
                "name": component_info["name"],
                "type": component_info["type"],
                "is_input": is_input,
                "is_output": is_output,
                "tweakable_params": tweakable_params
            })
        return components

```

# automagik/core/services/flow_sync.py

```py
"""
Flow Sync Module

This module handles synchronization with the LangFlow server, including fetching flows
and their details.
"""

import httpx
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FlowSync:
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize FlowSync with API credentials.
        
        Args:
            api_url: Base URL for the LangFlow API
            api_key: API key for authentication
        """
        self.api_url = self._normalize_api_url(api_url)
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key,
            "accept": "application/json"
        }

    def _normalize_api_url(self, url: str) -> str:
        """Ensure URL has the correct API version prefix."""
        url = url.rstrip('/')
        if not url.endswith('/api/v1'):
            url = f"{url}/api/v1"
        return url

    def get_remote_flows(self) -> List[Dict[str, Any]]:
        """
        Fetch flows from LangFlow server.
        
        Returns:
            List of flow dictionaries
        """
        params = {
            "remove_example_flows": "false",
            "components_only": "false",
            "get_all": "true",
            "header_flows": "false",
            "page": "1",
            "size": "50"
        }
        
        try:
            with httpx.Client(verify=False) as client:
                url = f"{self.api_url}/flows/"
                response = client.get(url, headers=self.headers, params=params)
                
                if response.status_code == 401:
                    logger.error("Invalid API key or unauthorized access")
                    return []
                elif response.status_code == 404:
                    logger.error("API endpoint not found. Please check the API URL")
                    return []
                    
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    logger.info("No flows found on the server")
                    return []
                    
                return data
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Status code: {e.response.status_code}")
                logger.error(f"Response: {e.response.text}")
            return []
        except Exception as e:
            logger.error(f"Error fetching flows: {str(e)}")
            return []

    def get_flow_details(self, flow_id: str) -> Dict[str, Any]:
        """
        Fetch detailed information about a specific flow.
        
        Args:
            flow_id: ID of the flow to fetch
            
        Returns:
            Flow details dictionary
        """
        try:
            with httpx.Client(verify=False) as client:
                url = f"{self.api_url}/flows/{flow_id}"
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching flow details: {str(e)}")
            return {}

    def get_folder_name(self, folder_id: str) -> Optional[str]:
        """
        Fetch folder name from the API.
        
        Args:
            folder_id: ID of the folder
            
        Returns:
            Folder name if found, None otherwise
        """
        if not folder_id:
            return None
            
        url = f"{self.api_url}/folders/{folder_id}"
        
        try:
            with httpx.Client(verify=False) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                folder_data = response.json()
                return folder_data.get('name')
        except Exception as e:
            logger.error(f"Error fetching folder name: {str(e)}")
            return None

```

# automagik/core/services/langflow_client.py

```py
"""
LangFlow API Client

This module provides a client for interacting with the LangFlow API.
"""

import httpx
import os
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class FlowComponent:
    """Helper class to manage flow component configurations."""
    
    def __init__(self, component_id: str, component_type: str, config: Dict[str, Any] = None):
        self.id = component_id
        self.type = component_type
        self.config = config or {}
        
    def update_config(self, **kwargs):
        """Update component configuration."""
        self.config.update(kwargs)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary format for API."""
        return {
            "id": self.id,
            "type": self.type,
            **self.config
        }

class FlowBuilder:
    """Helper class to build flow configurations."""
    
    def __init__(self):
        self.components: Dict[str, FlowComponent] = {}
        
    def add_component(self, component_id: str, component_type: str, **config):
        """Add a component to the flow."""
        self.components[component_id] = FlowComponent(component_id, component_type, config)
        
    def get_tweaks(self) -> Dict[str, Dict[str, Any]]:
        """Get the complete tweaks configuration for the flow."""
        return {
            component_id: component.to_dict()
            for component_id, component in self.components.items()
        }

class LangflowClient:
    """Client for interacting with the LangFlow API."""
    
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize LangFlow client.
        
        Args:
            api_url: LangFlow API base URL. If not provided, uses LANGFLOW_API_URL env var.
            api_key: API key for authentication. If not provided, uses LANGFLOW_API_KEY env var.
        """
        self.api_url = (api_url or os.getenv('LANGFLOW_API_URL', '')).rstrip('/')
        if not self.api_url:
            raise ValueError("LangFlow API URL not provided and LANGFLOW_API_URL env var not set")
            
        self.api_key = api_key or os.getenv('LANGFLOW_API_KEY')
        if not self.api_key:
            raise ValueError("API key not provided and LANGFLOW_API_KEY env var not set")
            
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        logger.debug(f"Initialized LangFlow client with API URL: {self.api_url}")
    
    def _make_url(self, endpoint: str) -> str:
        """Create full URL from endpoint."""
        endpoint = endpoint.lstrip('/')
        return urljoin(self.api_url, endpoint)
    
    async def get_flows(self) -> List[Dict[str, Any]]:
        """Get all flows from LangFlow server."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._make_url('/api/v1/flows'),
                headers=self.headers,
                follow_redirects=True
            )
            response.raise_for_status()
            logger.debug(f"Retrieved {len(response.json())} flows")
            return response.json()
    
    async def get_flow(self, flow_id: str) -> Dict[str, Any]:
        """Get flow details by ID."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._make_url(f'/api/v1/flows/{flow_id}'),
                headers=self.headers,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
    
    async def run_flow(self, flow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run a flow with given inputs."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._make_url(f'/api/v1/flows/{flow_id}/run'),
                headers=self.headers,
                json=inputs,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
    
    async def create_flow(self, name: str, description: str = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new flow."""
        payload = {
            "name": name,
            "description": description,
            "data": data or {}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._make_url('/api/v1/flows'),
                headers=self.headers,
                json=payload,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
    
    async def update_flow(self, flow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing flow."""
        async with httpx.AsyncClient() as client:
            response = await client.put(
                self._make_url(f'/api/v1/flows/{flow_id}'),
                headers=self.headers,
                json=data,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
    
    async def delete_flow(self, flow_id: str) -> None:
        """Delete a flow."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._make_url(f'/api/v1/flows/{flow_id}'),
                headers=self.headers,
                follow_redirects=True
            )
            response.raise_for_status()

```

# automagik/core/services/task_runner.py

```py
"""
Task Runner Service

This module provides functionality for managing and executing tasks.
"""

from datetime import datetime
import uuid
from typing import Optional, Dict, Any, List
import logging
import json
from sqlalchemy.orm import Session

from automagik.core.database.models import Task, Log, FlowDB
from automagik.core.services.langflow_client import LangflowClient

logger = logging.getLogger(__name__)

class TaskRunner:
    def __init__(self, session: Session, langflow_client: LangflowClient):
        """Initialize TaskRunner.
        
        Args:
            session: SQLAlchemy database session
            langflow_client: Client for interacting with LangFlow API
        """
        self.session = session
        self.langflow_client = langflow_client

    async def create_task(self, flow_id: uuid.UUID, input_data: Dict[str, Any] = None) -> Task:
        """Create a new task for a flow."""
        flow = self.session.query(FlowDB).filter(FlowDB.id == flow_id).first()
        if not flow:
            raise ValueError(f"Flow {flow_id} not found")
        
        task = Task(
            flow_id=flow_id,
            input_data=input_data or {},
            status="pending",
            tries=0,
            max_retries=3
        )
        self.session.add(task)
        self.session.commit()
        return task

    def _extract_output_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract useful information from the LangFlow response."""
        output_data = {
            "session_id": response.get("session_id"),
            "messages": [],
            "artifacts": [],
            "logs": []
        }
        
        # Extract messages and outputs
        for output in response.get("outputs", []):
            for result in output.get("outputs", []):
                # Get messages
                messages = result.get("messages", [])
                output_data["messages"].extend(messages)
                
                # Get artifacts
                artifacts = result.get("artifacts", [])
                output_data["artifacts"].extend(artifacts)
                
                # Get logs
                logs = result.get("logs", [])
                output_data["logs"].extend(logs)
        
        return output_data

    def _log_message(self, task_id: uuid.UUID, level: str, message: str):
        """Add a log message for a task."""
        log = Log(
            task_id=task_id,
            level=level,
            message=message,
            created_at=datetime.utcnow()
        )
        self.session.add(log)
        self.session.commit()

    async def run_task(self, task_id: uuid.UUID) -> bool:
        """Run a task."""
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")

        try:
            # Update task status
            task.status = "running"
            task.tries += 1
            task.updated_at = datetime.utcnow()
            self.session.commit()
            
            self._log_message(task.id, "info", f"Starting task execution (attempt {task.tries}/{task.max_retries})")
            
            # Run the flow
            flow_response = await self.langflow_client.run_flow(
                str(task.flow_id),
                task.input_data
            )
            
            # Process response
            output_data = self._extract_output_data(flow_response)
            task.output_data = output_data
            task.status = "completed"
            task.updated_at = datetime.utcnow()
            
            self._log_message(task.id, "info", "Task completed successfully")
            
            self.session.commit()
            return True
            
        except Exception as e:
            error_message = str(e)
            self._log_message(task.id, "error", f"Task execution failed: {error_message}")
            
            # Handle retries
            if task.tries < task.max_retries:
                task.status = "pending"
            else:
                task.status = "failed"
            
            task.updated_at = datetime.utcnow()
            self.session.commit()
            return False

    def get_task_logs(self, task_id: uuid.UUID) -> List[Log]:
        """Get all logs for a task."""
        return self.session.query(Log).filter(Log.task_id == task_id).order_by(Log.created_at).all()
```

# docker-compose.yml

```yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:

```

# docs/API.md

```md
# AutoMagik API Documentation

This document covers the AutoMagik REST API endpoints and usage.

## API Documentation Interfaces

AutoMagik provides API documentation in two formats:

### Interactive Documentation

- **Swagger UI** (`/docs`)
  - Interactive API documentation
  - Test endpoints directly in your browser
  - View request/response examples
  - Great for development and testing
  - Available at: http://your-server:8000/docs

### Reference Documentation

- **ReDoc** (`/redoc`)
  - Clean, organized documentation
  - Mobile-responsive design
  - Easy to read and navigate
  - Perfect for API reference
  - Available at: http://your-server:8000/redoc


## Authentication

All API requests require an API key passed in the `X-API-Key` header:

\`\`\`bash
curl -H "X-API-Key: your-api-key" http://your-server:8000/flows
\`\`\`

## Endpoints

### Health Check

\`\`\`http
GET /health
\`\`\`

Returns API health status.

### Flows

#### List Flows
\`\`\`http
GET /flows
\`\`\`

Returns all available flows.

#### Get Flow
\`\`\`http
GET /flows/{flow_id}
\`\`\`

Returns details of a specific flow.

### Tasks

#### List Tasks
\`\`\`http
GET /tasks
\`\`\`

Query Parameters:
- `flow_id` (optional): Filter by flow
- `status` (optional): Filter by status
- `limit` (optional): Maximum number of tasks to return

#### Get Task
\`\`\`http
GET /tasks/{task_id}
\`\`\`

Returns task details including logs and output.

### Schedules

#### List Schedules
\`\`\`http
GET /schedules
\`\`\`

Query Parameters:
- `flow_id` (optional): Filter by flow

#### Get Schedule
\`\`\`http
GET /schedules/{schedule_id}
\`\`\`

Returns schedule details.

## Response Formats

### Flow Response
\`\`\`json
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
\`\`\`

### Task Response
\`\`\`json
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
\`\`\`

### Schedule Response
\`\`\`json
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
\`\`\`

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized (invalid API key)
- 404: Not Found
- 500: Internal Server Error

Error responses include:
\`\`\`json
{
  "error_id": "string",
  "type": "string",
  "detail": "string"
}
\`\`\`

## Rate Limiting

The API currently has no rate limiting but may be added in future versions.

## Best Practices

1. Always check response status codes
2. Include error handling in your code
3. Store API key securely
4. Log API responses for debugging

```

# docs/ARCHITECTURE.md

```md
# AutoMagik Architecture

## Core Services

### Flow Manager
- Handles flow synchronization and storage
- Supports both string and dict data formats from LangFlow API
- Extracts and stores input/output components
- Manages flow metadata and versioning

### Flow Analyzer
- Analyzes flow components and structure
- Identifies input and output nodes
- Extracts tweakable parameters
- Validates flow structure

### Schedule Manager
- Manages flow execution schedules
- Creates and updates schedules
- Handles schedule metadata
- Manages schedule execution state

## Database Models

### FlowDB
- Stores flow data and metadata
- Tracks flow versions and states
- Manages flow relationships

### FlowComponent
- Tracks flow components and their relationships
- Stores component configurations
- Maps input/output connections

### Schedule
- Manages execution schedules for flows
- Tracks schedule states and history
- Handles schedule metadata

## Testing Strategy

### Integration Tests
- Uses SQLite for ephemeral testing
- Mocks LangFlow API responses
- Tests flow sync and schedule creation
- Verifies database operations

### Unit Tests
- Tests individual components
- Validates core functionality
- Ensures data integrity

## Development Status

### Recent Updates
- Added integration testing with SQLite
- Improved flow sync handling
- Enhanced error handling
- Added comprehensive test coverage

### Current Focus
- Improving test reliability
- Enhancing flow sync
- Expanding test coverage

See [TODO.md](/TODO.md) for detailed task tracking.

```

# docs/CLI.md

```md
# AutoMagik CLI Guide

This guide covers the AutoMagik command-line interface tools and usage.

## Global Options

These options apply to all commands:

\`\`\`bash
--help          Show help message
--debug         Enable debug logging
--config FILE   Use alternate config file
\`\`\`

## Flow Management

### List Flows
\`\`\`bash
automagik flows list
\`\`\`

Options:
- `--folder NAME`: Filter by folder
- `--source NAME`: Filter by source
- `--format {table,json}`: Output format

### Sync Flows
\`\`\`bash
automagik flows sync
\`\`\`

Options:
- `--source NAME`: Source to sync from
- `--force`: Force sync even if unchanged

## Task Management

### List Tasks
\`\`\`bash
automagik tasks list
\`\`\`

Options:
- `--flow-id ID`: Filter by flow
- `--status STATUS`: Filter by status
- `--limit N`: Limit number of results

### View Task Output
\`\`\`bash
automagik tasks output <task-id>
\`\`\`

### View Task Logs
\`\`\`bash
automagik tasks logs <task-id>
\`\`\`

Options:
- `--follow`: Follow log output
- `--tail N`: Show last N lines

## Schedule Management

### Create Schedule
\`\`\`bash
automagik schedules create <flow-name>
\`\`\`

Options:
- `--type {cron,interval}`: Schedule type
- `--expr EXPR`: Schedule expression
- `--params JSON`: Flow parameters

### List Schedules
\`\`\`bash
automagik schedules list
\`\`\`

Options:
- `--flow-id ID`: Filter by flow
- `--status STATUS`: Filter by status

### Delete Schedule
\`\`\`bash
automagik schedules delete <schedule-id>
\`\`\`

## Service Management

### Install Service
\`\`\`bash
automagik install-service
\`\`\`

Options:
- `--user NAME`: Run service as user
- `--port PORT`: Service port

### Service Status
\`\`\`bash
automagik service status
\`\`\`

## Database Management

### Initialize Database
\`\`\`bash
automagik db init
\`\`\`

### Migrate Database
\`\`\`bash
automagik db migrate
\`\`\`

Options:
- `--revision REV`: Target revision
- `--sql`: Generate SQL

## Examples

1. Create a scheduled flow:
\`\`\`bash
automagik schedules create "Daily Report" \
  --type cron \
  --expr "0 9 * * *" \
  --params '{"input": "daily report"}'
\`\`\`

2. View recent task failures:
\`\`\`bash
automagik tasks list \
  --status failed \
  --limit 10
\`\`\`

3. Follow task logs:
\`\`\`bash
automagik tasks logs abc123 --follow
\`\`\`

## Environment Variables

The CLI respects these environment variables:

- `AUTOMAGIK_API_KEY`: API authentication key
- `AUTOMAGIK_CONFIG`: Config file location
- `AUTOMAGIK_DEBUG`: Enable debug logging
- `DATABASE_URL`: Database connection string

## Configuration File

The CLI can be configured via `~/.automagik/config.yaml`:

\`\`\`yaml
api_key: your-api-key
database_url: postgresql://...
log_level: INFO
\`\`\`

## Logging

CLI logs are written to:
- `~/.automagik/cli.log`: Command execution logs
- `~/.automagik/debug.log`: Debug logs (if enabled)

## Troubleshooting

Common CLI issues:

1. **Command Not Found**
   - Ensure virtual environment is activated
   - Check PATH includes .venv/bin

2. **Authentication Errors**
   - Verify AUTOMAGIK_API_KEY is set
   - Check API key in config file

3. **Database Errors**
   - Verify DATABASE_URL is correct
   - Check database connectivity

```

# docs/DEVELOPMENT.md

```md
# AutoMagik Development Guide

This guide covers development setup and best practices for AutoMagik.

## Development Setup

### 1. Clone and Setup

\`\`\`bash
# Clone repository
git clone https://github.com/namastexlabs/automagik.git
cd automagik

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
\`\`\`

### 2. Configure Environment

\`\`\`bash
# Copy example environment
cp .env.example .env

# Edit .env with development settings
DATABASE_URL=postgresql://localhost/automagik_dev
AUTOMAGIK_API_KEY=dev-key
\`\`\`

### 3. Setup Database

\`\`\`bash
# Create development database
createdb automagik_dev

# Run migrations
automagik db upgrade
\`\`\`

## Project Structure

\`\`\`
automagik/
├── automagik/
│   ├── api/           # FastAPI application
│   ├── cli/           # CLI commands
│   ├── core/          # Core business logic
│   │   ├── services/   # Main services
│   │   ├── database/   # Database models
│   │   └── utils/      # Utilities
│   └── utils/         # Utility functions
├── docs/              # Documentation
├── scripts/           # Helper scripts
├── tests/             # Test suite
└── alembic/           # Database migrations
\`\`\`

## Testing

### Running Tests

\`\`\`bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=automagik

# Generate coverage report
coverage html
\`\`\`

### Writing Tests

1. Place tests in `tests/` directory
2. Name test files `test_*.py`
3. Use fixtures from `conftest.py`
4. Mock external services

Example test:
\`\`\`python
def test_flow_creation(client, mock_langflow):
    response = client.post("/flows", json={...})
    assert response.status_code == 200
\`\`\`

## Code Style

We use:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run formatters:
\`\`\`bash
# Format code
black automagik tests

# Sort imports
isort automagik tests

# Run linter
flake8 automagik tests

# Type check
mypy automagik
\`\`\`

## Database Migrations

### Create Migration

\`\`\`bash
# Generate migration
alembic revision -m "description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
\`\`\`

### Migration Guidelines

1. Make migrations reversible
2. Test both upgrade and downgrade
3. Don't modify existing migrations
4. Include data migrations when needed

## Debugging

### API Debugging

1. Enable debug mode in `.env`:
\`\`\`bash
DEBUG=True
LOG_LEVEL=DEBUG
\`\`\`

2. Run API with reload:
\`\`\`bash
uvicorn automagik.api.main:app --reload --log-level debug
\`\`\`

### CLI Debugging

Run with debug flag:
\`\`\`bash
automagik --debug flows list
\`\`\`

## Documentation

### API Documentation

1. Document new endpoints in `docs/API.md`
2. Update OpenAPI schema
3. Include request/response examples

### Code Documentation

1. Use Google-style docstrings
2. Document all public functions
3. Include type hints

Example:
\`\`\`python
def get_flow(flow_id: str) -> Flow:
    """Get flow by ID.

    Args:
        flow_id: Unique flow identifier

    Returns:
        Flow object if found

    Raises:
        FlowNotFound: If flow doesn't exist
    """
\`\`\`

## Logging

### Log Levels

- DEBUG: Detailed debugging
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical failures

### Best Practices

1. Use structured logging
2. Include context
3. Don't log sensitive data
4. Use appropriate levels

Example:
\`\`\`python
logger.info("Processing flow", 
    extra={
        "flow_id": flow.id,
        "user_id": user.id
    }
)
\`\`\`

## Error Handling

### API Errors

1. Use custom exceptions
2. Return consistent error responses
3. Log full stack traces
4. Hide internal details from users

Example:
\`\`\`python
try:
    process_flow(flow_id)
except FlowNotFound:
    raise HTTPException(status_code=404)
except Exception as e:
    logger.exception("Flow processing failed")
    raise HTTPException(status_code=500)
\`\`\`

## Contributing

1. Create feature branch
2. Write tests
3. Update documentation
4. Submit pull request

### Pull Request Checklist

- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped

```

# docs/SETUP.md

```md
# AutoMagik Setup Guide

This guide covers the installation and setup of AutoMagik.

## Prerequisites

Before installing AutoMagik, ensure you have:

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Redis Server
- LangFlow instance

## Installation Methods

### 1. Quick Installation (Recommended)

Use our automated setup script:

\`\`\`bash
# Clone the repository
git clone https://github.com/namastexlabs/automagik.git
cd automagik

# Copy and edit environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the setup script
sudo ./scripts/setup.sh
\`\`\`

### 2. Manual Installation

If you prefer manual control:

1. Clone and prepare:
\`\`\`bash
git clone https://github.com/namastexlabs/automagik.git
cd automagik
python -m venv .venv
source .venv/bin/activate
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -e .
\`\`\`

3. Configure environment:
\`\`\`bash
cp .env.example .env
# Edit .env with your settings
\`\`\`

4. Initialize database:
\`\`\`bash
automagik db init
\`\`\`

5. Set up logging:
\`\`\`bash
sudo mkdir -p /var/log/automagik
sudo chown -R root:root /var/log/automagik
\`\`\`

6. Install service:
\`\`\`bash
automagik install-service
sudo systemctl daemon-reload
sudo systemctl enable automagik
sudo systemctl start automagik
\`\`\`

## Environment Configuration

Required variables in `.env`:

\`\`\`bash
# API Key for AutoMagik API authentication
AUTOMAGIK_API_KEY=your-api-key

# PostgreSQL database URL
DATABASE_URL=postgresql://user:password@localhost:5432/automagik_db

# LangFlow configuration
LANGFLOW_API_URL=http://your-langflow-instance
LANGFLOW_API_KEY=your-langflow-api-key
\`\`\`

## Logging Configuration

Logs are stored in:
- `/var/log/automagik/api.log`: API access logs
- `/var/log/automagik/error.log`: Error logs

## Service Management

Control the service:
\`\`\`bash
# Start service
sudo systemctl start automagik

# Check status
sudo systemctl status automagik

# Stop service
sudo systemctl stop automagik

# View logs
tail -f /var/log/automagik/api.log
tail -f /var/log/automagik/error.log
\`\`\`

## Troubleshooting

### Common Issues

1. **Database Connection**
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Ensure database and user exist

2. **Service Won't Start**
   - Check error logs
   - Verify environment variables
   - Ensure PostgreSQL and Redis are running

3. **Port Conflicts**
   - Check if port 8000 is in use
   - Find conflicting process: `sudo lsof -i :8000`
   - Stop process or change port

### Getting Help

If you encounter issues:
1. Check the error logs
2. Review environment configuration
3. Ensure all prerequisites are met
4. Contact support with log files

```

# pytest.ini

```ini
[pytest]
asyncio_mode = strict
asyncio_default_fixture_loop_scope = function

```

# README.md

```md
# AutoMagik

AutoMagik is a powerful task automation and scheduling system that integrates with LangFlow to run AI workflows.

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis (for Celery)
- LangFlow server

### 1. Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/namastexlabs/automagik.git
cd automagik

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
\`\`\`

### 2. Configuration

Create a `.env` file in the root directory:

\`\`\`bash
# Environment
ENV=development

# Security
AUTOMAGIK_API_KEY=your-api-key

# PostgreSQL Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/automagik_db

# Redis & Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# LangFlow Configuration
LANGFLOW_API_URL=http://localhost:7860
LANGFLOW_API_KEY=your-langflow-api-key

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
\`\`\`

### 3. Database Setup

\`\`\`bash
# Start PostgreSQL (if not running)
sudo service postgresql start

# Create database and user
sudo -u postgres psql
postgres=# CREATE USER your_user WITH PASSWORD 'your_password';
postgres=# CREATE DATABASE automagik_db OWNER your_user;
postgres=# \q
\`\`\`

### 4. Running the Services

\`\`\`bash
# Start Redis (if not running)
sudo service redis-server start

# Start the API server
uvicorn automagik.api.main:app --reload --port 8000 --host 0.0.0.0

# Start the task processor
automagik run start

# Start the Celery worker (in a new terminal)
celery -A automagik.core.celery_app worker --loglevel=info
\`\`\`

### 5. Testing the Setup

\`\`\`bash
# Test the API
curl http://localhost:8000/health

# Create and test a flow
automagik flows sync  # Sync flows from LangFlow
automagik flows list  # List available flows
automagik run test <flow-id>  # Test run a flow
\`\`\`

## Features

- **Flow Management**: Sync and manage LangFlow workflows
- **Task Scheduling**: Schedule flows to run at specific intervals
- **Task Execution**: Run flows with custom inputs and handle retries
- **API Integration**: RESTful API for managing flows, schedules, and tasks
- **Monitoring**: Track task status and view execution logs

## Documentation

### Guides and References
- [Setup Guide](/docs/SETUP.md) - Detailed installation and configuration
- [CLI Reference](/docs/CLI.md) - Command-line interface documentation
- [Development Guide](/docs/DEVELOPMENT.md) - Contributing and development setup
- [Architecture](/docs/ARCHITECTURE.md) - System design and components

### API Documentation
- [API Guide](/docs/API.md) - REST API overview and usage
- Interactive API Explorer (Swagger UI): http://localhost:8000/docs
- API Reference (ReDoc): http://localhost:8000/redoc

## CLI Reference

\`\`\`bash
# General commands
automagik --help                  # Show all available commands

# Flow management
automagik flows list             # List all flows
automagik flows sync             # Sync flows from LangFlow
automagik flows get <flow-id>    # Get flow details

# Schedule management
automagik schedules list         # List all schedules
automagik schedules create       # Create a new schedule
automagik schedules get <id>     # Get schedule details

# Task management
automagik run start             # Start the task processor
automagik run test <flow-id>    # Test run a flow
\`\`\`

## CLI Examples

### Flow Management
\`\`\`bash
# List all flows with their IDs and status
automagik flows list

# Get details of a specific flow
automagik flows get 3cf82804-41b2-4731-9306-f77e17193799

# Sync flows from LangFlow server
automagik flows sync
\`\`\`

### Schedule Management
\`\`\`bash
# Create a new schedule for a flow
automagik schedules create \
  --flow-id 3cf82804-41b2-4731-9306-f77e17193799 \
  --type interval \
  --expr "1m" \
  --input '{"message": "Hello, World!"}'

# List all schedules
automagik schedules list

# Get schedule details
automagik schedules get 3cf82804-41b2-4731-9306-f77e17193799

# Update schedule status
automagik schedules update 3cf82804-41b2-4731-9306-f77e17193799 --status disabled
\`\`\`

### Task Management
\`\`\`bash
# Test run a flow with input
automagik run test 3cf82804-41b2-4731-9306-f77e17193799 \
  --input '{"message": "Test message"}'

# Start task processor in daemon mode
automagik run start --daemon

# Start task processor with debug logging
automagik run start --log-level DEBUG

# View task logs
automagik tasks logs 3cf82804-41b2-4731-9306-f77e17193799

# List recent tasks
automagik tasks list --limit 10 --status completed
\`\`\`

### Common Testing Scenarios

1. **Test Flow Sync and Listing**
\`\`\`bash
# Sync flows and verify they appear in list
automagik flows sync
automagik flows list | grep "WhatsApp"
\`\`\`

2. **Test Schedule Creation and Execution**
\`\`\`bash
# Create a one-time schedule
FLOW_ID=$(automagik flows list | grep "WhatsApp" | cut -d' ' -f1)
automagik schedules create \
  --flow-id $FLOW_ID \
  --type oneshot \
  --expr "2025-01-24T00:00:00" \
  --input '{"message": "Scheduled test"}'

# Verify schedule was created
automagik schedules list | grep $FLOW_ID
\`\`\`


3. **Test Flow Execution with Different Inputs**
\`\`\`bash
# Test with text input
automagik run test $FLOW_ID --input '{"message": "Text input test"}'

# Test with JSON input
automagik run test $FLOW_ID --input '{"message": "JSON test", "metadata": {"source": "cli", "priority": "high"}}'

# Test with file input
echo '{"message": "File test"}' > test_input.json
automagik run test $FLOW_ID --input @test_input.json
\`\`\`

4. **Test Error Handling**
\`\`\`bash
# Test with invalid flow ID
automagik run test invalid-id

# Test with invalid input format
automagik run test $FLOW_ID --input 'invalid json'

# Test with missing required input
automagik run test $FLOW_ID --input '{}'
\`\`\`

5. **Test Task Monitoring**
\`\`\`bash
# Monitor task execution
TASK_ID=$(automagik run test $FLOW_ID --input '{"message": "Monitor test"}' | grep "Created task" | cut -d' ' -f3)
automagik tasks logs $TASK_ID --follow

# Check task status
automagik tasks get $TASK_ID
\`\`\`

### Environment Testing
\`\`\`bash
# Test with different API URLs
LANGFLOW_API_URL=http://other-server:7860 automagik flows list

# Test with different API keys
LANGFLOW_API_KEY=new-key automagik flows sync

# Test with debug logging
AUTOMAGIK_LOG_LEVEL=DEBUG automagik run test $FLOW_ID
\`\`\`

## Development Status

### Recent Updates
- Added integration testing with SQLite for ephemeral test databases
- Improved flow sync to handle different API response formats
- Added test cases for flow and schedule creation
- Enhanced error handling in core services

### Current Focus
- Improving integration test reliability
- Enhancing flow sync functionality
- Adding comprehensive test coverage

Check [TODO.md](TODO.md) for current tasks and upcoming features.

## Architecture

### Core Services
- **Flow Manager**: Handles flow synchronization and storage
  - Supports both string and dict data formats from LangFlow API
  - Extracts and stores input/output components
  - Manages flow metadata and versioning

- **Flow Analyzer**: Analyzes flow components and structure
  - Identifies input and output nodes
  - Extracts tweakable parameters
  - Validates flow structure

- **Schedule Manager**: Manages flow execution schedules
  - Creates and updates schedules
  - Handles schedule metadata
  - Manages schedule execution state

### Database Models
- **FlowDB**: Stores flow data and metadata
- **FlowComponent**: Tracks flow components and their relationships
- **Schedule**: Manages execution schedules for flows

### Testing
- **Integration Tests**: Uses SQLite for ephemeral testing
  - Mocks LangFlow API responses
  - Tests flow sync and schedule creation
  - Verifies database operations

## Development

\`\`\`bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8
black .
isort .
\`\`\`

For more detailed information, check out our [documentation](docs/README.md).

## License

This project is licensed under the terms of the MIT license.

```

# requirements.txt

```txt
click>=8.0.0
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
tabulate>=0.9.0
croniter>=1.4.1
pytz>=2023.3
setuptools>=65.0.0
httpx>=0.24.1
inquirer>=3.1.3
celery>=5.3.0
redis>=4.5.0
pytest>=7.4.0
alembic>=1.12.0
psycopg2-binary>=2.9.9
# Testing dependencies
pytest-asyncio>=0.21.1
requests>=2.31.0

```

# scripts/setup.sh

```sh
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is not installed. Please install it first."
        exit 1
    fi
}

# Function to check if a service is running
check_service() {
    if ! systemctl is-active --quiet $1; then
        print_error "$1 is not running. Please start it first."
        exit 1
    fi
}

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root"
    exit 1
fi

print_status "Starting AutoMagik setup..."

# Check prerequisites
print_status "Checking prerequisites..."
check_command python3
check_command pip3
check_command postgresql
check_command redis-server

# Check PostgreSQL and Redis services
print_status "Checking required services..."
check_service postgresql
check_service redis-server

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
pip install -e .

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning "Please update the .env file with your configuration"
    else
        print_error ".env.example file not found"
        exit 1
    fi
fi

# Load environment variables
set -a
source .env
set +a

# Test database connection
print_status "Testing database connection..."
if ! psql "${DATABASE_URL}" -c '\q' 2>/dev/null; then
    print_error "Could not connect to database. Please check your DATABASE_URL in .env"
    exit 1
fi

# Create log directory
print_status "Setting up logging..."
mkdir -p /var/log/automagik
chown -R root:root /var/log/automagik

# Check if port 8000 is in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    print_warning "Port 8000 is already in use. Stopping conflicting process..."
    lsof -ti :8000 | xargs kill -9
fi

# Install systemd service
print_status "Installing systemd service..."
cat > /etc/systemd/system/automagik.service << EOL
[Unit]
Description=AutoMagik Service
After=network.target postgresql.service redis.service
Requires=postgresql.service redis.service

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/automagik

# Environment setup
Environment=PATH=/root/automagik/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONPATH=/root/automagik
Environment=LOG_LEVEL=INFO
EnvironmentFile=/root/automagik/.env

# Logging
StandardOutput=append:/var/log/automagik/api.log
StandardError=append:/var/log/automagik/error.log

# Start command with proper logging
ExecStartPre=/bin/mkdir -p /var/log/automagik
ExecStartPre=/bin/chown -R root:root /var/log/automagik
ExecStart=/root/automagik/.venv/bin/uvicorn automagik.api.main:app --host 0.0.0.0 --port 8000 --log-level info

# Restart configuration
Restart=always
RestartSec=3

# Give the service time to start up
TimeoutStartSec=30

# Limit resource usage
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and enable service
print_status "Configuring service..."
systemctl daemon-reload
systemctl enable automagik
systemctl restart automagik

# Wait for service to start
print_status "Waiting for service to start..."
sleep 5

# Test API
print_status "Testing API..."
if curl -s -f -X GET "http://localhost:8000/health" -H "accept: application/json" > /dev/null; then
    print_status "API is running successfully!"
else
    print_error "API failed to start. Check logs at /var/log/automagik/error.log"
    exit 1
fi

print_status "Setup completed successfully!"
print_status "You can check the logs at:"
print_status "  - API logs: /var/log/automagik/api.log"
print_status "  - Error logs: /var/log/automagik/error.log"
print_status "To check service status: sudo systemctl status automagik"

```

# setup.py

```py
from setuptools import setup, find_packages

setup(
    name="automagik",
    version="0.1.0",
    packages=find_packages(include=['automagik*']),
    package_data={
        'cli': ['templates/*'],
    },
    include_package_data=True,
    install_requires=[
        'click>=8.0.0',
        'sqlalchemy>=2.0.0',
        'python-dotenv>=1.0.0',
        'tabulate>=0.9.0',
        'croniter>=1.4.1',
        'pytz>=2023.3',
        'setuptools>=65.0.0',
        'httpx>=0.24.0',
        'inquirer>=3.1.3',
        'celery>=5.3.0',
        'redis>=4.5.0',
        'psycopg2-binary>=2.9.0',  # PostgreSQL adapter
        'alembic>=1.12.0',  # Database migrations
        'fastapi>=0.104.0',  # API framework
        'uvicorn>=0.24.0',  # ASGI server
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.1.0',
            'mypy>=1.5.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'automagik=automagik.cli.cli:cli',
        ],
    },
    python_requires='>=3.9',
)
```

# tests/__init__.py

```py


```

# tests/conftest.py

```py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from automagik.core.database.models import Base
from automagik.core.database.session import get_db_session

# Create an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture
def db_session(engine):
    """Create a new database session for a test."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

```

# tests/test_api.py

```py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import uuid

from automagik.api.main import app
from automagik.core.database.models import FlowDB, Schedule, Task
from automagik.core.database.session import get_db_session

client = TestClient(app)

# Test data
TEST_API_KEY = "namastex-888"
HEADERS = {"X-API-Key": TEST_API_KEY}

# Sample data for testing
SAMPLE_FLOW_ID = str(uuid.uuid4())
SAMPLE_SCHEDULE_ID = str(uuid.uuid4())
SAMPLE_TASK_ID = str(uuid.uuid4())

@pytest.fixture
def db_session():
    """Get a database session for testing."""
    with get_db_session() as session:
        yield session

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_list_flows():
    """Test listing flows endpoint."""
    response = client.get("/flows", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "flows" in data
    assert isinstance(data["flows"], list)
    
    # Validate flow structure if any flows exist
    if data["flows"]:
        flow = data["flows"][0]
        assert "id" in flow
        assert "name" in flow
        assert "description" in flow
        assert "source" in flow
        assert "source_id" in flow
        assert "data" in flow
        assert "created_at" in flow
        assert "updated_at" in flow
        assert "tags" in flow

def test_get_flow():
    """Test getting a specific flow endpoint."""
    # First get list of flows
    response = client.get("/flows", headers=HEADERS)
    assert response.status_code == 200
    flows = response.json()["flows"]
    
    if flows:
        # Test getting an existing flow
        flow_id = flows[0]["id"]
        response = client.get(f"/flows/{flow_id}", headers=HEADERS)
        assert response.status_code == 200
        flow = response.json()
        assert flow["id"] == flow_id
    
    # Test getting a non-existent flow
    response = client.get(f"/flows/{uuid.uuid4()}", headers=HEADERS)
    assert response.status_code == 404

def test_list_schedules():
    """Test listing schedules endpoint."""
    response = client.get("/schedules", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "schedules" in data
    assert isinstance(data["schedules"], list)
    
    # Validate schedule structure if any schedules exist
    if data["schedules"]:
        schedule = data["schedules"][0]
        assert "id" in schedule
        assert "flow_id" in schedule
        assert "schedule_type" in schedule
        assert "schedule_expr" in schedule
        assert "flow_params" in schedule
        assert "status" in schedule
        assert "next_run_at" in schedule
        assert "created_at" in schedule
        assert "updated_at" in schedule

def test_get_schedule():
    """Test getting a specific schedule endpoint."""
    # First get list of schedules
    response = client.get("/schedules", headers=HEADERS)
    assert response.status_code == 200
    schedules = response.json()["schedules"]
    
    if schedules:
        # Test getting an existing schedule
        schedule_id = schedules[0]["id"]
        response = client.get(f"/schedules/{schedule_id}", headers=HEADERS)
        assert response.status_code == 200
        schedule = response.json()
        assert schedule["id"] == schedule_id
    
    # Test getting a non-existent schedule
    response = client.get(f"/schedules/{uuid.uuid4()}", headers=HEADERS)
    assert response.status_code == 404

def test_list_tasks():
    """Test listing tasks endpoint."""
    response = client.get("/tasks", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
    
    # Validate task structure if any tasks exist
    if data["tasks"]:
        task = data["tasks"][0]
        assert "id" in task
        assert "flow_id" in task
        assert "status" in task
        assert "input_data" in task
        assert "created_at" in task
        assert "updated_at" in task

def test_get_task():
    """Test getting a specific task endpoint."""
    # First get list of tasks
    response = client.get("/tasks", headers=HEADERS)
    assert response.status_code == 200
    tasks = response.json()["tasks"]
    
    if tasks:
        # Test getting an existing task
        task_id = tasks[0]["id"]
        response = client.get(f"/tasks/{task_id}", headers=HEADERS)
        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
    
    # Test getting a non-existent task
    response = client.get(f"/tasks/{uuid.uuid4()}", headers=HEADERS)
    assert response.status_code == 404

def test_api_key_validation():
    """Test API key validation."""
    # Test without API key
    response = client.get("/flows")
    assert response.status_code == 401
    
    # Test with invalid API key
    response = client.get("/flows", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 401
    
    # Test with valid API key
    response = client.get("/flows", headers=HEADERS)
    assert response.status_code == 200

def test_error_handling():
    """Test error handling."""
    # Test 404 error
    response = client.get("/nonexistent-endpoint", headers=HEADERS)
    assert response.status_code == 404
    
    # Test invalid UUID format
    response = client.get("/flows/not-a-uuid", headers=HEADERS)
    assert response.status_code in [400, 404, 422]  # Depending on how we handle invalid UUIDs

```

# tests/test_cli.py

```py
"""
Test CLI Commands

This module contains tests for the AutoMagik CLI commands.
"""

import os
import pytest
import uuid
import json
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from automagik.cli.commands.flows import flows
from automagik.cli.commands.schedules import schedules
from automagik.cli.commands.run import run
from automagik.core.database.models import FlowDB, Schedule, Task
from automagik.core.services.langflow_client import LangflowClient
from automagik.core.services.task_runner import TaskRunner

# Test data
TEST_FLOW_ID = str(uuid.uuid4())
TEST_SCHEDULE_ID = str(uuid.uuid4())
TEST_TASK_ID = str(uuid.uuid4())

@pytest.fixture
def mock_db_session():
    """Mock database session"""
    with patch('automagik.core.database.get_db_session') as mock:
        session = mock()
        session.add = MagicMock()
        session.commit = MagicMock()
        
        # Mock query builder
        query = MagicMock()
        query.all = MagicMock()
        query.filter = MagicMock(return_value=query)
        query.first = MagicMock()
        session.query = MagicMock(return_value=query)
        yield session

@pytest.fixture
def mock_langflow_client():
    """Mock LangFlow client"""
    with patch('automagik.core.services.langflow_client.LangflowClient') as mock:
        client = mock.return_value
        # Mock the async methods
        client.get_flows = MagicMock(return_value=[{
            'id': TEST_FLOW_ID,
            'name': 'Test Flow',
            'description': 'Test flow description'
        }])
        client.get_flow = MagicMock()
        client.run_flow = MagicMock()
        yield client

@pytest.fixture
def mock_task_runner():
    """Mock TaskRunner"""
    with patch('automagik.core.services.task_runner.TaskRunner') as mock:
        runner = mock.return_value
        runner.process_schedules = MagicMock()
        runner.run_task = MagicMock()
        yield runner

@pytest.fixture
def runner():
    """Click test runner"""
    return CliRunner()

@pytest.fixture
def sample_flow():
    """Sample flow data"""
    return FlowDB(
        id=uuid.UUID(TEST_FLOW_ID),
        name="Test Flow",
        description="Test flow description",
        source="langflow",
        folder_name="test",
        input_component=True,
        output_component=True,
        flow_version=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

@pytest.fixture
def sample_schedule():
    """Sample schedule data"""
    return Schedule(
        id=uuid.UUID(TEST_SCHEDULE_ID),
        flow_id=uuid.UUID(TEST_FLOW_ID),
        schedule_type="interval",
        schedule_expr="1m",
        status="active",
        next_run_at=datetime.utcnow() + timedelta(minutes=1),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

class TestFlowCommands:
    """Test flow-related CLI commands"""

    def test_flows_list(self, runner, mock_db_session, sample_flow):
        """Test listing flows"""
        # Set specific values for the flow to match expected output
        sample_flow.name = "WhatsApp Audio to Message Automation 1D (prod)"
        sample_flow.folder_name = "whatsapp-pal"
        sample_flow.id = uuid.UUID("9b6b04c3-64d0-4a02-a3ef-a9ae126b733d")
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        result = runner.invoke(flows, ['list'])
        assert result.exit_code == 0
        assert str(sample_flow.id) in result.output
        assert sample_flow.name in result.output
        assert sample_flow.folder_name in result.output

    @pytest.mark.asyncio
    async def test_flows_sync(self, runner, mock_db_session, mock_langflow_client):
        """Test syncing flows"""
        result = runner.invoke(flows, ['sync'], input='0\n')
        assert result.exit_code == 0
        assert "Flow synced successfully" in result.output

class TestScheduleCommands:
    """Test schedule-related CLI commands"""

    def test_schedules_list(self, runner, mock_db_session, sample_schedule, sample_flow):
        """Test listing schedules"""
        # Set specific values to match expected output
        sample_flow.name = "WhatsApp Audio to Message Automation 1D (prod)"
        sample_schedule.id = uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799")
        sample_schedule.schedule_type = "interval"
        sample_schedule.schedule_expr = "1m"
        sample_schedule.status = "active"
        sample_schedule.next_run_at = datetime(2025, 1, 23, 4, 51, 38)
        sample_schedule.flow = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_schedule]
        
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert str(sample_schedule.id) in result.output
        assert sample_schedule.schedule_type in result.output
        assert sample_schedule.schedule_expr in result.output
        assert sample_schedule.status in result.output
        assert "2025-01-23 04:51:38" in result.output

    def test_schedules_create(self, runner, mock_db_session, sample_flow):
        """Test creating a schedule"""
        # Mock the flow relationship and query results
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        # Simulate user input:
        # 0 - Select the first flow
        # 0 - Select interval type
        # 5m - Set interval to 5 minutes
        # y - Yes to set input value
        # vai filhote - The input value
        result = runner.invoke(schedules, ['create'], input='0\n0\n5m\ny\nvai filhote\n')
        
        assert result.exit_code == 0
        assert "Schedule created successfully" in result.output
        assert "Flow: WhatsApp Audio to Message Automation 1D (prod)" in result.output
        assert "Type: interval" in result.output
        assert "Expression: 5m" in result.output
        assert "2025-01-23" in result.output  # Check for date in next run

class TestRunCommands:
    """Test run-related CLI commands"""

    @pytest.mark.asyncio
    async def test_run_test(self, runner, mock_db_session, mock_langflow_client, sample_schedule, caplog):
        """Test running a flow test"""
        # Set specific ID to match the error message
        sample_schedule.id = uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799")
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_schedule
        mock_langflow_client.run_flow.return_value = {"status": "success"}
        
        try:
            runner.invoke(run, ['test', str(sample_schedule.id)], catch_exceptions=False)
        except RuntimeError:
            pass  # Expected asyncio error
        
        assert any("Testing schedule" in record.message for record in caplog.records)

    def test_run_start_no_daemon(self, runner, mock_task_runner, caplog):
        """Test starting task processor without daemon mode"""
        with patch('automagik.cli.commands.run.TaskRunner', return_value=mock_task_runner):
            try:
                runner.invoke(run, ['start'], catch_exceptions=False)
            except RuntimeError:
                pass  # Expected asyncio error
            
            assert any("Starting AutoMagik service" in record.message for record in caplog.records)

    def test_invalid_flow_id(self, runner, mock_db_session):
        """Test handling invalid flow ID"""
        # Set empty list to indicate no flows
        mock_db_session.query.return_value.all.return_value = []
        
        result = runner.invoke(flows, ['list'])
        assert result.exit_code == 0
        # When no flows are present, the output should be empty or just contain table headers
        assert len([line for line in result.output.splitlines() if line.strip() and '|' in line]) <= 3

    def test_invalid_schedule_type(self, runner, mock_db_session, sample_flow):
        """Test creating schedule with invalid type"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        result = runner.invoke(schedules, ['create'], input='0\n99\n')  # Invalid schedule type
        assert "Invalid schedule type" in result.output

    def test_invalid_json_input(self, runner, mock_db_session, sample_flow):
        """Test handling invalid JSON input"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        # Since the CLI accepts any string input, we'll test that it properly wraps it in a dict
        result = runner.invoke(schedules, ['create'], input='0\n0\n5m\ny\n{invalid json}\n')
        assert "'input': '{invalid json}'" in result.output

```

# tests/test_integration.py

```py
import os
import uuid
import pytest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from automagik.core.database.models import Base, FlowDB, Schedule
from automagik.cli.commands.flows import flows
from automagik.cli.commands.run import run
from automagik.cli.commands.schedules import schedules
from automagik.core.database import get_db_session

@pytest.fixture
def temp_db(monkeypatch):
    """Create a temporary SQLite database for testing."""
    # Create a temporary file to store the SQLite database
    temp_db_file = tempfile.NamedTemporaryFile(delete=False)
    db_url = f"sqlite:///{temp_db_file.name}"
    
    # Create the database and tables
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Patch the get_db_session to use our temporary database
    monkeypatch.setattr('automagik.core.database.get_db_session', lambda: session)
    
    yield session
    
    # Cleanup
    session.close()
    temp_db_file.close()
    os.unlink(temp_db_file.name)

@pytest.fixture
def sample_flow(temp_db):
    """Create a sample flow in the database."""
    flow = FlowDB(
        id=uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799"),
        name="Test Flow",
        description="A test flow",
        data={"nodes": [], "edges": []},
        source="langflow",
        source_id="test_flow",
        flow_version=1,
        input_component="test_input",
        output_component="test_output"
    )
    temp_db.add(flow)
    temp_db.commit()
    return flow

@pytest.fixture
def sample_schedule(temp_db, sample_flow):
    """Create a sample schedule in the database."""
    schedule = Schedule(
        id=uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799"),
        flow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="1m",
        flow_params={"test": "data"},
        status="active"
    )
    temp_db.add(schedule)
    temp_db.commit()
    return schedule

@pytest.fixture
def runner():
    """Create a Click CLI runner."""
    from click.testing import CliRunner
    return CliRunner()

class TestIntegration:
    """Integration tests using a real SQLite database."""
    
    def test_flows_list(self, runner, temp_db, sample_flow):
        """Test listing flows from the database."""
        result = runner.invoke(flows, ['list'])
        assert result.exit_code == 0
        assert "Test Flow" in result.output
        
    def test_schedules_list(self, runner, temp_db, sample_schedule):
        """Test listing schedules from the database."""
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert "interval" in result.output
        assert "1m" in result.output
        
    def test_schedule_create(self, runner, temp_db, sample_flow):
        """Test creating a schedule in the database."""
        result = runner.invoke(schedules, ['create'], input='3cf82804-41b2-4731-9306-f77e17193799\ninterval\n1m\n{"test":"input"}\n')
        assert result.exit_code == 0
        
        # Verify schedule was created
        schedule = temp_db.query(Schedule).first()
        assert schedule is not None
        assert schedule.schedule_type == "interval"
        assert schedule.schedule_expr == "1m"
        
    def test_flow_sync(self, runner, temp_db, monkeypatch):
        """Test syncing flows to the database."""
        # Mock environment variables
        monkeypatch.setenv('LANGFLOW_API_URL', 'http://test.com')
        monkeypatch.setenv('LANGFLOW_API_KEY', 'test_key')

        # First, ensure the database is empty
        temp_db.query(FlowDB).delete()
        temp_db.commit()
        
        # Mock FlowSync methods
        def mock_get_remote_flows():
            return [{
                'id': '123',
                'name': 'Test Flow',
                'description': 'A test flow'
            }]
            
        def mock_get_flow_details(flow_id):
            return {
                'id': flow_id,
                'name': 'Test Flow',
                'description': 'A test flow',
                'data': {
                    'nodes': [],
                    'edges': []
                }
            }
            
        from automagik.core.services.flow_sync import FlowSync
        monkeypatch.setattr(FlowSync, 'get_remote_flows', mock_get_remote_flows)
        monkeypatch.setattr(FlowSync, 'get_flow_details', mock_get_flow_details)
        
        result = runner.invoke(flows, ['sync'])
        assert result.exit_code == 0
        
        # Verify flows were synced
        flows_count = temp_db.query(FlowDB).count()
        assert flows_count > 0
```

