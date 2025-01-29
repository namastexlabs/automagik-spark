"""CLI entry point for automagik."""

import os
import click
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .commands import (
    flow_group,
    schedule_group,
    task_group,
    db_group,
    worker_group,
    api
)

@click.group()
@click.option('--debug/--no-debug', default=False, help='Enable debug mode')
def main(debug):
    """AutoMagik CLI"""
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.getLogger().setLevel(logging.INFO)

# Add command groups
main.add_command(flow_group)
main.add_command(schedule_group)
main.add_command(worker_group)
main.add_command(task_group)
main.add_command(db_group)
main.add_command(api)

if __name__ == '__main__':
    main()
