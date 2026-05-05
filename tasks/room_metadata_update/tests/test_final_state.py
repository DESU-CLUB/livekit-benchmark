import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
SCRIPT_FILE = PROJECT_DIR / "update_metadata.mjs"
LOG_FILE = PROJECT_DIR / "output.log"


def test_update_metadata_script_exists():
    assert SCRIPT_FILE.is_file(), f"update_metadata.mjs not found at {SCRIPT_FILE}"


def test_script_uses_room_service_client():
    source = SCRIPT_FILE.read_text()
    assert "RoomServiceClient" in source, (
        "update_metadata.mjs must import and use RoomServiceClient"
    )


def test_script_calls_update_room_metadata():
    source = SCRIPT_FILE.read_text()
    assert "updateRoomMetadata" in source, (
        "update_metadata.mjs must call updateRoomMetadata"
    )


def test_script_targets_conference_room():
    source = SCRIPT_FILE.read_text()
    assert "conference-room" in source, (
        "update_metadata.mjs must target room 'conference-room'"
    )


def test_script_reads_env_vars():
    source = SCRIPT_FILE.read_text()
    assert "LIVEKIT_URL" in source or "process.env" in source, (
        "update_metadata.mjs must read LIVEKIT_URL from environment variables"
    )


def test_output_log_exists():
    assert LOG_FILE.is_file(), f"output.log not found at {LOG_FILE}"


def test_output_log_contains_success_message():
    content = LOG_FILE.read_text()
    assert "Metadata updated successfully" in content, (
        "output.log must contain 'Metadata updated successfully'"
    )
