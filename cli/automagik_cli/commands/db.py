import click
from alembic.config import Config
from alembic import command
import os
import sys
from sqlalchemy import inspect
from core.database import get_db_session

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
        
        # Run all migrations, ignoring errors about existing tables
        try:
            command.upgrade(alembic_cfg, "head")
            click.echo("Database initialized successfully!")
        except Exception as e:
            if "already exists" in str(e):
                click.echo("Database is already initialized and up to date!")
            else:
                raise
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)
