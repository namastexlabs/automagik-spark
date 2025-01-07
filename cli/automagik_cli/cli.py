#!/usr/bin/env python3

import click
import os
import sys
from typing import List, Dict, Any
import uuid
from dotenv import load_dotenv
from .commands.run import run
from .commands.tasks import tasks
from .commands.schedule import schedule
from .commands.flows import flows
from .logger import setup_logger
import logging
import pkg_resources
from pathlib import Path
import subprocess
import shutil

# Add parent directory to Python path to find shared package
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

def set_log_level(ctx, param, value):
    if value:
        logger = setup_logger(level=value.upper())
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
cli.add_command(tasks)
cli.add_command(schedule)
cli.add_command(flows)

@cli.command()
def install_service():
    """Install AutoMagik as a system service"""
    try:
        # Get current user
        user = os.getenv('USER')
        if not user:
            click.echo("Error: Could not determine current user", err=True)
            return

        # Get virtual environment path
        venv_path = os.path.dirname(os.path.dirname(sys.executable))
        if not os.path.exists(os.path.join(venv_path, 'bin', 'python')):
            click.echo("Error: Not running in a valid virtual environment", err=True)
            return

        # Get template path
        template_path = pkg_resources.resource_filename('automagik_cli', 'templates/automagik.service')
        if not os.path.exists(template_path):
            click.echo("Error: Service template not found", err=True)
            return

        # Read template
        with open(template_path, 'r') as f:
            service_content = f.read()

        # Get project root directory (where .env is located)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Replace placeholders
        service_content = service_content.replace('%USER%', user)
        service_content = service_content.replace('%WORKDIR%', project_root)
        service_content = service_content.replace('%VENV_PATH%', venv_path)

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
        subprocess.run(['sudo', 'chmod', '644', systemd_path])

        # Reload systemd
        result = subprocess.run(['sudo', 'systemctl', 'daemon-reload'], capture_output=True, text=True)
        if result.returncode != 0:
            click.echo(f"Error reloading systemd: {result.stderr}", err=True)
            return

        click.echo("Service installed successfully!")
        click.echo("\nTo start the service:")
        click.echo("  sudo systemctl start automagik")
        click.echo("\nTo enable service on boot:")
        click.echo("  sudo systemctl enable automagik")
        click.echo("\nTo check service status:")
        click.echo("  sudo systemctl status automagik")
        click.echo("\nTo view logs:")
        click.echo("  journalctl -u automagik -f")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli() 