"""Configuration module."""

import os
from typing import Optional

# LangFlow API configuration
LANGFLOW_API_URL = os.getenv("LANGFLOW_API_URL", "http://localhost:7860/api/v1").rstrip("/")
LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY")
