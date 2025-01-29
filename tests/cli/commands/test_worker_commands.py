"""Test worker command functionality."""

import os
import signal
import pytest
from click.testing import CliRunner
from unittest import mock
from unittest.mock import patch, MagicMock
import logging

from automagik.cli.commands.worker import worker_group, configure_logging


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


@pytest.fixture(autouse=True)
def cleanup_logging():
    """Clean up logging configuration after each test."""
    yield
    # Reset root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.root.setLevel(logging.WARNING)


def test_worker_status_not_running(mock_pid_file):
    """Test worker status when not running."""
    runner = CliRunner()
    result = runner.invoke(worker_group, ["status"])
    assert result.exit_code == 0
    assert "Worker process is not running" in result.output


def test_worker_status_running(mock_pid_file):
    """Test worker status when running."""
    # Write a PID file
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write(str(os.getpid()))

    with patch("os.kill") as mock_kill:
        runner = CliRunner()
        result = runner.invoke(worker_group, ["status"])
        assert result.exit_code == 0
        assert "Worker process is running" in result.output
        mock_kill.assert_called_once_with(os.getpid(), 0)


def test_worker_stop_not_running(mock_pid_file):
    """Test stopping worker when not running."""
    runner = CliRunner()
    result = runner.invoke(worker_group, ["stop"])
    assert result.exit_code == 0
    assert "No worker process is running" in result.output


@patch("psutil.Process")
def test_worker_stop_running(mock_process_class, mock_pid_file):
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
    mock_process_class.return_value = mock_process

    runner = CliRunner()
    result = runner.invoke(worker_group, ["stop"])
    assert result.exit_code == 0
    assert "Stopping worker process" in result.output
    assert "Worker process stopped" in result.output

    # Verify process was terminated
    mock_process.terminate.assert_called_once()
    mock_process.wait.assert_called_once_with(timeout=10)


@patch("asyncio.run")
@patch("signal.signal")
def test_worker_start(mock_signal, mock_run, mock_pid_file, mock_log_dir):
    """Test starting worker process."""
    custom_log_path = str(mock_log_dir / "worker.log")
    with patch.dict(os.environ, {"AUTOMAGIK_WORKER_LOG": custom_log_path}):
        runner = CliRunner()
        result = runner.invoke(worker_group, ["start"])
        assert result.exit_code == 0
        assert "Starting worker process" in result.output
        assert mock_run.called
        assert mock_signal.call_count == 2  # SIGINT and SIGTERM handlers


def test_worker_start_already_running(mock_pid_file, mock_log_dir):
    """Test starting worker when already running."""
    # Write a PID file with current process ID
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write(str(os.getpid()))

    with patch("os.kill"), \
         patch.dict(os.environ, {"AUTOMAGIK_WORKER_LOG": str(mock_log_dir / "worker.log")}):
        runner = CliRunner()
        result = runner.invoke(worker_group, ["start"])
        assert result.exit_code == 0
        assert "Worker is already running" in result.output


def test_read_pid_no_file(mock_pid_file):
    """Test reading PID when file doesn't exist."""
    from automagik.cli.commands.worker import read_pid
    pid = read_pid()
    assert pid is None


def test_read_pid_invalid_content(mock_pid_file):
    """Test reading PID with invalid content."""
    os.makedirs(os.path.dirname(mock_pid_file), exist_ok=True)
    with open(mock_pid_file, "w") as f:
        f.write("not a pid")
    
    from automagik.cli.commands.worker import read_pid
    pid = read_pid()
    assert pid is None


def test_configure_logging_default(mock_log_dir):
    """Test logging configuration with default path."""
    with patch("automagik.cli.commands.worker.os.path.expanduser") as mock_expand:
        mock_expand.return_value = str(mock_log_dir / "worker.log")
        with patch.dict(os.environ, {}, clear=True):  # Clear env vars
            log_path = configure_logging()
            assert log_path == str(mock_log_dir / "worker.log")
            assert os.path.exists(log_path)

            # Verify log file is writable
            logger = logging.getLogger("test_logger")
            test_message = "Test log message"
            logger.info(test_message)

            # Allow a small delay for log writing
            import time
            time.sleep(0.1)

            with open(log_path) as f:
                log_content = f.read()
                assert test_message in log_content


def test_configure_logging_custom_path(mock_log_dir):
    """Test logging configuration with custom path from env."""
    custom_log_path = str(mock_log_dir / "custom" / "worker.log")
    with patch.dict(os.environ, {"AUTOMAGIK_WORKER_LOG": custom_log_path}):
        log_path = configure_logging()
        assert log_path == custom_log_path
        assert os.path.exists(custom_log_path)
        assert os.path.exists(os.path.dirname(custom_log_path))

        # Verify log file is writable
        logger = logging.getLogger("test_logger")
        test_message = "Test log message"
        logger.info(test_message)

        # Allow a small delay for log writing
        import time
        time.sleep(0.1)

        with open(custom_log_path) as f:
            log_content = f.read()
            assert test_message in log_content


def test_worker_start_logging(mock_pid_file, mock_log_dir):
    """Test that worker start configures logging correctly."""
    custom_log_path = str(mock_log_dir / "worker.log")
    with patch.dict(os.environ, {"AUTOMAGIK_WORKER_LOG": custom_log_path}):
        with patch("asyncio.run"), patch("signal.signal"):
            runner = CliRunner()
            result = runner.invoke(worker_group, ["start"])
            assert result.exit_code == 0
            assert "Starting worker process" in result.output
            assert os.path.exists(custom_log_path)

            # Allow a small delay for log writing
            import time
            time.sleep(0.1)

            # Verify log file contains startup message
            with open(custom_log_path) as f:
                log_content = f.read()
                assert "Worker logs will be written to" in log_content
