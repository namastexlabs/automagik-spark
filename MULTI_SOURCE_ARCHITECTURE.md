# Multi-Source Workflow Architecture - Hybrid Approach

## Executive Summary

Design a flexible, extensible architecture for Spark to support multiple workflow sources (LangFlow, Hive, n8n, Make, etc.) using the **Adapter Pattern** with **Strategy Pattern** for execution.

## Current State Analysis

### ✅ What Works Well

1. **WorkflowSource Model** - Already stores multiple source types
2. **SourceType Enum** - Defines source types (LANGFLOW, AUTOMAGIK_AGENTS, AUTOMAGIK_HIVE)
3. **Manager Factory** - `_get_source_manager()` returns appropriate manager
4. **Separate Managers** - Each source has dedicated manager (LangFlowManager, AutomagikHiveManager, etc.)

### ❌ Current Problems

1. **Hard-coded if/elif chains** - Not scalable for new sources
2. **Inconsistent response formats** - Each manager returns different structure
3. **Source-specific parameters** - Sync endpoint requires LangFlow's `input_component`/`output_component`
4. **No unified interface** - Each manager has different method signatures
5. **Duplicate logic** - Sync/async code duplicated for each source

## Proposed Architecture

### 1. Base Workflow Adapter (Abstract Interface)

Create a unified adapter interface that all source-specific adapters implement:

```python
# automagik_spark/core/workflows/adapters/base.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class WorkflowExecutionResult:
    """Unified result format across all workflow sources."""
    success: bool
    result: Any  # The actual response content
    session_id: Optional[str] = None
    run_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class WorkflowSyncParams:
    """Parameters for syncing a workflow."""
    flow_id: str
    source_url: str
    # Optional source-specific parameters
    input_component: Optional[str] = None
    output_component: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None

class BaseWorkflowAdapter(ABC):
    """Abstract base adapter for workflow sources."""

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return the source type identifier."""
        pass

    @abstractmethod
    async def list_flows(self) -> List[Dict[str, Any]]:
        """List available flows from this source."""
        pass

    @abstractmethod
    async def get_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific flow by ID."""
        pass

    @abstractmethod
    async def execute_flow(
        self,
        flow_id: str,
        input_data: Any,
        session_id: Optional[str] = None
    ) -> WorkflowExecutionResult:
        """Execute a flow and return normalized result."""
        pass

    @abstractmethod
    async def validate_connection(self) -> Dict[str, Any]:
        """Validate connection to the source."""
        pass

    def get_default_sync_params(self, flow_data: Dict[str, Any]) -> Dict[str, str]:
        """Get default parameters for syncing this flow type.

        Override this for source-specific defaults.
        """
        return {
            "input_component": "message",
            "output_component": "result"
        }

    def normalize_flow_data(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize flow data to common format.

        Override this for source-specific transformations.
        """
        return flow_data
```

### 2. Source-Specific Adapters

Implement adapters for each source:

