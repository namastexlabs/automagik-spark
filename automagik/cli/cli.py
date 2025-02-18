
"""Main CLI entry point."""

import click
import logging
import os

from dotenv import load_dotenv

load_dotenv()

from .commands import (
    api_group,
    db_group,
    worker_group,
    workflow_group,
    schedule_group,
    task_group,
    source_group,
)


@click.group()
@click.option("--debug/--no-debug", default=False)
def main(debug):
    """Automagik CLI."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

# Add command groups
main.add_command(api_group)
main.add_command(db_group)
main.add_command(worker_group)
main.add_command(workflow_group)
main.add_command(schedule_group)
main.add_command(task_group)
main.add_command(source_group)

if __name__ == "__main__":
    main()


