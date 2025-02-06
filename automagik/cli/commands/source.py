"""CLI commands for managing workflow sources."""

import json
import click
import httpx
from typing import Optional
from sqlalchemy import select

from ...core.database.session import get_session
from ...core.workflows.source import WorkflowSource

@click.group()
def source():
    """Manage workflow sources."""
    pass

@source.command()
@click.option("--type", "-t", required=True, help="Source type (e.g., langflow)")
@click.option("--url", "-u", required=True, help="Source URL")
@click.option("--api-key", "-k", required=True, help="API key for authentication")
@click.option("--status", "-s", default="active", help="Source status (active/inactive)")
async def add(type: str, url: str, api_key: str, status: str):
    """Add a new workflow source."""
    async with get_session() as session:
        # Check if source with URL already exists
        result = await session.execute(
            select(WorkflowSource).where(WorkflowSource.url == url)
        )
        existing = result.scalar_one_or_none()
        if existing:
            click.echo(f"Source with URL {url} already exists. Updating instead...")
            existing.source_type = type
            existing.encrypted_api_key = WorkflowSource.encrypt_api_key(api_key)
            existing.status = status
            source = existing
        else:
            # Create new source
            source = WorkflowSource(
                source_type=type,
                url=url,
                encrypted_api_key=WorkflowSource.encrypt_api_key(api_key),
                status=status
            )
            session.add(source)

        # Validate source by fetching version info
        try:
            async with httpx.AsyncClient(verify=False) as client:
                headers = {"accept": "application/json"}
                if api_key:
                    headers["x-api-key"] = api_key
                response = await client.get(f"{url}/api/v1/version", headers=headers)
                response.raise_for_status()
                source.version_info = response.json()
        except Exception as e:
            click.echo(f"Warning: Failed to fetch version info: {str(e)}")

        await session.commit()
        click.echo(f"Successfully {'updated' if existing else 'added'} source: {url}")

@source.command()
@click.argument("url")
async def remove(url: str):
    """Remove a workflow source."""
    async with get_session() as session:
        result = await session.execute(
            select(WorkflowSource).where(WorkflowSource.url == url)
        )
        source = result.scalar_one_or_none()
        if not source:
            click.echo(f"Source not found: {url}")
            return
        
        await session.delete(source)
        await session.commit()
        click.echo(f"Successfully removed source: {url}")

@source.command()
@click.option("--status", "-s", help="Filter by status (active/inactive)")
async def list(status: Optional[str] = None):
    """List workflow sources."""
    async with get_session() as session:
        query = select(WorkflowSource)
        if status:
            query = query.where(WorkflowSource.status == status)
        
        result = await session.execute(query)
        sources = result.scalars().all()
        
        if not sources:
            click.echo("No sources found.")
            return
        
        for source in sources:
            version = json.dumps(source.version_info) if source.version_info else "N/A"
            click.echo(f"URL: {source.url}")
            click.echo(f"Type: {source.source_type}")
            click.echo(f"Status: {source.status}")
            click.echo(f"Version: {version}")
            click.echo("---")

@source.command()
@click.argument("url")
@click.option("--status", "-s", help="New status (active/inactive)")
@click.option("--api-key", "-k", help="New API key")
async def update(url: str, status: Optional[str] = None, api_key: Optional[str] = None):
    """Update a workflow source."""
    async with get_session() as session:
        result = await session.execute(
            select(WorkflowSource).where(WorkflowSource.url == url)
        )
        source = result.scalar_one_or_none()
        if not source:
            click.echo(f"Source not found: {url}")
            return
        
        if status:
            source.status = status
        if api_key:
            source.encrypted_api_key = WorkflowSource.encrypt_api_key(api_key)
            
            # Validate new API key by fetching version info
            try:
                async with httpx.AsyncClient(verify=False) as client:
                    headers = {"accept": "application/json", "x-api-key": api_key}
                    response = await client.get(f"{url}/api/v1/version", headers=headers)
                    response.raise_for_status()
                    source.version_info = response.json()
            except Exception as e:
                click.echo(f"Warning: Failed to fetch version info with new API key: {str(e)}")
        
        await session.commit()
        click.echo(f"Successfully updated source: {url}")
