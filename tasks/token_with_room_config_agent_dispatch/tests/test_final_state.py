import os
import re
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
SCRIPT_FILE = PROJECT_DIR / "dispatch_token.mjs"
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


def test_script_contains_room_configuration():
    content = SCRIPT_FILE.read_text()
    assert "RoomConfiguration" in content, \
        "dispatch_token.mjs must use RoomConfiguration"


def test_script_contains_room_agent_dispatch():
    content = SCRIPT_FILE.read_text()
    assert "RoomAgentDispatch" in content, \
        "dispatch_token.mjs must use RoomAgentDispatch"


def test_script_contains_my_agent():
    content = SCRIPT_FILE.read_text()
    assert "my-agent" in content, \
        "dispatch_token.mjs must reference agent name 'my-agent'"


def test_script_contains_host_user():
    content = SCRIPT_FILE.read_text()
    assert "host-user" in content, \
        "dispatch_token.mjs must set participant identity to 'host-user'"


def test_script_contains_ai_room():
    content = SCRIPT_FILE.read_text()
    assert "ai-room" in content, \
        "dispatch_token.mjs must set room name to 'ai-room'"


def test_script_contains_access_token():
    content = SCRIPT_FILE.read_text()
    assert "AccessToken" in content, \
        "dispatch_token.mjs must use AccessToken from livekit-server-sdk"


def test_script_contains_room_config_assignment():
    content = SCRIPT_FILE.read_text()
    assert "roomConfig" in content, \
        "dispatch_token.mjs must set at.roomConfig"


def test_script_contains_to_jwt():
    content = SCRIPT_FILE.read_text()
    assert "toJwt" in content, \
        "dispatch_token.mjs must call at.toJwt()"


def test_script_contains_token_txt_write():
    content = SCRIPT_FILE.read_text()
    assert "token.txt" in content, \
        "dispatch_token.mjs must write to token.txt"


def test_script_imports_livekit_protocol():
    content = SCRIPT_FILE.read_text()
    assert "@livekit/protocol" in content, \
        "dispatch_token.mjs must import from @livekit/protocol"
