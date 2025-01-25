"""
Main CLI Entry Point

Provides the main entry point for the Automagik CLI.
"""

import click
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from .commands import flow_group, schedule_group, task_group, db_group, worker

# Load environment variables from .env file
env_path = Path(os.getcwd()) / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)

@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(debug: bool):
    """Automagik CLI - Manage and automate LangFlow workflows."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

# Add command groups
main.add_command(flow_group)
main.add_command(schedule_group)
main.add_command(worker)
main.add_command(task_group)
main.add_command(db_group)

if __name__ == '__main__':
    main()
