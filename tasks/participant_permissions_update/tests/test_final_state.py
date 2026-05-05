import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
SCRIPT_FILE = PROJECT_DIR / "update_permissions.py"
LOG_FILE = PROJECT_DIR / "output.log"


def test_update_permissions_script_exists():
    assert SCRIPT_FILE.is_file(), f"update_permissions.py not found at {SCRIPT_FILE}"


def test_script_calls_update_participant():
    source = SCRIPT_FILE.read_text()
    assert "update_participant" in source, (
        "update_permissions.py must call update_participant"
    )


def test_script_targets_speaker_identity():
    source = SCRIPT_FILE.read_text()
    assert "speaker-1" in source, (
        "update_permissions.py must reference identity 'speaker-1'"
    )


def test_script_targets_stage_room():
    source = SCRIPT_FILE.read_text()
    assert "stage-room" in source, (
        "update_permissions.py must reference room 'stage-room'"
    )


def test_script_sets_can_publish_true():
    source = SCRIPT_FILE.read_text()
    assert "can_publish=True" in source, (
        "update_permissions.py must set can_publish=True"
    )


def test_script_uses_livekit_api():
    source = SCRIPT_FILE.read_text()
    assert "LiveKitAPI" in source or "livekit" in source.lower(), (
        "update_permissions.py must use the LiveKit API client"
    )


def test_output_log_exists():
    assert LOG_FILE.is_file(), f"output.log not found at {LOG_FILE}"


def test_output_log_contains_success_message():
    content = LOG_FILE.read_text()
    assert "Permissions updated" in content, (
        "output.log must contain 'Permissions updated'"
    )
