
"""
Automagik package initialization.
"""

import logging
from .version import __version__

# Set httpx logger to WARNING level to reduce verbosity
logging.getLogger("httpx").setLevel(logging.WARNING)

__all__ = ["__version__"]

