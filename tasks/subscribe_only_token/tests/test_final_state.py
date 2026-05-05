import re
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-token")
SCRIPT_FILE = PROJECT_DIR / "subscribe_only.py"
TOKEN_FILE = PROJECT_DIR / "token.txt"


def test_subscribe_only_script_exists():
    assert SCRIPT_FILE.is_file(), f"subscribe_only.py not found at {SCRIPT_FILE}"


def test_script_sets_can_publish_false():
    source = SCRIPT_FILE.read_text()
    assert "can_publish=False" in source or "canPublish: false" in source, (
        "subscribe_only.py must set can_publish=False (or canPublish: false)"
    )


def test_script_sets_can_subscribe_true():
    source = SCRIPT_FILE.read_text()
    assert "can_subscribe=True" in source or "canSubscribe: true" in source, (
        "subscribe_only.py must set can_subscribe=True (or canSubscribe: true)"
    )


def test_script_uses_viewer_identity():
    source = SCRIPT_FILE.read_text()
    assert "viewer-1" in source, "subscribe_only.py must use identity 'viewer-1'"


def test_script_uses_broadcast_room():
    source = SCRIPT_FILE.read_text()
    assert "broadcast-room" in source, (
        "subscribe_only.py must target room 'broadcast-room'"
    )


def test_script_uses_livekit_access_token():
    source = SCRIPT_FILE.read_text()
    assert "livekit" in source.lower(), "subscribe_only.py must import from livekit"
    assert "AccessToken" in source or "access_token" in source.lower(), (
        "subscribe_only.py must use AccessToken"
    )


def test_token_file_exists():
    assert TOKEN_FILE.is_file(), f"token.txt not found at {TOKEN_FILE}"


def test_token_file_not_empty():
    content = TOKEN_FILE.read_text().strip()
    assert len(content) > 0, "token.txt must not be empty"


def test_token_is_valid_jwt_format():
    content = TOKEN_FILE.read_text().strip()
    parts = content.split(".")
    assert len(parts) == 3, (
        f"JWT must have exactly 3 dot-separated parts, got {len(parts)}: {content[:80]}"
    )
    base64url_pattern = re.compile(r"^[A-Za-z0-9\-_]+$")
    for i, part in enumerate(parts):
        assert len(part) > 0, f"JWT part {i} must not be empty"
        assert base64url_pattern.match(part), (
            f"JWT part {i} is not valid base64url: {part[:40]}"
        )
