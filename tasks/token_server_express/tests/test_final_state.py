import json
import os
import re
import shutil
import subprocess
import time
import urllib.request
import urllib.error
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-token-server")
SCRIPT_FILE = PROJECT_DIR / "index.js"
SERVER_PORT = 3000
SERVER_URL = f"http://localhost:{SERVER_PORT}"


def test_index_js_exists():
    assert SCRIPT_FILE.is_file(), f"index.js not found at {SCRIPT_FILE}"


def test_script_uses_access_token():
    source = SCRIPT_FILE.read_text()
    assert "AccessToken" in source, "index.js must use AccessToken from livekit-server-sdk"


def test_script_uses_express():
    source = SCRIPT_FILE.read_text()
    assert "express" in source.lower(), "index.js must use express"


def test_script_listens_on_port_3000():
    source = SCRIPT_FILE.read_text()
    assert "3000" in source, "index.js must listen on port 3000"


def test_script_has_token_endpoint():
    source = SCRIPT_FILE.read_text()
    assert "/token" in source, "index.js must define a /token route"


def test_token_endpoint_returns_jwt():
    node_path = shutil.which("node")
    assert node_path is not None, "node must be installed"

    env = os.environ.copy()
    env.setdefault("LIVEKIT_API_KEY", "test-api-key")
    env.setdefault("LIVEKIT_API_SECRET", "test-api-secret")

    proc = subprocess.Popen(
        [node_path, "index.js"],
        cwd=str(PROJECT_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)

        token_url = f"{SERVER_URL}/token?room=test-room&identity=alice"
        try:
            with urllib.request.urlopen(token_url, timeout=5) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            pytest.fail(f"GET /token returned HTTP {e.code}: {body}")

        assert status == 200, f"Expected HTTP 200, got {status}"

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {body[:200]}")

        assert "token" in data, f"Response JSON must have a 'token' field, got: {data}"

        jwt = data["token"]
        parts = jwt.split(".")
        assert len(parts) == 3, f"Token must be a JWT with 3 parts, got: {jwt[:80]}"

        base64url_pattern = re.compile(r"^[A-Za-z0-9\-_]+$")
        for i, part in enumerate(parts):
            assert len(part) > 0, f"JWT part {i} must not be empty"
            assert base64url_pattern.match(part), f"JWT part {i} is not valid base64url"

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
