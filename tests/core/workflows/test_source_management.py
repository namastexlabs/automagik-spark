"""Tests for workflow source management functionality."""

import json
import pytest
from uuid import uuid4
from typing import AsyncGenerator
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from automagik.core.database.models import WorkflowSource, Workflow
from automagik.core.workflows.source import WorkflowSource as WorkflowSourceModel
from automagik.core.workflows.manager import WorkflowManager

@pytest.fixture(autouse=True)
async def cleanup_database(session: AsyncSession):
    """Clean up the database before each test."""
    await session.execute(delete(Workflow))
    await session.execute(delete(WorkflowSource))
    await session.commit()

@pytest.fixture
async def workflow_source(session: AsyncSession) -> AsyncGenerator[WorkflowSource, None]:
    """Create a test workflow source."""
    source = WorkflowSource(
        source_type="langflow",
        url="http://test-langflow:7860",
        encrypted_api_key=WorkflowSourceModel.encrypt_api_key("test-api-key"),
        version_info={"version": "1.1.1", "main_version": "1.1.1", "package": "Langflow"},
        status="active"
    )
    session.add(source)
    await session.commit()
    yield source
    try:
        # Delete source if it exists
        source = await session.get(WorkflowSource, source.id)
        if source:
            await session.delete(source)
            await session.commit()
    except Exception:
        # If there's an error (like a rollback), try to rollback and continue
        await session.rollback()

@pytest.fixture
async def workflow_with_source(session: AsyncSession, workflow_source: WorkflowSource) -> AsyncGenerator[Workflow, None]:
    """Create a test workflow with an associated source."""
    workflow = Workflow(
        id=uuid4(),
        name="Test Workflow",
        description="A test workflow",
        source="langflow",
        remote_flow_id=str(uuid4()),
        workflow_source=workflow_source
    )
    session.add(workflow)
    await session.commit()
    yield workflow
    await session.delete(workflow)
    await session.commit()

async def test_create_workflow_source(session: AsyncSession):
    """Test creating a workflow source."""
    source = WorkflowSource(
        source_type="langflow",
        url="http://test-langflow:7860",
        encrypted_api_key=WorkflowSourceModel.encrypt_api_key("test-api-key"),
        version_info={"version": "1.1.1"},
        status="active"
    )
    session.add(source)
    await session.commit()

    # Verify source was created
    result = await session.execute(select(WorkflowSource))
    sources = result.scalars().all()
    assert len(sources) == 1
    assert sources[0].url == "http://test-langflow:7860"
    assert sources[0].source_type == "langflow"
    assert sources[0].status == "active"

    # Verify API key encryption
    decrypted_key = WorkflowSourceModel.decrypt_api_key(sources[0].encrypted_api_key)
    assert decrypted_key == "test-api-key"

async def test_workflow_source_relationship(session: AsyncSession, workflow_with_source: Workflow):
    """Test the relationship between workflows and sources."""
    # Verify workflow has source
    workflow = await session.get(Workflow, workflow_with_source.id)
    assert workflow.workflow_source is not None
    assert workflow.workflow_source.url == "http://test-langflow:7860"

    # Verify source has workflow using select to properly load relationships
    stmt = select(WorkflowSource).where(WorkflowSource.id == workflow.workflow_source.id)
    result = await session.execute(stmt)
    source = result.scalar_one()
    workflows = await session.execute(select(Workflow).where(Workflow.workflow_source_id == source.id))
    workflows = workflows.scalars().all()
    assert len(workflows) == 1
    assert workflows[0].id == workflow.id

async def test_workflow_manager_source_handling(session: AsyncSession, workflow_with_source: Workflow):
    """Test that WorkflowManager properly handles workflow sources."""
    manager = WorkflowManager(session)

    # Get LangFlowManager for workflow
    langflow = await manager._get_langflow_manager(str(workflow_with_source.id))
    assert langflow.api_url == "http://test-langflow:7860"
    
    # The API key should be decrypted
    decrypted_key = WorkflowSourceModel.decrypt_api_key(workflow_with_source.workflow_source.encrypted_api_key)
    assert langflow.api_key == decrypted_key

    # Test fallback to environment variables
    langflow = await manager._get_langflow_manager()
    assert langflow.api_url != "http://test-langflow:7860"  # Should use env var

async def test_delete_workflow_source(session: AsyncSession, workflow_with_source: Workflow):
    """Test deleting a workflow source."""
    source_id = workflow_with_source.workflow_source.id
    
    # Delete source
    source = await session.get(WorkflowSource, source_id)
    if source:  # Only delete if it exists
        await session.delete(source)
        await session.commit()
    
    # Verify source is deleted
    source = await session.get(WorkflowSource, source_id)
    assert source is None
    
    # Verify workflow still exists but has no source
    workflow = await session.get(Workflow, workflow_with_source.id)
    assert workflow is not None
    assert workflow.workflow_source_id is None

async def test_update_workflow_source(session: AsyncSession, workflow_source: WorkflowSource):
    """Test updating a workflow source."""
    # Update source
    source = await session.get(WorkflowSource, workflow_source.id)
    source.status = "inactive"
    source.encrypted_api_key = WorkflowSourceModel.encrypt_api_key("new-api-key")
    await session.commit()
    
    # Verify changes
    source = await session.get(WorkflowSource, workflow_source.id)
    assert source.status == "inactive"
    decrypted_key = WorkflowSourceModel.decrypt_api_key(source.encrypted_api_key)
    assert decrypted_key == "new-api-key"

async def test_unique_url_constraint(session: AsyncSession, workflow_source: WorkflowSource):
    """Test that workflow sources must have unique URLs."""
    # Try to create another source with the same URL
    with pytest.raises(Exception):  # SQLAlchemy will raise an IntegrityError
        source = WorkflowSource(
            source_type="langflow",
            url=workflow_source.url,  # Same URL as existing source
            encrypted_api_key=WorkflowSourceModel.encrypt_api_key("another-key"),
            status="active"
        )
        session.add(source)
        await session.commit()
