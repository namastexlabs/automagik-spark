#!/usr/bin/env python3

import click
import asyncio
from dotenv import load_dotenv
import os
import sys
import pwd
import grp

from automagik.core.logger import get_logger
from automagik.cli.commands.flows import flows
from automagik.cli.commands.run import run
from automagik.cli.commands.tasks import tasks
from automagik.cli.commands.schedules import schedules
from automagik.cli.commands.db import db

# Add parent directory to Python path to find shared package
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

logger = get_logger(__name__)

# CLI Commands
@click.group()
def cli():
    """Automagik CLI"""
    pass

# Register commands
cli.add_command(flows)
cli.add_command(run)
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

def main():
    """Main entry point for the CLI."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(cli())
    finally:
        loop.close()

if __name__ == '__main__':
    main()