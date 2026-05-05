import json
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-rooms")
ROOMS_FILE = PROJECT_DIR / "rooms.json"


def test_rooms_json_exists():
    assert ROOMS_FILE.is_file(), f"rooms.json not found at {ROOMS_FILE}"


def test_rooms_json_not_empty():
    content = ROOMS_FILE.read_text().strip()
    assert len(content) > 0, "rooms.json must not be empty"


def test_rooms_json_is_valid_json():
    content = ROOMS_FILE.read_text().strip()
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        pytest.fail(f"rooms.json is not valid JSON: {e}")


def test_rooms_json_is_array():
    content = ROOMS_FILE.read_text().strip()
    data = json.loads(content)
    assert isinstance(data, list), (
        f"rooms.json must be a JSON array at the top level, got {type(data).__name__}"
    )
