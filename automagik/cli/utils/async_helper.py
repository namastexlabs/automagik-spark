
"""Async helper functions for CLI commands."""

import asyncio
import click
import functools
import logging
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)


def handle_async_command(coro: Coroutine) -> Callable[..., Any]:
    """Handle async command in a sync context."""
    try:
        return asyncio.get_event_loop().run_until_complete(coro)
    except Exception as e:
        logger.error(f"Command failed: {str(e)}")
        raise click.ClickException(str(e))