```python
# automagik_spark/core/workflows/adapters/langflow_adapter.py

from .base import BaseWorkflowAdapter, WorkflowExecutionResult
from ..remote import LangFlowManager

class LangFlowAdapter(BaseWorkflowAdapter):
    """Adapter for LangFlow workflows."""

    def __init__(self, api_url: str, api_key: str, source_id: Optional[UUID] = None):
        self.manager = LangFlowManager(api_url=api_url, api_key=api_key)
        self.source_id = source_id

    @property
    def source_type(self) -> str:
        return "langflow"

    async def list_flows(self) -> List[Dict[str, Any]]:
        return self.manager.list_flows_sync()

    async def get_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        return self.manager.get_flow_sync(flow_id)

    async def execute_flow(
        self,
        flow_id: str,
        input_data: Any,
        session_id: Optional[str] = None
    ) -> WorkflowExecutionResult:
        try:
            result = await self.manager.run_flow(flow_id, input_data)
            return WorkflowExecutionResult(
                success=True,
                result=result,
                session_id=session_id
            )
        except Exception as e:
            return WorkflowExecutionResult(
                success=False,
                result=None,
                error=str(e)
            )

    async def validate_connection(self) -> Dict[str, Any]:
        # LangFlow validation logic
        return await self.manager.validate()

    def get_default_sync_params(self, flow_data: Dict[str, Any]) -> Dict[str, str]:
        """LangFlow requires explicit input/output components."""
        # Try to auto-detect from flow data
        nodes = flow_data.get('data', {}).get('nodes', [])
        input_node = next((n for n in nodes if n.get('data', {}).get('type') == 'ChatInput'), None)
        output_node = next((n for n in nodes if n.get('data', {}).get('type') == 'ChatOutput'), None)

        return {
            "input_component": input_node['id'] if input_node else None,
            "output_component": output_node['id'] if output_node else None
        }


# automagik_spark/core/workflows/adapters/hive_adapter.py

from .base import BaseWorkflowAdapter, WorkflowExecutionResult
from ..automagik_hive import AutomagikHiveManager

class HiveAdapter(BaseWorkflowAdapter):
    """Adapter for AutoMagik Hive workflows."""

    def __init__(self, api_url: str, api_key: str, source_id: Optional[UUID] = None):
        self.manager = AutomagikHiveManager(api_url=api_url, api_key=api_key, source_id=source_id)
        self.source_id = source_id

    @property
    def source_type(self) -> str:
        return "automagik-hive"

    async def list_flows(self) -> List[Dict[str, Any]]:
        return self.manager.list_flows_sync()

    async def get_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        return self.manager.get_flow_sync(flow_id)

    async def execute_flow(
        self,
        flow_id: str,
        input_data: Any,
        session_id: Optional[str] = None
    ) -> WorkflowExecutionResult:
        try:
            result = self.manager.run_flow_sync(flow_id, input_data, session_id)
            return WorkflowExecutionResult(
                success=result.get('success', True),
                result=result.get('result'),
                session_id=result.get('session_id'),
                run_id=result.get('run_id'),
                metadata={
                    'agent_id': result.get('agent_id'),
                    'team_id': result.get('team_id'),
                    'workflow_id': result.get('workflow_id'),
                    'status': result.get('status')
                }
            )
        except Exception as e:
            return WorkflowExecutionResult(
                success=False,
                result=None,
                error=str(e)
            )

    async def validate_connection(self) -> Dict[str, Any]:
        return await self.manager.validate()

    def get_default_sync_params(self, flow_data: Dict[str, Any]) -> Dict[str, str]:
        """Hive doesn't need component IDs - uses message/result convention."""
        return {
            "input_component": "message",
            "output_component": "result"
        }

    def normalize_flow_data(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add Hive-specific metadata."""
        flow_data['flow_type'] = flow_data.get('data', {}).get('type', 'unknown')
        return flow_data
```

### 3. Adapter Factory & Registry

Central registry for managing adapters:

```python
# automagik_spark/core/workflows/adapters/factory.py

from typing import Dict, Type, Optional
from uuid import UUID
from .base import BaseWorkflowAdapter
from .langflow_adapter import LangFlowAdapter
from .hive_adapter import HiveAdapter
from .agents_adapter import AgentsAdapter
from ...schemas.source import SourceType

class AdapterRegistry:
    """Registry for workflow adapters."""

    _adapters: Dict[str, Type[BaseWorkflowAdapter]] = {}

    @classmethod
    def register(cls, source_type: str, adapter_class: Type[BaseWorkflowAdapter]):
        """Register an adapter for a source type."""
        cls._adapters[source_type] = adapter_class

    @classmethod
    def get_adapter(
        cls,
        source_type: str,
        api_url: str,
        api_key: str,
        source_id: Optional[UUID] = None
    ) -> BaseWorkflowAdapter:
        """Get an adapter instance for the given source type."""
        adapter_class = cls._adapters.get(source_type)
        if not adapter_class:
            raise ValueError(f"No adapter registered for source type: {source_type}")
        return adapter_class(api_url=api_url, api_key=api_key, source_id=source_id)

    @classmethod
    def list_supported_types(cls) -> List[str]:
        """List all registered source types."""
        return list(cls._adapters.keys())

# Register built-in adapters
AdapterRegistry.register(SourceType.LANGFLOW, LangFlowAdapter)
AdapterRegistry.register(SourceType.AUTOMAGIK_HIVE, HiveAdapter)
AdapterRegistry.register(SourceType.AUTOMAGIK_AGENTS, AgentsAdapter)

# Future sources can be easily added:
# AdapterRegistry.register("n8n", N8NAdapter)
# AdapterRegistry.register("make", MakeAdapter)
```

