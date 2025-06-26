
"""Configuration module."""

import os
from typing import Optional
from functools import lru_cache

class Settings:
    def __init__(self):
        # Worker settings
        self.worker_log = os.getenv("AUTOMAGIK_SPARK_WORKER_LOG", "/var/log/automagik/worker.log")
        self.log_level = os.getenv("AUTOMAGIK_SPARK_LOG_LEVEL", "INFO")
        
        # API settings
        self.api_key = os.getenv("AUTOMAGIK_SPARK_API_KEY")
        self.remote_url = os.getenv("AUTOMAGIK_SPARK_REMOTE_URL", "http://localhost:8000").rstrip("/")
        
        # LangFlow settings
        self.langflow_api_url = os.getenv("LANGFLOW_API_URL", "http://localhost:7860/").rstrip("/")
        self.langflow_api_key = os.getenv("LANGFLOW_API_KEY")

@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_api_key() -> Optional[str]:
    """Get API key from settings."""
    return get_settings().api_key


# Expose LangFlow settings for backward compatibility
LANGFLOW_API_URL = get_settings().langflow_api_url
LANGFLOW_API_KEY = get_settings().langflow_api_key
