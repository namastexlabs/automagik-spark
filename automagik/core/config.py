
"""Configuration module."""

import os
from typing import Optional
from functools import lru_cache

class Settings:
    def __init__(self):
        # Worker settings
        self.worker_log = os.getenv("AUTOMAGIK_WORKER_LOG", "/var/log/automagik/worker.log")
        self.log_level = os.getenv("AUTOMAGIK_LOG_LEVEL", "INFO")
        
        # LangFlow settings
        self.langflow_api_url = os.getenv("LANGFLOW_API_URL", "http://localhost:7860/").rstrip("/")
        self.langflow_api_key = os.getenv("LANGFLOW_API_KEY")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Expose LangFlow settings for backward compatibility
LANGFLOW_API_URL = get_settings().langflow_api_url
LANGFLOW_API_KEY = get_settings().langflow_api_key