### 4. Updated WorkflowManager

Simplified manager using adapters:

```python
# automagik_spark/core/workflows/manager.py (updated)

class WorkflowManager:
    """Workflow management class using adapter pattern."""

    async def _get_adapter(self, source: WorkflowSource) -> BaseWorkflowAdapter:
        """Get the appropriate adapter for a source."""
        api_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)
        return AdapterRegistry.get_adapter(
            source_type=source.source_type,
            api_url=source.url,
            api_key=api_key,
            source_id=source.id
        )

    async def sync_flow(
        self,
        flow_id: str,
        source_url: str,
        input_component: Optional[str] = None,
        output_component: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Sync a flow from any source - parameters now optional!"""
        # Get source
        source = await self._get_source_by_url(source_url)
        if not source:
            raise ValueError(f"No source found: {source_url}")

        # Get adapter
        adapter = await self._get_adapter(source)

        # Get flow data
        flow_data = await adapter.get_flow(flow_id)
        if not flow_data:
            raise ValueError(f"Flow {flow_id} not found")

        # Use provided params or get defaults from adapter
        if not input_component or not output_component:
            defaults = adapter.get_default_sync_params(flow_data)
            input_component = input_component or defaults.get("input_component")
            output_component = output_component or defaults.get("output_component")

        # Normalize flow data
        flow_data = adapter.normalize_flow_data(flow_data)
        flow_data['input_component'] = input_component
        flow_data['output_component'] = output_component

        # Create/update workflow
        return await self._create_or_update_workflow(flow_data, source)

    async def run_workflow(
        self,
        workflow_id: str | UUID,
        input_data: str,
        existing_task: Optional[Task] = None
    ) -> Optional[Task]:
        """Run a workflow using appropriate adapter."""
        workflow = await self.get_workflow(str(workflow_id))
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        # Create or use existing task
        task = existing_task or Task(
            id=uuid4(),
            workflow_id=workflow.id,
            input_data=input_data,
            status="running",
            started_at=datetime.now(timezone.utc)
        )

        if not existing_task:
            self.session.add(task)
            await self.session.commit()

        try:
            # Get adapter for this workflow's source
            adapter = await self._get_adapter(workflow.workflow_source)

            # Execute using adapter
            result = await adapter.execute_flow(
                flow_id=workflow.remote_flow_id,
                input_data=input_data,
                session_id=str(task.id)
            )

            # Update task with normalized result
            if result.success:
                task.output_data = json.dumps(result.result) if isinstance(result.result, (dict, list)) else str(result.result)
                task.status = 'completed'
            else:
                task.status = 'failed'
                task.error = result.error

            task.finished_at = datetime.now(timezone.utc)

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            task.status = 'failed'
            task.error = str(e)
            task.finished_at = datetime.now(timezone.utc)

        await self.session.commit()
        return task
```

### 5. Updated API Endpoint

