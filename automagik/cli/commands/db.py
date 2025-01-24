import click
from alembic.config import Config
from alembic import command
import os
import sys
from sqlalchemy import inspect
from automagik.core.database.session import engine

@click.group()
def db():
    """Database management commands"""
    pass

@db.command()
@click.option('--force', is_flag=True, help='Force reinitialization even if tables exist')
def init(force):
    """Initialize the database with all tables"""
    try:
        # Get the absolute path to alembic.ini in root directory
        alembic_ini = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'alembic.ini')
        
        if not os.path.exists(alembic_ini):
            click.echo(f"Error: Could not find alembic.ini at {alembic_ini}")
            sys.exit(1)

        # Check if tables already exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        required_tables = ['flow_components', 'flows', 'tasks', 'logs', 'schedules']
        tables_exist = all(table in existing_tables for table in required_tables)

        if tables_exist and not force:
            click.echo("Database is already initialized! Use --force to reinitialize if needed.")
            sys.exit(0)
            
        # Create Alembic configuration
        alembic_cfg = Config(alembic_ini)
        
        try:
            # Run all migrations
            command.upgrade(alembic_cfg, "head")
            click.echo("Database initialized successfully!")
        except Exception as e:
            if 'already exists' in str(e) and not force:
                click.echo("Database is already initialized! Use --force to reinitialize if needed.")
                sys.exit(0)
            else:
                raise e
                
    except Exception as e:
        click.echo(f"Error initializing database: {str(e)}")
        sys.exit(1)
