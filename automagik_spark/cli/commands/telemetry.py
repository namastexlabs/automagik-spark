"""Telemetry management commands."""

import click
from automagik_spark.core.telemetry import (
    disable_telemetry,
    enable_telemetry,
    get_telemetry_client,
)


@click.group()
def telemetry_group():
    """Manage telemetry settings."""
    pass


@telemetry_group.command("status")
def status():
    """Show telemetry status."""
    client = get_telemetry_client()

    if client.enabled:
        click.echo("✅ Telemetry is ENABLED")
        click.echo(f"   User ID: {client.user_id}")
        click.echo(f"   Session ID: {client.session_id}")
        click.echo(f"   Endpoint: {client.endpoint}")
    else:
        click.echo("❌ Telemetry is DISABLED")

    click.echo("\nHow to disable:")
    click.echo("  • Set environment variable: AUTOMAGIK_SPARK_DISABLE_TELEMETRY=true")
    click.echo("  • Create opt-out file: ~/.automagik-no-telemetry")
    click.echo("  • Use CLI flag: --no-telemetry")
    click.echo("  • Run command: automagik-spark telemetry disable")


@telemetry_group.command("disable")
def disable():
    """Disable telemetry permanently."""
    disable_telemetry()


@telemetry_group.command("enable")
def enable():
    """Enable telemetry."""
    enable_telemetry()


@telemetry_group.command("info")
def info():
    """Show what data is collected."""
    click.echo("📊 Automagik Spark Telemetry Information")
    click.echo("=" * 40)

    click.echo("\n🔍 Data We Collect:")
    click.echo("  • Command usage (which CLI commands you run)")
    click.echo("  • API endpoint usage")
    click.echo("  • Workflow execution metrics")
    click.echo("  • Feature usage patterns")
    click.echo("  • Error rates and types")
    click.echo("  • Performance metrics (response times)")
    click.echo("  • System information (OS, Python version)")

    click.echo("\n🚫 Data We DON'T Collect:")
    click.echo("  • Your actual data or workflow content")
    click.echo("  • Personal information")
    click.echo("  • File paths or names")
    click.echo("  • Environment variables")
    click.echo("  • Database connection strings")

    click.echo("\n🎯 Why We Collect This:")
    click.echo("  • Understand which features are most useful")
    click.echo("  • Identify performance bottlenecks")
    click.echo("  • Prioritize development efforts")
    click.echo("  • Improve documentation and user experience")

    click.echo("\n🔒 Privacy:")
    click.echo("  • All data is anonymous (random user ID)")
    click.echo("  • No personal information is collected")
    click.echo("  • Data is used only for product improvement")
    click.echo("  • You can opt-out at any time")

    click.echo("\n💡 How to Opt-Out:")
    click.echo("  • Run: automagik-spark telemetry disable")
    click.echo("  • Set: AUTOMAGIK_SPARK_DISABLE_TELEMETRY=true")
    click.echo("  • Create: ~/.automagik-no-telemetry file")
    click.echo("  • Use: --no-telemetry flag")
