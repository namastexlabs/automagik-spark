## Workflow Source Management

### Overview
The goal is to introduce multi-source support for workflows. Instead of relying solely on environment variables for LangFlow configuration, users can now define workflow source configurations (initially for LangFlow) via API, CLI, or other integrations. This will manage multiple instances of LangFlow and, in the future, additional source types.

### Required Changes

#### 1. Workflow Source Model
- Create a new database table/model `WorkflowSource` with the following fields:
  - `id`: Primary key (UUID).
  - `source_type`: Type of the source (e.g., "langflow").
  - `url`: The unique URL of the workflow source (unique identifier).
  - `encrypted_api_key`: Securely stored API key which must be encrypted using reversible encryption (e.g., using Fernet from the cryptography library).
  - `version_info`: JSON or structured data to store information from the `/api/v1/version` endpoint (e.g., version, main_version, package).
  - `status`: Reflection of whether the source is active or inactive.
  - Timestamps for creation and last update.

*Encryption Note*: Use an encryption key from application settings/environment to encrypt and decrypt API keys. This is essential since the repository is public.

#### 2. Workflow & Source Relationship
- Update the workflow model (in `automagik/core/workflows/workflow.py`) to include a foreign key referencing `WorkflowSource`.
- Each workflow must be associated with exactly one source, which provides:
  - Base URL for API calls
  - API key for authentication
  - Version and connection information

#### 3. Remote Manager & Workflow Manager Updates
- **LangFlowManager Updates**:
  - Modify the constructor to accept optional parameters (URL, API key). 
  - Instantiate the manager with source-specific settings if a workflow has an associated source; otherwise, fall back to the default configuration from environment variables.

- **WorkflowManager Updates**:
  - In methods like `run_workflow`, check for an associated workflow source. If present:
    - Retrieve and decrypt the API key from the `WorkflowSource` model.
    - Instantiate `LangFlowManager` with the source’s URL and decrypted API key.
  - Maintain existing behavior as a fallback if no source is defined.

#### 4. API / CLI Endpoints for Source Management
- Develop endpoints and CLI commands to:
  - Create or update a workflow source. When a source with an existing URL is provided, update the record instead of creating a duplicate.
  - List and delete workflow sources.
  - Validate source credentials by fetching data from the `/api/v1/version` endpoint.

*Validation Example*:
```
curl -H "Authorization: Bearer <API_KEY>" <source_url>/api/v1/version
```
Expected output:
```json
{"version":"1.1.1.dev22","main_version":"1.1.1","package":"Langflow Nightly"}
```

#### 5. Version Information Fetching
- On creating or updating a workflow source, automatically call the `/api/v1/version` endpoint to fetch version info and store it in the source record.
- Ensure that version data is refreshed periodically or on subsequent updates.

### Relevant Files / Modules to Update
- **New Model**: Create `automagik/core/workflows/source.py` for the `WorkflowSource` model.
- **Workflow Model**: Update `automagik/core/workflows/workflow.py` to add a relationship with `WorkflowSource`.
- **Remote Manager**: Update `automagik/core/workflows/remote.py` (LangFlowManager) to handle dynamic configuration.
- **Workflow Manager**: Update `automagik/core/workflows/manager.py` to use the associated workflow source when running workflows.
- **API Endpoints**: Create or update endpoints in `automagik/api/routers` (or separate file like `sources.py`) for source management.
- **CLI Commands**: Add commands in `automagik/cli/commands/sources.py` for creating, updating, and testing sources.

### Additional Considerations
- **Migrations**: Ensure that migration scripts are created to add the new `WorkflowSource` table and update foreign keys in the workflow table.
- **Security**: Follow best practices to manage encryption keys and avoid exposing sensitive data in logs or API responses.
- **Testing & Validation**: Validate the implementation using automated tests to ensure encryption, decryption, and API integration work as expected.