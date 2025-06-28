
"""
Automagik package initialization.
"""

import logging
import tomllib
from pathlib import Path

def _get_version():
    """Get version from pyproject.toml"""
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    except Exception:
        return "unknown"

__version__ = _get_version()

# Set httpx logger to WARNING level to reduce verbosity
logging.getLogger("httpx").setLevel(logging.WARNING)

__all__ = ["__version__"]

