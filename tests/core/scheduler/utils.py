"""
Test cases for scheduler utility functions in automagik_spark.core.scheduler.utils.
"""

import pytest
from datetime import timedelta

from automagik_spark.core.scheduler.utils import (
    validate_interval,
    parse_interval,
)


@pytest.mark.parametrize(
    "interval, expected",
    [
        # Valid Cases
        ("1m", True),  # 1 minute
        ("30m", True),  # 30 minutes
        ("1h", True),  # 1 hour
        ("24h", True),  # 24 hours
        ("1d", True),  # 1 day
        ("7d", True),  # 7 days
        ("999m", True),  # Large number
        # Invalid Cases (from AC)
        ("invalid", False),  # Invalid characters
        ("1x", False),  # Invalid unit
        ("0m", False),  # Zero value (must be +ve)
        ("-5h", False),  # Negative value
        # =Edge Cases (from AC)
        ("", False),  # Empty string
        (None, False),  # None type
        (123, False),  # Non-string type (int)
        # Additional Invalid Cases for 100% Coverage
        ("1.5m", False),  # Non-integer value
        ("m", False),  # Missing value
        ("1mm", False),  # Extra characters
        ("m1", False),  # Unit before value
        (" 1m", False),  # Leading space
        ("1m ", False),  # Trailing space
    ],
)
def test_validate_interval(interval, expected):
    """
    Test validate_interval with a comprehensive set of valid and invalid formats.
    """
    assert validate_interval(interval) == expected


@pytest.mark.parametrize(
    "interval, expected_timedelta",
    [
        # Valid conversions from AC
        ("30m", timedelta(minutes=30)),
        ("2h", timedelta(hours=2)),
        ("1d", timedelta(days=1)),
        # Additional valid conversions
        ("1m", timedelta(minutes=1)),
        ("24h", timedelta(hours=24)),
        ("7d", timedelta(days=7)),
        ("365d", timedelta(days=365)),
    ],
)
def test_parse_interval_valid_conversions(interval, expected_timedelta):
    """
    Test parse_interval correctly converts valid interval strings to timedelta objects.
    """
    assert parse_interval(interval) == expected_timedelta


@pytest.mark.parametrize(
    "invalid_interval",
    [
        # All these cases should fail validation
        "invalid",
        "1x",
        "0m",
        "-5h",
        "",
        None,
        123,
        "1.5m",
        "m",
    ],
)
def test_parse_interval_invalid_raises_value_error(invalid_interval):
    """
    Test parse_interval raises ValueError for any invalid interval format.
    The function must first validate the interval and raise a ValueError if
    it's invalid.
    """
    with pytest.raises(ValueError, match=f"Invalid interval format: {invalid_interval}"):
        parse_interval(invalid_interval)


def test_parse_interval_invalid_unit_post_validation(mocker):
    """
    Test the internal 'else' block of parse_interval for 100% coverage.
    This case should be impossible if validate_interval is working correctly,
    but it ensures the function is robust.
    """
    # Mock validate_interval to return True for a string that would
    # else fail, specifically one with an invalid unit.
    mocker.patch(
        "automagik_spark.core.scheduler.utils.validate_interval",
        return_value=True,
    )

    # "1x" has an invalid unit. validate_interval is mocked to pass,
    # so parse_interval will fail on its internal unit check.
    #
    with pytest.raises(ValueError, match="Invalid interval unit"):
        parse_interval("1x")
