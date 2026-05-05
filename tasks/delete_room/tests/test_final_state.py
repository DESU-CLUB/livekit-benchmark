import os
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
SCRIPT_FILE = PROJECT_DIR / "delete_room.js"
LOG_FILE = PROJECT_DIR / "output.log"


def test_delete_room_script_exists():
    assert SCRIPT_FILE.is_file(), f"delete_room.js not found at {SCRIPT_FILE}"


def test_output_log_exists():
    assert LOG_FILE.is_file(), f"output.log not found at {LOG_FILE}"


def test_output_log_contains_success_message():
    content = LOG_FILE.read_text()
    assert "Room deleted successfully" in content, (
        f"output.log must contain 'Room deleted successfully', got: {content[:200]}"
    )


def test_script_uses_room_service_client():
    source = SCRIPT_FILE.read_text()
    assert "RoomServiceClient" in source, (
        "delete_room.js must use RoomServiceClient from livekit-server-sdk"
    )


def test_script_imports_livekit_server_sdk():
    source = SCRIPT_FILE.read_text()
    assert "livekit-server-sdk" in source, (
        "delete_room.js must import from 'livekit-server-sdk'"
    )


def test_script_targets_correct_room():
    source = SCRIPT_FILE.read_text()
    assert "old-meeting-room" in source, (
        "delete_room.js must reference 'old-meeting-room'"
    )


def test_script_uses_environment_variables():
    source = SCRIPT_FILE.read_text()
    assert "LIVEKIT_URL" in source or "process.env" in source, (
        "delete_room.js must read LiveKit credentials from environment variables"
    )
