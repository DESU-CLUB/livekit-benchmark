import json
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
SCRIPT_FILE = PROJECT_DIR / "list_participants.mjs"
OUTPUT_FILE = PROJECT_DIR / "participants.json"


def test_list_participants_script_exists():
    assert SCRIPT_FILE.is_file(), f"list_participants.mjs not found at {SCRIPT_FILE}"


def test_script_uses_room_service_client():
    source = SCRIPT_FILE.read_text()
    assert "RoomServiceClient" in source, (
        "list_participants.mjs must import and use RoomServiceClient"
    )


def test_script_calls_list_participants():
    source = SCRIPT_FILE.read_text()
    assert "listParticipants" in source, (
        "list_participants.mjs must call listParticipants"
    )


def test_script_targets_main_room():
    source = SCRIPT_FILE.read_text()
    assert "main-room" in source, (
        "list_participants.mjs must target room 'main-room'"
    )


def test_participants_json_exists():
    assert OUTPUT_FILE.is_file(), f"participants.json not found at {OUTPUT_FILE}"


def test_participants_json_is_valid_json():
    content = OUTPUT_FILE.read_text().strip()
    assert len(content) > 0, "participants.json must not be empty"
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise AssertionError(
            f"participants.json is not valid JSON: {e}\nContent: {content[:200]}"
        )


def test_participants_json_is_array():
    content = OUTPUT_FILE.read_text().strip()
    data = json.loads(content)
    assert isinstance(data, list), (
        f"participants.json must be a JSON array, got: {type(data).__name__}"
    )
