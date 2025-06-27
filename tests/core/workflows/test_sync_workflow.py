
"""Test flow sync functionality."""

import json
from uuid import uuid4, UUID
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy import select
import httpx
from cryptography.fernet import Fernet

from automagik_spark.core.workflows import WorkflowManager
from automagik_spark.core.database.models import Workflow, WorkflowSource


