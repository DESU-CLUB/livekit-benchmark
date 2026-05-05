import os
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
SCRIPT_FILE = PROJECT_DIR / "remove_participant.py"
LOG_FILE = PROJECT_DIR / "output.log"


def test_remove_participant_script_exists():
    assert SCRIPT_FILE.is_file(), f"remove_participant.py not found at {SCRIPT_FILE}"


def test_output_log_exists():
    assert LOG_FILE.is_file(), f"output.log not found at {LOG_FILE}"


def test_output_log_not_empty():
    content = LOG_FILE.read_text().strip()
    assert len(content) > 0, "output.log must not be empty"


def test_script_imports_livekit_api():
    source = SCRIPT_FILE.read_text()
    assert "livekit" in source.lower(), (
        "remove_participant.py must import from livekit"
    )


def test_script_uses_remove_participant():
    source = SCRIPT_FILE.read_text()
    assert "remove_participant" in source, (
        "remove_participant.py must call the remove_participant method"
    )


def test_script_targets_correct_room():
    source = SCRIPT_FILE.read_text()
    assert "demo-room" in source, (
        "remove_participant.py must reference room 'demo-room'"
    )


def test_script_targets_correct_identity():
    source = SCRIPT_FILE.read_text()
    assert "user-123" in source, (
        "remove_participant.py must reference identity 'user-123'"
    )


def test_script_uses_livekit_api_context_manager():
    source = SCRIPT_FILE.read_text()
    assert "LiveKitAPI" in source, (
        "remove_participant.py must use LiveKitAPI"
    )
