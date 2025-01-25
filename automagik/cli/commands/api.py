import click
import uvicorn
from automagik.api.config import get_api_host, get_api_port

@click.command()
@click.option('--host', default=None, help='Host to bind the API server (overrides AUTOMAGIK_HOST)')
@click.option('--port', default=None, type=int, help='Port to bind the API server (overrides AUTOMAGIK_PORT)')
@click.option('--reload', is_flag=True, help='Enable auto-reload for development')
def api(host: str | None, port: int | None, reload: bool):
    """Start the AutoMagik API server"""
    uvicorn.run(
        "automagik.api.app:app",
        host=host or get_api_host(),
        port=port or get_api_port(),
        reload=reload,
        log_level="info"
    )
