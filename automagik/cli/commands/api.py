"""API server command."""

import click
import uvicorn
from automagik.api.config import get_api_host, get_api_port

api_group = click.Group(name="api", help="API server commands")


@api_group.command("start")
@click.option("--host", default=get_api_host(), help="Host to bind to (overrides AUTOMAGIK_HOST)")
@click.option("--port", default=get_api_port(), help="Port to bind to (overrides AUTOMAGIK_PORT)")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def start_api(host: str, port: int, reload: bool):
    """Start the API server."""
    uvicorn.run(
        "automagik.api.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
