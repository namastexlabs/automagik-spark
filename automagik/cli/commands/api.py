import click
import uvicorn

@click.command()
@click.option('--host', default="0.0.0.0", help='Host to bind the API server')
@click.option('--port', default=8000, help='Port to bind the API server')
@click.option('--reload', is_flag=True, help='Enable auto-reload for development')
def api(host: str, port: int, reload: bool):
    """Start the AutoMagik API server"""
    uvicorn.run(
        "automagik.api.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
