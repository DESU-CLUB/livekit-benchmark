import os
import shutil
import subprocess
import time
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-broadcast")
SCRIPT_FILE = PROJECT_DIR / "broadcast.py"
LOG_FILE = PROJECT_DIR / "broadcast.log"
ENV_FILE = PROJECT_DIR / ".env.local"


def test_broadcast_script_exists():
    assert SCRIPT_FILE.is_file(), f"broadcast.py not found at {SCRIPT_FILE}"


def test_script_uses_send_data():
    source = SCRIPT_FILE.read_text()
    assert "send_data" in source, (
        "broadcast.py must call send_data to broadcast messages"
    )


def test_script_uses_list_rooms():
    source = SCRIPT_FILE.read_text()
    assert "list_rooms" in source, (
        "broadcast.py must call list_rooms to enumerate active rooms"
    )


def test_script_uses_data_packet_kind_reliable():
    source = SCRIPT_FILE.read_text()
    assert "DATA_PACKET_KIND_RELIABLE" in source, (
        "broadcast.py must use DATA_PACKET_KIND_RELIABLE for reliable delivery"
    )


def test_script_has_system_message_type():
    source = SCRIPT_FILE.read_text()
    assert "system" in source, (
        "broadcast.py must include a message with type 'system'"
    )


def test_script_has_maintenance_message():
    source = SCRIPT_FILE.read_text()
    assert "maintenance" in source.lower(), (
        "broadcast.py must include a maintenance-related message"
    )


def test_script_references_log_file():
    source = SCRIPT_FILE.read_text()
    assert "broadcast.log" in source, (
        "broadcast.py must write logs to broadcast.log"
    )


def test_script_uses_livekit_api():
    source = SCRIPT_FILE.read_text()
    assert "LiveKitAPI" in source or "api.LiveKitAPI" in source, (
        "broadcast.py must use LiveKitAPI context manager"
    )


def test_broadcast_log_created_after_run():
    python_path = shutil.which("python3")
    assert python_path is not None, "python3 must be installed"

    env = os.environ.copy()
    # Load from .env.local if keys not already set
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env.setdefault(k.strip(), v.strip())

    result = subprocess.run(
        [python_path, "broadcast.py"],
        cwd=str(PROJECT_DIR),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )

    # Script may fail due to network issues in test env; we still check log was created
    assert LOG_FILE.is_file(), (
        f"broadcast.log was not created at {LOG_FILE} after running broadcast.py. "
        f"stdout: {result.stdout[:200]}, stderr: {result.stderr[:200]}"
    )


def test_broadcast_log_has_valid_content():
    if not LOG_FILE.is_file():
        pytest.skip("broadcast.log does not exist — run test_broadcast_log_created_after_run first")

    content = LOG_FILE.read_text()
    assert "Broadcast sent to" in content or "No active rooms found" in content, (
        "broadcast.log must contain 'Broadcast sent to <room>' or 'No active rooms found'"
    )
