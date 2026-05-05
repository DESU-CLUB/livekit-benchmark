import os
import re
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-token")
TOKEN_FILE = PROJECT_DIR / "token.txt"
SCRIPT_FILE = PROJECT_DIR / "generate_token.py"


def test_generate_token_script_exists():
    assert SCRIPT_FILE.is_file(), f"generate_token.py not found at {SCRIPT_FILE}"


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


def test_script_uses_livekit_api():
    source = SCRIPT_FILE.read_text()
    assert "livekit" in source.lower(), "generate_token.py must import from livekit"
    assert "AccessToken" in source or "access_token" in source.lower(), (
        "generate_token.py must use AccessToken"
    )


def test_script_targets_correct_room():
    source = SCRIPT_FILE.read_text()
    assert "test-room" in source, "generate_token.py must reference room 'test-room'"


def test_script_targets_correct_identity():
    source = SCRIPT_FILE.read_text()
    assert "test-user" in source, "generate_token.py must reference identity 'test-user'"
