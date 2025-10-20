"""Lightweight telemetry for usage analytics."""

import json
import os
import platform
import sys
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List
from urllib.request import Request, urlopen
from urllib.error import URLError
import logging

logger = logging.getLogger(__name__)


class TelemetryClient:
    """Lightweight telemetry client using OTLP format."""

    def __init__(self):
        self.endpoint = "https://telemetry.namastex.ai/v1/traces"
        self.timeout = 5  # seconds
        self.user_id = self._get_or_create_user_id()
        self.session_id = str(uuid.uuid4())
        self.enabled = self._is_telemetry_enabled()

        # Project identification for multiple Namastex projects
        self.project_name = "automagik-spark"
        self.project_version = "0.3.6"  # TODO: Get from package metadata
        self.organization = "namastex"

    def _get_or_create_user_id(self) -> str:
        """Get or create anonymous user ID."""
        user_id_file = Path.home() / ".automagik" / "user_id"

        if user_id_file.exists():
            try:
                return user_id_file.read_text().strip()
            except Exception:
                pass

        # Create new user ID
        user_id = str(uuid.uuid4())
        try:
            user_id_file.parent.mkdir(exist_ok=True)
            user_id_file.write_text(user_id)
        except Exception:
            pass

        return user_id

    def _is_telemetry_enabled(self) -> bool:
        """Check if telemetry is enabled."""
        # Check project-specific environment variable
        if os.getenv("AUTOMAGIK_SPARK_DISABLE_TELEMETRY", "false").lower() in (
            "true",
            "1",
            "yes",
            "on",
        ):
            return False

        # Check opt-out file
        opt_out_file = Path.home() / ".automagik-no-telemetry"
        if opt_out_file.exists():
            return False

        # Check CI/testing environments
        if any(os.getenv(var) for var in ["CI", "GITHUB_ACTIONS", "TRAVIS", "JENKINS"]):
            return False

        return True

    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        return {
            "os": platform.system(),
            "os_version": platform.release(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "architecture": platform.machine(),
            "is_docker": os.path.exists("/.dockerenv"),
            "project_name": self.project_name,
            "project_version": self.project_version,
            "organization": self.organization,
        }

    def _send_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Send telemetry event in OTLP format."""
        if not self.enabled:
            return

        # Create OTLP-compatible trace data
        trace_id = str(uuid.uuid4()).replace("-", "")[:32]
        span_id = str(uuid.uuid4()).replace("-", "")[:16]

        # OTLP format payload
        payload = {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": [
                            {
                                "key": "service.name",
                                "value": {"stringValue": self.project_name},
                            },
                            {
                                "key": "service.version",
                                "value": {"stringValue": self.project_version},
                            },
                            {
                                "key": "service.organization",
                                "value": {"stringValue": self.organization},
                            },
                            {"key": "user.id", "value": {"stringValue": self.user_id}},
                            {
                                "key": "session.id",
                                "value": {"stringValue": self.session_id},
                            },
                            {
                                "key": "telemetry.sdk.name",
                                "value": {"stringValue": "automagik-spark"},
                            },
                            {
                                "key": "telemetry.sdk.version",
                                "value": {"stringValue": self.project_version},
                            },
                        ]
                    },
                    "scopeSpans": [
                        {
                            "scope": {
                                "name": f"{self.project_name}.telemetry",
                                "version": self.project_version,
                            },
                            "spans": [
                                {
                                    "traceId": trace_id,
                                    "spanId": span_id,
                                    "name": event_type,
                                    "kind": "SPAN_KIND_INTERNAL",
                                    "startTimeUnixNano": int(
                                        time.time() * 1_000_000_000
                                    ),
                                    "endTimeUnixNano": int(time.time() * 1_000_000_000),
                                    "attributes": self._create_attributes(data),
                                    "status": {"code": "STATUS_CODE_OK"},
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        try:
            request = Request(
                self.endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )

            with urlopen(request, timeout=self.timeout) as response:
                if response.status != 200:
                    logger.debug(
                        f"Telemetry event failed with status {response.status}"
                    )

        except URLError as e:
            logger.debug(f"Telemetry event failed: {e}")
        except Exception as e:
            logger.debug(f"Telemetry event error: {e}")

    def _create_attributes(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert data to OTLP attribute format."""
        attributes = []

        # Add system info
        system_info = self._get_system_info()
        for key, value in system_info.items():
            attributes.append(
                {"key": f"system.{key}", "value": {"stringValue": str(value)}}
            )

        # Add event data
        for key, value in data.items():
            if isinstance(value, bool):
                attributes.append(
                    {"key": f"event.{key}", "value": {"boolValue": value}}
                )
            elif isinstance(value, (int, float)):
                attributes.append(
                    {"key": f"event.{key}", "value": {"doubleValue": float(value)}}
                )
            else:
                attributes.append(
                    {"key": f"event.{key}", "value": {"stringValue": str(value)}}
                )

        return attributes

    def track_installation(self, install_type: str = "pip") -> None:
        """Track installation event."""
        self._send_event(
            "installation", {"install_type": install_type, "first_run": True}
        )

    def track_command(
        self,
        command: str,
        duration: Optional[float] = None,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """Track CLI command usage."""
        data = {"command": command, "success": success}

        if duration is not None:
            data["duration_ms"] = int(duration * 1000)

        if error:
            data["error"] = str(error)[:500]  # Truncate long errors

        self._send_event("command", data)

    def track_api_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        duration: Optional[float] = None,
    ) -> None:
        """Track API request."""
        data = {"endpoint": endpoint, "method": method, "status_code": status_code}

        if duration is not None:
            data["duration_ms"] = int(duration * 1000)

        self._send_event("api_request", data)

    def track_workflow_execution(
        self,
        workflow_type: str,
        duration: Optional[float] = None,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """Track workflow execution."""
        data = {"workflow_type": workflow_type, "success": success}

        if duration is not None:
            data["duration_ms"] = int(duration * 1000)

        if error:
            data["error"] = str(error)[:500]

        self._send_event("workflow_execution", data)

    def track_feature_usage(
        self, feature: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Track feature usage."""
        data = {"feature": feature}

        if metadata:
            # Type ignore: data dict accepts Any values, metadata is Dict[str, Any]
            # This is safe as _create_attributes handles nested dicts properly
            data["metadata"] = metadata  # type: ignore[dict-item]

        self._send_event("feature_usage", data)


# Global telemetry client instance
_client = None


def get_telemetry_client() -> TelemetryClient:
    """Get global telemetry client instance."""
    global _client
    if _client is None:
        _client = TelemetryClient()
    return _client


def disable_telemetry() -> None:
    """Disable telemetry by creating opt-out file."""
    opt_out_file = Path.home() / ".automagik-no-telemetry"
    try:
        opt_out_file.touch()
        print(f"Telemetry disabled. Opt-out file created at: {opt_out_file}")
    except Exception as e:
        print(f"Failed to create opt-out file: {e}")


def enable_telemetry() -> None:
    """Enable telemetry by removing opt-out file."""
    opt_out_file = Path.home() / ".automagik-no-telemetry"
    try:
        if opt_out_file.exists():
            opt_out_file.unlink()
            print("Telemetry enabled. Opt-out file removed.")
        else:
            print("Telemetry is already enabled.")
    except Exception as e:
        print(f"Failed to remove opt-out file: {e}")


def is_telemetry_enabled() -> bool:
    """Check if telemetry is enabled."""
    return get_telemetry_client().enabled


# Convenience functions for common events
def track_installation(install_type: str = "pip") -> None:
    """Track installation event."""
    get_telemetry_client().track_installation(install_type)


def track_command(
    command: str,
    duration: Optional[float] = None,
    success: bool = True,
    error: Optional[str] = None,
) -> None:
    """Track CLI command usage."""
    get_telemetry_client().track_command(command, duration, success, error)


def track_api_request(
    endpoint: str, method: str, status_code: int, duration: Optional[float] = None
) -> None:
    """Track API request."""
    get_telemetry_client().track_api_request(endpoint, method, status_code, duration)


def track_workflow_execution(
    workflow_type: str,
    duration: Optional[float] = None,
    success: bool = True,
    error: Optional[str] = None,
) -> None:
    """Track workflow execution."""
    get_telemetry_client().track_workflow_execution(
        workflow_type, duration, success, error
    )


def track_feature_usage(
    feature: str, metadata: Optional[Dict[str, Any]] = None
) -> None:
    """Track feature usage."""
    get_telemetry_client().track_feature_usage(feature, metadata)
