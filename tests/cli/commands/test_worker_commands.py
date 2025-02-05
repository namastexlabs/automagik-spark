"""Test worker command functionality."""

import os
import logging
import pytest
import asyncio
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


@pytest.mark.asyncio
async def test_worker_status_not_running():
    """Test worker status when not running."""
    with patch("automagik.cli.commands.worker.get_session") as mock_session_factory:
        # Set up mock session
        mock_session = AsyncMock()
        mock_session_factory.return_value.__aenter__.return_value = mock_session
        
        # Set up mock result
        mock_result = AsyncMock()
        mock_result.scalars = MagicMock()
        mock_result.scalars.return_value = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result
        
        # Mock click.echo
        with patch("click.echo") as mock_echo:
            # Mock asyncio.get_event_loop to return our test event loop
            with patch("asyncio.get_event_loop", return_value=asyncio.get_running_loop()):
                runner = CliRunner()
                result = runner.invoke(worker_group, ["status"])
                
                await asyncio.sleep(0.1)  # Give time for tasks to complete
                
                assert result.exit_code == 0
                mock_echo.assert_called_with("No workers found")


@pytest.mark.asyncio
async def test_worker_status_running():
    """Test worker status when running."""
    with patch("automagik.cli.commands.worker.get_session") as mock_session_factory:
        mock_session = AsyncMock()
        mock_session_factory.return_value.__aenter__.return_value = mock_session
        
        # Create a mock worker
        mock_worker = MagicMock()
        mock_worker.id = "12345678"
        mock_worker.hostname = "test-host"
        mock_worker.pid = 1234
        mock_worker.status = "running"
        mock_worker.current_task_id = None
        mock_worker.last_heartbeat = None
        
        # Set up mock result
        mock_result = AsyncMock()
        mock_result.scalars = MagicMock()
        mock_result.scalars.return_value = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_worker]
        mock_session.execute.return_value = mock_result
        
        # Mock click.echo
        with patch("click.echo") as mock_echo:
            # Mock asyncio.get_event_loop to return our test event loop
            with patch("asyncio.get_event_loop", return_value=asyncio.get_running_loop()):
                runner = CliRunner()
                result = runner.invoke(worker_group, ["status"])
                
                await asyncio.sleep(0.1)  # Give time for tasks to complete
                
                assert result.exit_code == 0
                mock_echo.assert_called()  # Table output is complex, just check if echo was called


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
    # Write a fake PID file
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    fake_pid = 12345  # Use a fake PID that doesn't exist
    with open(mock_pid_file, "w") as f:
        f.write(str(fake_pid))

    with patch("automagik.cli.commands.worker.is_worker_running") as mock_running, \
         patch("psutil.Process") as mock_process:
        mock_running.return_value = True
        
        # Mock the Process class
        mock_proc = MagicMock()
        mock_proc.is_running.return_value = True
        mock_proc.name.return_value = "python"
        mock_process.return_value = mock_proc
        
        runner = CliRunner()
        result = runner.invoke(worker_group, ["stop"])
        assert result.exit_code == 0
        assert "Stopping worker process..." in result.output
        assert "Worker process stopped" in result.output
        
        # Verify process was terminated
        mock_proc.terminate.assert_called_once()


@pytest.mark.asyncio
async def test_worker_start(mock_pid_file, mock_log_dir, caplog):
    """Test starting worker process."""
    with patch("automagik.cli.commands.worker.is_worker_running") as mock_running, \
         patch("automagik.cli.commands.worker.configure_logging") as mock_logging, \
         patch("automagik.cli.commands.worker.write_pid") as mock_write_pid, \
         patch("automagik.cli.commands.worker.worker_loop", new_callable=AsyncMock) as mock_loop:
        mock_running.return_value = False
        mock_logging.return_value = str(mock_log_dir / "worker.log")
        mock_loop.return_value = None
        
        runner = CliRunner()
        with caplog.at_level(logging.INFO):
            result = runner.invoke(worker_group, ["start"])
            
            # Wait for any pending tasks
            loop = asyncio.get_event_loop()
            await asyncio.sleep(0.1)  # Give time for tasks to complete
            
            assert result.exit_code == 0
            assert "Starting worker process" in caplog.text


@pytest.mark.asyncio
async def test_worker_start_already_running(mock_pid_file, mock_log_dir):
    """Test starting worker when already running."""
    # Write a PID file
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write(str(os.getpid()))

    runner = CliRunner()
    result = runner.invoke(worker_group, ["start"])
    assert result.exit_code == 0
    assert "Worker is already running" in result.output


@pytest.mark.asyncio
async def test_read_pid_no_file(mock_pid_file):
    """Test reading PID when file doesn't exist."""
    assert read_pid() is None


@pytest.mark.asyncio
async def test_read_pid_invalid_content(mock_pid_file):
    """Test reading PID with invalid content."""
    # Write invalid content to PID file
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write("invalid")

    assert read_pid() is None


@pytest.mark.asyncio
async def test_configure_logging_default():
    """Test configuring logging with default settings."""
    with patch("automagik.cli.commands.worker.os.makedirs") as mock_makedirs, \
         patch("automagik.cli.commands.worker.logging.FileHandler") as mock_handler, \
         patch("automagik.cli.commands.worker.os.path.isdir") as mock_isdir:
        mock_isdir.return_value = True
        log_path = configure_logging()
        mock_makedirs.assert_called_once()
        mock_handler.assert_called_once()
        assert "logs/worker.log" in log_path


@pytest.mark.asyncio
async def test_configure_logging_custom_path(mock_log_dir):
    """Test configuring logging with custom path."""
    custom_log_path = str(mock_log_dir / "worker.log")
    with patch("automagik.cli.commands.worker.os.makedirs") as mock_makedirs, \
         patch("automagik.cli.commands.worker.logging.FileHandler") as mock_handler, \
         patch.dict(os.environ, {"AUTOMAGIK_WORKER_LOG": custom_log_path}):
        log_path = configure_logging()
        mock_makedirs.assert_called_once()
        mock_handler.assert_called_once()
        assert custom_log_path == log_path


@pytest.mark.asyncio
async def test_worker_start_logging(mock_pid_file, mock_log_dir, caplog):
    """Test that worker start configures logging correctly."""
    custom_log_path = str(mock_log_dir / "worker.log")
    with patch("automagik.cli.commands.worker.is_worker_running") as mock_running, \
         patch("automagik.cli.commands.worker.configure_logging") as mock_logging, \
         patch("automagik.cli.commands.worker.write_pid") as mock_write_pid, \
         patch("automagik.cli.commands.worker.worker_loop", new_callable=AsyncMock) as mock_loop, \
         patch.dict(os.environ, {"AUTOMAGIK_WORKER_LOG": custom_log_path}):
        mock_running.return_value = False
        mock_logging.return_value = custom_log_path
        mock_loop.return_value = None

        runner = CliRunner()
        with caplog.at_level(logging.INFO):
            result = runner.invoke(worker_group, ["start"])
            
            # Wait for any pending tasks
            loop = asyncio.get_event_loop()
            await asyncio.sleep(0.1)  # Give time for tasks to complete
            
            assert result.exit_code == 0
            assert "Starting worker process" in caplog.text
            assert f"Worker logs will be written to {custom_log_path}" in caplog.text
            mock_logging.assert_called_once()
            mock_write_pid.assert_called_once()


@pytest.fixture(autouse=True)
def cleanup_logging():
    """Clean up logging configuration after each test."""
    yield
    # Remove all handlers from the root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
