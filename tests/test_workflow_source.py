import json
import pytest
from automagik.core.workflows.source import WorkflowSource
from automagik.core.workflows.workflow import Workflow

# These tests assume that you have implemented the following in your codebase:
# 1. A 'WorkflowSource' model in automagik/core/workflows/source.py with methods:
#    - encrypt_api_key(plain_text: str) -> str
#    - decrypt_api_key(encrypted_text: str) -> str
#    and attributes: source_type, url, encrypted_api_key, version_info, status
# 2. A 'Workflow' model in automagik/core/workflows/workflow.py that has a relationship with WorkflowSource via an attribute 'source'

# The following tests are part of a TDD approach for the new multi-source support feature.

def test_create_workflow_source_encryption():
    """Test that the API key encryption and decryption work as expected."""
    sample_api_key = "secret_key_123"

    # Create a WorkflowSource instance with encrypted API key
    # Note: The encrypt_api_key method should be implemented to securely encrypt the API key.
    encrypted_key = WorkflowSource.encrypt_api_key(sample_api_key)

    # Instantiate a WorkflowSource object. In a real scenario, you would likely use an ORM constructor.
    source = WorkflowSource(
        source_type="langflow",
        url="http://example.com",
        encrypted_api_key=encrypted_key,
        version_info=json.dumps({"version": "1.1.1.dev22", "main_version": "1.1.1", "package": "Langflow Nightly"}),
        status="active"
    )

    # Decrypt the API key and verify it matches
    decrypted_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)
    assert decrypted_key == sample_api_key, "Decrypted API key does not match the original"


def test_workflow_association_with_source():
    """Test that a Workflow can be associated with a WorkflowSource."""
    # Create a dummy WorkflowSource instance
    encrypted_key = WorkflowSource.encrypt_api_key("dummy_secret")

    source = WorkflowSource(
        source_type="langflow",
        url="http://example.com",
        encrypted_api_key=encrypted_key,
        version_info=json.dumps({"version": "1.0.0", "main_version": "1.0.0"}),
        status="active"
    )

    # Create a dummy Workflow linked to the above source
    # It is assumed that Workflow model's constructor accepts a 'source' parameter
    workflow = Workflow(name="Test Workflow", source=source)

    # Verify that the workflow's source is set correctly
    assert workflow.source.url == "http://example.com", "Workflow does not reference the correct source URL"
