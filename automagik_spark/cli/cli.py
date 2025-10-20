"""Main CLI entry point."""

import click
import logging

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
    telemetry_group,
)


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--no-telemetry", is_flag=True, help="Disable telemetry for this session")
def main(debug, no_telemetry):
    """Automagik CLI."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # Handle telemetry
    if no_telemetry:
        import os

        os.environ["AUTOMAGIK_SPARK_DISABLE_TELEMETRY"] = "true"

    # Log telemetry status on CLI startup
    _log_telemetry_status()


def _log_telemetry_status():
    """Log telemetry status on startup."""
    from automagik_spark.core.telemetry import is_telemetry_enabled

    logger = logging.getLogger(__name__)

    if is_telemetry_enabled():
        logger.info("📊 Telemetry is ENABLED - helps us improve Automagik Spark")
        logger.info(
            "   • We collect anonymous usage analytics (commands, API usage, performance)"
        )
        logger.info(
            "   • No personal data, credentials, or workflow content is collected"
        )
        logger.info("   • Disable: export AUTOMAGIK_SPARK_DISABLE_TELEMETRY=true")
        logger.info("   • More info: automagik-spark telemetry info")
    else:
        logger.info("📊 Telemetry is DISABLED")


# Add command groups
main.add_command(api_group)
main.add_command(db_group)
main.add_command(worker_group)
main.add_command(workflow_group)
main.add_command(schedule_group)
main.add_command(task_group)
main.add_command(source_group)
main.add_command(telemetry_group)

if __name__ == "__main__":
    main()