```python
# automagik_spark/api/routers/workflows.py (updated)

@router.post("/sync/{flow_id}", dependencies=[Depends(verify_api_key)])
async def sync_flow(
    flow_id: str,
    source_url: str,  # Required via query param
    input_component: Optional[str] = None,  # Now optional!
    output_component: Optional[str] = None,  # Now optional!
    workflow_manager: WorkflowManager = Depends(get_workflow_manager)
) -> Dict[str, Any]:
    """Sync a flow from any source.

    input_component and output_component are optional - will use source-specific defaults if not provided.
    """
    workflow_data = await workflow_manager.sync_flow(
        flow_id=flow_id,
        source_url=source_url,
        input_component=input_component,
        output_component=output_component
    )
    if not workflow_data:
        raise HTTPException(status_code=404, detail="Flow not found")
    return workflow_data
```

## Benefits of This Architecture

### ✅ Extensibility
- Add new sources by creating adapter + registration (2 files)
- No changes to core WorkflowManager needed
- No if/elif chains to maintain

### ✅ Consistency
- Unified `WorkflowExecutionResult` across all sources
- Consistent error handling
- Standardized response format

### ✅ Flexibility
- Source-specific defaults via `get_default_sync_params()`
- Custom normalization via `normalize_flow_data()`
- Optional parameters with smart defaults

### ✅ Testability
- Mock adapters for testing
- Test each adapter independently
- No tight coupling to specific implementations

### ✅ Maintainability
- Clear separation of concerns
- Single Responsibility Principle
- Easy to understand and modify

## Database Schema (Current - No Changes Needed!)

The current schema already supports this:

```python
class Workflow:
    source = Column(String(50))  # "langflow", "automagik-hive", etc.
    workflow_source_id = Column(UUID, ForeignKey("workflow_sources.id"))
    # ... rest of fields

class WorkflowSource:
    source_type = Column(String(50))  # Used to select adapter
    url = Column(String(255))
    encrypted_api_key = Column(String)
```

## Migration Path

### Phase 1: Create Adapter Infrastructure ✅
- [ ] Create `adapters/` directory structure
- [ ] Implement `BaseWorkflowAdapter`
- [ ] Implement `AdapterRegistry`
- [ ] Implement `WorkflowExecutionResult`

### Phase 2: Migrate Existing Sources ✅
- [ ] Create `LangFlowAdapter`
- [ ] Create `HiveAdapter`
- [ ] Create `AgentsAdapter`
- [ ] Register all adapters

### Phase 3: Update Core System ✅
- [ ] Update `WorkflowManager._get_adapter()`
- [ ] Update `WorkflowManager.sync_flow()`
- [ ] Update `WorkflowManager.run_workflow()`
- [ ] Update API endpoints

### Phase 4: Testing & Validation ✅
- [ ] Unit tests for each adapter
- [ ] Integration tests for workflow sync
- [ ] Integration tests for workflow execution
- [ ] Update existing tests

### Phase 5: Future Sources 🚀
- [ ] n8n adapter (when needed)
- [ ] Make adapter (when needed)
- [ ] Zapier adapter (when needed)
- [ ] Custom webhook adapter

## Adding New Sources (Future)

Example for n8n:

```python
# 1. Create adapter
class N8NAdapter(BaseWorkflowAdapter):
    def __init__(self, api_url, api_key, source_id=None):
        self.manager = N8NManager(api_url, api_key)

    @property
    def source_type(self) -> str:
        return "n8n"

    # Implement required methods...

# 2. Register it
AdapterRegistry.register("n8n", N8NAdapter)

# 3. Add to SourceType enum
class SourceType:
    N8N = "n8n"

# Done! No other changes needed.
```

## Conclusion

This hybrid approach:
- ✅ Preserves existing functionality
- ✅ Adds extensibility for future sources
- ✅ Simplifies maintenance
- ✅ Provides consistent interface
- ✅ Requires minimal database changes
- ✅ Enables optional parameters for sync
- ✅ Standardizes execution results

**Next Steps**: Approve architecture → Implement Phase 1 → Test with Hive → Complete migration
