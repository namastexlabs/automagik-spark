#!/usr/bin/env python3

import click
from agents.cli import cli as agents_cli
from scheduler.cli import cli as scheduler_cli
from sync_flows.sync_flows import main as sync_flows_main
from executions.cli import cli as executions_cli

@click.group()
def cli():
    """AutoMagik CLI - Unified command-line interface for AutoMagik"""
    pass

# Add the existing CLIs as sub-commands
cli.add_command(agents_cli, "agents")
cli.add_command(scheduler_cli, "scheduler")
cli.add_command(executions_cli, "executions")

@cli.group()
def flows():
    """Manage Langflow flows"""
    pass

@flows.command()
def sync():
    """Sync flows from Langflow server"""
    sync_flows_main()

if __name__ == '__main__':
    cli() 