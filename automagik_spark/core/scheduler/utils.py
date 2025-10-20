"""
Scheduler utility functions.

Provides standalone utility functions for scheduling operations.
"""

from datetime import timedelta


def validate_interval(interval: str) -> bool:
    """
    Validate interval expression.

    Valid formats:
    - Xm: X minutes (e.g., "1m", "30m")
    - Xh: X hours (e.g., "1h", "24h")
    - Xd: X days (e.g., "1d", "7d")

    Where X is a positive integer.

    Args:
        interval: Interval string to validate

    Returns:
        True if interval is valid, False otherwise
    """
    try:
        # Must be a non-empty string
        if not interval or not isinstance(interval, str):
            return False

        # Must end with valid unit (m, h, d)
        if len(interval) < 2 or interval[-1].lower() not in ["m", "h", "d"]:
            return False

        # Must have a value before the unit
        value_str = interval[:-1]
        if not value_str.isdigit():
            return False

        # Value must be a positive integer
        value = int(value_str)
        if value <= 0:
            return False

        # Must not have any extra characters
        if len(interval) != len(str(value)) + 1:
            return False

        return True

    except (ValueError, TypeError, AttributeError):
        return False


def parse_interval(interval: str) -> timedelta:
    """
    Parse interval string into timedelta.

    Args:
        interval: Interval string (e.g., "30m", "1h", "1d")

    Returns:
        timedelta object

    Raises:
        ValueError if interval is invalid

    Examples:
        >>> parse_interval("30m")
        timedelta(minutes=30)
        >>> parse_interval("2h")
        timedelta(hours=2)
        >>> parse_interval("7d")
        timedelta(days=7)
    """
    if not validate_interval(interval):
        raise ValueError(f"Invalid interval format: {interval}")

    value = int(interval[:-1])
    unit = interval[-1].lower()

    if unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    else:
        raise ValueError("Invalid interval unit")
