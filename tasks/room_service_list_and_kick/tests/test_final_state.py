import os
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
SCRIPT_FILE = PROJECT_DIR / "list_and_kick.mjs"
LOG_FILE = PROJECT_DIR / "output.log"


def test_script_exists():
    assert SCRIPT_FILE.exists(), f"{SCRIPT_FILE} does not exist"


def test_output_log_exists():
    assert LOG_FILE.exists(), f"{LOG_FILE} does not exist"


def test_output_log_not_empty():
    content = LOG_FILE.read_text().strip()
    assert len(content) > 0, "output.log must not be empty"


def test_output_log_contains_active_rooms():
    content = LOG_FILE.read_text()
    assert "Active rooms:" in content, \
        "output.log must contain the 'Active rooms:' log line"


def test_output_log_contains_removed_participant():
    content = LOG_FILE.read_text()
    assert "Removed participant banned-user" in content, \
        "output.log must contain 'Removed participant banned-user'"


def test_output_log_contains_live_session():
    content = LOG_FILE.read_text()
    assert "live-session" in content, \
        "output.log must mention 'live-session'"


def test_script_contains_list_rooms():
    content = SCRIPT_FILE.read_text()
    assert "listRooms" in content, \
        "list_and_kick.mjs must call listRooms()"


def test_script_contains_remove_participant():
    content = SCRIPT_FILE.read_text()
    assert "removeParticipant" in content, \
        "list_and_kick.mjs must call removeParticipant()"


def test_script_contains_banned_user():
    content = SCRIPT_FILE.read_text()
    assert "banned-user" in content, \
        "list_and_kick.mjs must reference the participant 'banned-user'"


def test_script_contains_live_session():
    content = SCRIPT_FILE.read_text()
    assert "live-session" in content, \
        "list_and_kick.mjs must reference the room 'live-session'"


def test_script_contains_room_service_client():
    content = SCRIPT_FILE.read_text()
    assert "RoomServiceClient" in content, \
        "list_and_kick.mjs must use RoomServiceClient"


def test_script_contains_output_log_write():
    content = SCRIPT_FILE.read_text()
    assert "output.log" in content, \
        "list_and_kick.mjs must write to output.log"


def test_script_has_error_handling():
    content = SCRIPT_FILE.read_text()
    assert "try" in content and "catch" in content, \
        "list_and_kick.mjs must have try/catch error handling for removeParticipant"


def test_active_rooms_line_has_number():
    content = LOG_FILE.read_text()
    import re
    match = re.search(r'Active rooms:\s*(\d+)', content)
    assert match is not None, \
        "output.log 'Active rooms:' line must be followed by a non-negative integer"
