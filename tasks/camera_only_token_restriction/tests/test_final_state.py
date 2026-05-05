import os
import re
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-token")
SCRIPT_FILE = PROJECT_DIR / "camera_token.py"
TOKEN_FILE = PROJECT_DIR / "token.txt"

JWT_PATTERN = re.compile(r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$')


def test_script_exists():
    assert SCRIPT_FILE.exists(), f"{SCRIPT_FILE} does not exist"


def test_token_file_exists():
    assert TOKEN_FILE.exists(), f"{TOKEN_FILE} does not exist"


def test_token_file_not_empty():
    content = TOKEN_FILE.read_text().strip()
    assert len(content) > 0, "token.txt must not be empty"


def test_token_is_valid_jwt():
    content = TOKEN_FILE.read_text().strip()
    assert JWT_PATTERN.match(content), \
        f"token.txt must contain a valid JWT (3 dot-separated base64url segments), got: {content[:80]}"


def test_script_contains_can_publish_sources():
    content = SCRIPT_FILE.read_text()
    assert "can_publish_sources" in content, \
        "camera_token.py must use can_publish_sources to restrict publish tracks"


def test_script_contains_camera_source():
    content = SCRIPT_FILE.read_text()
    assert '"camera"' in content or "'camera'" in content, \
        "camera_token.py must include 'camera' in the publish sources"


def test_script_contains_video_only_user():
    content = SCRIPT_FILE.read_text()
    assert "video-only-user" in content, \
        "camera_token.py must set participant identity to 'video-only-user'"


def test_script_contains_broadcast_room():
    content = SCRIPT_FILE.read_text()
    assert "broadcast" in content, \
        "camera_token.py must target the 'broadcast' room"


def test_script_contains_access_token():
    content = SCRIPT_FILE.read_text()
    assert "AccessToken" in content, \
        "camera_token.py must use AccessToken from livekit"


def test_script_contains_token_txt_write():
    content = SCRIPT_FILE.read_text()
    assert "token.txt" in content, \
        "camera_token.py must write the JWT to token.txt"


def test_script_does_not_allow_microphone():
    content = SCRIPT_FILE.read_text()
    # Script should NOT include microphone in can_publish_sources
    assert "microphone" not in content, \
        "camera_token.py must NOT include 'microphone' in can_publish_sources"


def test_script_does_not_allow_screen_share():
    content = SCRIPT_FILE.read_text()
    assert "screen_share" not in content and "screenShare" not in content, \
        "camera_token.py must NOT include screen_share in can_publish_sources"


def test_script_imports_livekit():
    content = SCRIPT_FILE.read_text()
    assert "livekit" in content, \
        "camera_token.py must import from the livekit package"
