"""Test cases for scheduler utility functions."""

import pytest
from datetime import timedelta
from automagik_spark.core.scheduler.utils import validate_interval, parse_interval


@pytest.mark.parametrize(
    "interval,expected",
    [
        # Valid formats
        ("1m", True),      # 1 minute
        ("30m", True),     # 30 minutes
        ("2h", True),      # 2 hours
        ("24h", True),     # 24 hours
        ("1d", True),      # 1 day
        ("7d", True),      # 7 days
        ("60m", True),     # 60 minutes
        ("168h", True),    # 168 hours (1 week)
        ("365d", True),    # 365 days
        ("999m", True),    # Large number
        
        # Invalid formats
        ("invalid", False),  # Invalid string
        ("1x", False),      # Invalid unit
        ("0m", False),      # Zero value
        ("-5h", False),     # Negative value
        ("1.5h", False),    # Decimal value
        ("m", False),       # Missing value
        ("h1", False),      # Unit before value
        ("1mm", False),     # Double unit
        ("1 m", False),     # Space in string
        ("one m", False),   # Text instead of number
        
        # Edge cases
        ("", False),        # Empty string
        (None, False),      # None value
        (123, False),       # Integer
        (1.5, False),      # Float
        (True, False),      # Boolean
        ("1H", False),      # Uppercase unit
        ("01m", False),     # Leading zero
    ],
)
def test_validate_interval(interval, expected):
    """Test validate_interval function with various inputs."""
    assert validate_interval(interval) == expected


@pytest.mark.parametrize(
    "interval,expected",
    [
        ("1m", timedelta(minutes=1)),
        ("30m", timedelta(minutes=30)),
        ("1h", timedelta(hours=1)),
        ("24h", timedelta(hours=24)),
        ("1d", timedelta(days=1)),
        ("7d", timedelta(days=7)),
        ("60m", timedelta(minutes=60)),
        ("168h", timedelta(hours=168)),
    ],
)
def test_parse_interval_valid(interval, expected):
    """Test parse_interval function with valid intervals."""
    assert parse_interval(interval) == expected


@pytest.mark.parametrize(
    "interval",
    [
        "invalid",  # Invalid string
        "1x",      # Invalid unit
        "0m",      # Zero value
        "-5h",     # Negative value
        "1.5h",    # Decimal value
        "m",       # Missing value
        "h1",      # Unit before value
        "1mm",     # Double unit
        "1 m",     # Space in string
        "one m",   # Text instead of number
        "",        # Empty string
        None,      # None value
    ],
)
def test_parse_interval_invalid(interval):
    """Test parse_interval function with invalid intervals."""
    with pytest.raises(ValueError) as exc_info:
        parse_interval(interval)
    assert "Invalid interval format" in str(exc_info.value)


def test_parse_interval_type_errors():
    """Test parse_interval function with invalid types."""
    invalid_types = [123, 1.5, True, [], {}]
    for value in invalid_types:
        with pytest.raises(ValueError) as exc_info:
            parse_interval(value)
        assert "Invalid interval format" in str(exc_info.value)


def test_validate_interval_with_exceptions():
    """Test validate_interval with inputs that would raise exceptions."""
    class FailingString:
        def __str__(self):
            raise AttributeError("String conversion failed")
        
        def __len__(self):
            raise ValueError("Length check failed")
            
        def lower(self):
            raise AttributeError("Lower conversion failed")
        
    assert validate_interval(FailingString()) is False
    
    class ExplodingString:
        def __str__(self):
            return "30m"
            
        def __len__(self):
            raise TypeError("Cannot get length")
            
    assert validate_interval(ExplodingString()) is False


@pytest.mark.parametrize(
    "interval",
    [
        object(),  # Object that will raise TypeError on string operations
        b"30m",    # Bytes object to test TypeError scenarios
    ]
)
def test_validate_interval_type_errors(interval):
    """Test validate_interval with inputs that would raise TypeError."""
    assert validate_interval(interval) is False


def test_parse_interval_extreme_values():
    """Test parse_interval function with extreme but valid values."""
    # Test large values that are still valid
    assert parse_interval("999m") == timedelta(minutes=999)
    assert parse_interval("999h") == timedelta(hours=999)
    assert parse_interval("999d") == timedelta(days=999)