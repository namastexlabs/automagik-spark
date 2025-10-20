"""Utility functions for consistent table styling across CLI commands."""

from rich.console import Console
from rich.table import Table
from rich import box
from typing import List, Dict, Any, Optional
from datetime import datetime


def create_rich_table(
    title: str,
    columns: List[Dict[str, Any]],
    caption: Optional[str] = None,
) -> Table:
    """Create a consistently styled Rich table.

    Args:
        title: Table title
        columns: List of column definitions with keys:
            - name: Column header text
            - justify: Text justification (left, center, right)
            - style: Color style for the column
            - no_wrap: Whether to prevent text wrapping
        caption: Optional caption text

    Returns:
        Rich Table object with consistent styling
    """
    table = Table(
        title=f"[bold blue]{title}[/bold blue]",
        caption=f"[dim]{caption}[/dim]" if caption else None,
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
        padding=(0, 1),
        width=None,  # Remove width constraint
    )

    for col in columns:
        table.add_column(
            col["name"],
            justify=col.get("justify", "left"),
            style=col.get("style", "white"),
            no_wrap=col.get("no_wrap", False),
            width=None,  # Remove width constraint
        )

    return table


def format_timestamp(dt: datetime) -> str:
    """Format a timestamp consistently."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_status_style(status: str) -> str:
    """Get consistent status styling."""
    status_styles = {
        "completed": "[bold green]✓[/bold green] COMPLETED",
        "failed": "[bold red]✗[/bold red] FAILED",
        "running": "[bold yellow]⟳[/bold yellow] RUNNING",
        "pending": "[bold blue]⋯[/bold blue] PENDING",
        "error": "[bold red]![/bold red] ERROR",
        "active": "[bold green]●[/bold green] ACTIVE",
        "inactive": "[bold red]○[/bold red] INACTIVE",
    }
    return status_styles.get(
        status.lower(), f"[bold white]{status.upper()}[/bold white]"
    )


def print_table(table: Table) -> None:
    """Print a table with consistent spacing."""
    console = Console()
    console.print()  # Add spacing before
    console.print(table)
    console.print()  # Add spacing after
