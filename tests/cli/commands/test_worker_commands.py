"""Test worker command functionality."""

import os
import logging
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from click.testing import CliRunner
from contextlib import asynccontextmanager
from automagik.cli.commands.worker import (
    worker_group,
    configure_logging,
    get_pid_file,
    write_pid,
    read_pid,
    is_worker_running,
    stop_worker,
    start_worker,
    stop_worker_command,
    worker_status
)

from automagik.core.database.session import get_session


@pytest.fixture
def mock_pid_file(tmp_path):
    """Mock PID file location."""
    pid_file = tmp_path / "worker.pid"
    with patch("automagik.cli.commands.worker.os.path.expanduser") as mock_expand:
        mock_expand.return_value = str(pid_file)
        yield pid_file


@pytest.fixture
def mock_log_dir(tmp_path):
    """Mock log directory."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir(exist_ok=True)
    return log_dir


class MockScalars:
    """Mock scalars result that has an all() method."""
    def __init__(self, values):
        print("Creating MockScalars with values:", values)
        self._values = values
    
    def all(self):
        print("Called MockScalars.all(), returning:", self._values)
        return self._values

class MockResult:
    """Mock execute result that has a scalars() method."""
    def __init__(self, values):
        print("Creating MockResult with values:", values)
        self._values = values
    
    def scalars(self):
        print("Called MockResult.scalars()")
        return MockScalars(self._values)
    
    def __await__(self):
        print("Called MockResult.__await__()")
        yield
        return self

class MockSession:
    """Mock database session."""
    def __init__(self):
        print("Creating MockSession")
        
    async def execute(self, *args, **kwargs):
        print("Called MockSession.execute()")
        return MockResult([])
    
    async def __aenter__(self):
        print("Called MockSession.__aenter__()")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Called MockSession.__aexit__()")
        pass
    
    async def close(self):
        print("Called MockSession.close()")
        pass
    
    async def commit(self):
        print("Called MockSession.commit()")
        pass
    
    async def rollback(self):
        print("Called MockSession.rollback()")
        pass

@pytest.fixture
def mock_session():
    """Mock database session."""
    return MockSession()

@pytest.fixture
def mock_get_session(mock_session):
    """Mock get_session context manager."""
    @asynccontextmanager
    async def _mock_get_session():
        print("Entering mock_get_session context")
        try:
            yield mock_session
        finally:
            print("Exiting mock_get_session context")
    return _mock_get_session


@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    
    asyncio.set_event_loop(loop)
    yield loop
    try:
        loop.close()
    except RuntimeError:
        pass


@pytest.mark.asyncio
async def test_worker_status_not_running(mock_pid_file, mock_session):
    """Test worker status when not running."""
    with patch("automagik.cli.commands.worker.asyncio.run") as mock_run:
        mock_run.return_value = "Worker is not running"
        runner = CliRunner()
        result = runner.invoke(worker_group, ["status"])
        assert result.exit_code == 0
        assert "Worker is not running" in mock_run.return_value

@pytest.mark.asyncio
async def test_worker_status_running(mock_pid_file, mock_session):
    """Test worker status when running."""
    # Write a PID file
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write(str(os.getpid()))

    with patch("automagik.cli.commands.worker.asyncio.run") as mock_run:
        mock_run.return_value = "Worker is running"
        runner = CliRunner()
        result = runner.invoke(worker_group, ["status"])
        assert result.exit_code == 0
        assert "Worker is running" in mock_run.return_value

@pytest.mark.asyncio
async def test_worker_stop_not_running(mock_pid_file):
    """Test stopping worker when not running."""
    runner = CliRunner()
    result = runner.invoke(worker_group, ["stop"])
    assert result.exit_code == 0
    assert "No worker process is running" in result.output

@pytest.mark.asyncio
async def test_worker_stop_running(mock_pid_file):
    """Test stopping worker when running."""
    # Write a PID file with current process ID
    pid = os.getpid()
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write(str(pid))

    # Setup mock process
    mock_process = MagicMock()
    mock_process.is_running.return_value = True
    mock_process.name.return_value = "python"
    with patch("psutil.Process", return_value=mock_process):
        runner = CliRunner()
        result = runner.invoke(worker_group, ["stop"])
        assert result.exit_code == 0
        assert "Stopping worker process" in result.output
        assert "Worker process stopped" in result.output

@pytest.mark.asyncio
async def test_worker_start(mock_pid_file, mock_log_dir):
    """Test starting worker process."""
    custom_log_path = str(mock_log_dir / "worker.log")
    os.environ["AUTOMAGIK_WORKER_LOG"] = custom_log_path
    os.environ["AUTOMAGIK_ENV"] = "testing"  # Skip worker registration

    # Create a synchronous mock for worker_loop
    def mock_worker_loop():
        return None

    runner = CliRunner()
    with patch("automagik.cli.commands.worker.daemonize"), \
         patch("automagik.cli.commands.worker.worker_loop", new=mock_worker_loop), \
         patch("asyncio.run", lambda x: None):  # Make asyncio.run do nothing
        result = runner.invoke(worker_group, ["start"])
        assert result.exit_code == 0
        assert "Starting worker process" in result.output

@pytest.mark.asyncio
async def test_worker_start_already_running(mock_pid_file, mock_log_dir):
    """Test starting worker when already running."""
    # Write a PID file with current process ID
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write(str(os.getpid()))

    # Create a mock coroutine for worker_loop
    mock_worker_loop = AsyncMock()

    with patch("os.kill"), \
         patch.dict(os.environ, {"AUTOMAGIK_WORKER_LOG": str(mock_log_dir / "worker.log")}), \
         patch("automagik.cli.commands.worker.worker_loop", return_value=mock_worker_loop):
        runner = CliRunner()
        result = runner.invoke(worker_group, ["start"])
        assert result.exit_code == 0
        assert "Worker is already running" in result.output

@pytest.mark.asyncio
async def test_read_pid_no_file(mock_pid_file):
    """Test reading PID when file doesn't exist."""
    from automagik.cli.commands.worker import read_pid
    assert read_pid() is None

