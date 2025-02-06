"""
Database Management Commands

Provides CLI commands for managing the database:
- Initialize database
- Run migrations
- Clear database
"""

import asyncio
import click
import logging
import os
import sys
import shutil
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
from alembic.config import Config
from alembic import command
from alembic.util import CommandError

from ...core.database import Base
from ...core.database.session import get_session, async_engine as engine, DATABASE_URL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
MIGRATIONS_DIR = PROJECT_ROOT / 'migrations'

def create_alembic_ini():
    """Create alembic.ini with our configuration."""
    alembic_ini = PROJECT_ROOT / 'alembic.ini'
    with open(alembic_ini, 'w') as f:
        f.write(f"""[alembic]
# path to migration scripts
script_location = migrations

# template used to generate migration files
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# timezone to use when rendering the date
# within the migration file as well as the filename.
timezone = UTC

# max length of characters to apply to the
# "slug" field
truncate_slug_length = 40

sqlalchemy.url = {DATABASE_URL}

[post_write_hooks]

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
""")

def create_env_py():
    """Create env.py with our configuration."""
    env_py = MIGRATIONS_DIR / 'env.py'
    with open(env_py, 'w') as f:
        f.write("""import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from automagik.core.database import Base
from automagik.core.database.session import DATABASE_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    \"\"\"Run migrations in 'offline' mode.\"\"\"
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    \"\"\"In this scenario we need to create an Engine
    and associate a connection with the context.\"\"\"

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    \"\"\"Run migrations in 'online' mode.\"\"\"
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""")

db_group = click.Group(name="db", help="Database management commands")

@db_group.command()
def init():
    """Initialize database and migrations."""
    try:
        # Only initialize if migrations directory doesn't exist
        if not MIGRATIONS_DIR.exists():
            # Create empty migrations directory
            os.makedirs(MIGRATIONS_DIR)
            
            # Create temporary alembic.ini for initialization
            alembic_ini = PROJECT_ROOT / 'alembic.ini'
            with open(alembic_ini, 'w') as f:
                f.write("""[alembic]
script_location = migrations
""")
            
            # Initialize alembic
            click.echo("Initializing alembic...")
            alembic_cfg = Config(str(alembic_ini))
            command.init(config=alembic_cfg, directory=str(MIGRATIONS_DIR), template='async')
            
            # Update config files with our custom content
            click.echo("Updating configuration...")
            create_alembic_ini()
            create_env_py()
            
            click.echo("Database initialization complete!")
            click.echo("\nNext steps:")
            click.echo("1. Run 'automagik db migrate' to create initial migration")
            click.echo("2. Run 'automagik db upgrade' to apply migrations")
        else:
            click.echo("Migrations directory already exists. Skipping initialization.")
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise click.ClickException(str(e))

@db_group.command()
@click.option('--message', '-m', help='Migration message')
def migrate(message: str):
    """Generate new migration."""
    try:
        alembic_cfg = Config('alembic.ini')
        command.revision(alembic_cfg, message=message, autogenerate=True)
        click.echo("Migration created successfully!")
    except Exception as e:
        logger.error(f"Error creating migration: {str(e)}")
        raise click.ClickException(str(e))

@db_group.command()
def upgrade():
    """Apply all pending migrations."""
    try:
        alembic_cfg = Config('alembic.ini')
        command.upgrade(alembic_cfg, 'head')
        click.echo("Database upgraded successfully!")
    except Exception as e:
        logger.error(f"Error upgrading database: {str(e)}")
        raise click.ClickException(str(e))

@db_group.command()
def downgrade():
    """Revert last migration."""
    try:
        alembic_cfg = Config('alembic.ini')
        command.downgrade(alembic_cfg, '-1')
        click.echo("Database downgraded successfully!")
    except Exception as e:
        logger.error(f"Error downgrading database: {str(e)}")
        raise click.ClickException(str(e))

@db_group.command()
def clear():
    """Clear all data from database but preserve schema."""
    async def _clear():
        async with get_session() as session:
            # Drop all tables except alembic_version
            async with session.begin():
                # Get all table names from PostgreSQL's information_schema
                result = await session.execute(text(
                    """
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    AND table_name != 'alembic_version'
                    """
                ))
                tables = [row[0] for row in result]
                
                # Truncate each table
                for table in tables:
                    await session.execute(text(f'TRUNCATE TABLE "{table}" CASCADE'))
            
            click.echo("Database data cleared successfully (schema preserved)")
    
    asyncio.run(_clear())
