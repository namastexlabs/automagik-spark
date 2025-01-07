#!/usr/bin/env python3

import click
import os
import sys
import httpx
from typing import List, Dict, Any
import uuid
from dotenv import load_dotenv

# Add parent directory to Python path to find shared package
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from automagik_cli.commands.agents import agents
from .commands.schedules import schedules
from .commands.tasks import tasks
from .commands.run import run
from .commands.flows import flows
from .commands.test_setup import setup_test_tasks

# CLI Commands
@click.group()
def cli():
    """Automagik CLI"""
    pass

# Register commands
cli.add_command(agents)
cli.add_command(schedules)
cli.add_command(tasks)
cli.add_command(run)
cli.add_command(flows)
cli.add_command(setup_test_tasks, name='setup-test-tasks')

if __name__ == '__main__':
    cli() 