@pytest.mark.asyncio
async def test_read_pid_invalid_content(mock_pid_file):
    """Test reading PID with invalid content."""
    from automagik.cli.commands.worker import read_pid

    # Write invalid content to PID file
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write("invalid")

    assert read_pid() is None

@pytest.mark.asyncio
async def test_configure_logging_default():
    """Test configuring logging with default settings."""
    from automagik.cli.commands.worker import configure_logging

    # Clear any existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure logging with default settings
    configure_logging()

    # Verify logger configuration
    root_logger = logging.getLogger()
    assert len(root_logger.handlers) >= 1
    assert any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers)

@pytest.mark.asyncio
async def test_configure_logging_custom_path(mock_log_dir):
    """Test configuring logging with custom path."""
    from automagik.cli.commands.worker import configure_logging

    # Clear any existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure logging with custom path
    custom_log_path = str(mock_log_dir / "worker.log")
    os.environ["AUTOMAGIK_WORKER_LOG"] = custom_log_path
    configure_logging()

    # Verify logger configuration
    root_logger = logging.getLogger()
    assert len(root_logger.handlers) >= 1
    assert any(isinstance(h, logging.FileHandler) and h.baseFilename == custom_log_path for h in root_logger.handlers)

@pytest.mark.asyncio
async def test_worker_start_logging(mock_pid_file, mock_log_dir):
    """Test that worker start configures logging correctly."""
    custom_log_path = os.path.join(mock_log_dir, "worker.log")
    os.environ["AUTOMAGIK_WORKER_LOG"] = custom_log_path
    os.environ["AUTOMAGIK_ENV"] = "testing"  # Skip worker registration

    # Create a synchronous mock for worker_loop
    def mock_worker_loop():
        return None

    runner = CliRunner()
    with patch("automagik.cli.commands.worker.daemonize"), \
         patch("automagik.cli.commands.worker.worker_loop", new=mock_worker_loop), \
         patch("asyncio.run", lambda x: None):  # Make asyncio.run do nothing
        result = runner.invoke(worker_group, ["start"])
        assert result.exit_code == 0
        assert "Starting worker process" in result.output

        # Verify log file was created
        assert os.path.exists(custom_log_path)


@pytest.fixture(autouse=True)
def cleanup_logging():
    """Clean up logging configuration after each test."""
    # Store original env vars
    worker_log = os.environ.get("AUTOMAGIK_WORKER_LOG")
    env = os.environ.get("AUTOMAGIK_ENV")
    
    yield
    
    # Reset root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Reset env vars
    if worker_log:
        os.environ["AUTOMAGIK_WORKER_LOG"] = worker_log
    else:
        os.environ.pop("AUTOMAGIK_WORKER_LOG", None)
        
    if env:
        os.environ["AUTOMAGIK_ENV"] = env
    else:
        os.environ.pop("AUTOMAGIK_ENV", None)
