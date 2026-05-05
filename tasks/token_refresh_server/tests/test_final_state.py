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
SCRIPT_FILE = PROJECT_DIR / "server.js"
SERVER_PORT = 3000
SERVER_URL = f"http://localhost:{SERVER_PORT}"


def test_server_js_exists():
    assert SCRIPT_FILE.is_file(), f"server.js not found at {SCRIPT_FILE}"


def test_script_uses_access_token():
    source = SCRIPT_FILE.read_text()
    assert "AccessToken" in source, "server.js must use AccessToken from livekit-server-sdk"


def test_script_has_ttl_30m():
    source = SCRIPT_FILE.read_text()
    assert "30m" in source, "server.js must set ttl: '30m' on AccessToken"


def test_script_listens_on_port_3000():
    source = SCRIPT_FILE.read_text()
    assert "3000" in source, "server.js must listen on port 3000"


def test_script_has_token_endpoint():
    source = SCRIPT_FILE.read_text()
    assert "/token" in source, "server.js must define a GET /token route"


def test_script_has_refresh_endpoint():
    source = SCRIPT_FILE.read_text()
    assert "/refresh" in source, "server.js must define a POST /refresh route"


def test_script_has_health_endpoint():
    source = SCRIPT_FILE.read_text()
    assert "/health" in source, "server.js must define a GET /health route"


def _start_server():
    node_path = shutil.which("node")
    assert node_path is not None, "node must be installed"
    env = os.environ.copy()
    env.setdefault("LIVEKIT_API_KEY", "test-api-key")
    env.setdefault("LIVEKIT_API_SECRET", "test-api-secret-at-least-32-chars-long!")
    proc = subprocess.Popen(
        [node_path, "server.js"],
        cwd=str(PROJECT_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)
    return proc


def test_health_endpoint_returns_ok():
    proc = _start_server()
    try:
        url = f"{SERVER_URL}/health"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            pytest.fail(f"GET /health returned HTTP {e.code}")

        assert status == 200, f"Expected 200, got {status}"
        data = json.loads(body)
        assert data.get("status") == "ok", f"Expected {{status: 'ok'}}, got {data}"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_token_endpoint_returns_token_and_expires_in():
    proc = _start_server()
    try:
        url = f"{SERVER_URL}/token?room=test&identity=bob"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            pytest.fail(f"GET /token returned HTTP {e.code}: {body}")

        assert status == 200, f"Expected 200, got {status}"
        data = json.loads(body)

        assert "token" in data, f"Response must have a 'token' field, got: {data}"
        assert data.get("expiresIn") == "30m", (
            f"Response must have expiresIn: '30m', got: {data}"
        )

        jwt = data["token"]
        parts = jwt.split(".")
        assert len(parts) == 3, f"Token must be a JWT with 3 parts, got: {jwt[:80]}"

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_refresh_endpoint_returns_refreshed_true():
    proc = _start_server()
    try:
        url = f"{SERVER_URL}/refresh"
        payload = json.dumps({"room": "test", "identity": "bob"}).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=5) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            pytest.fail(f"POST /refresh returned HTTP {e.code}: {body}")

        assert status == 200, f"Expected 200, got {status}"
        data = json.loads(body)

        assert "token" in data, f"Response must have a 'token' field, got: {data}"
        assert data.get("refreshed") is True, (
            f"Response must have refreshed: true, got: {data}"
        )

        jwt = data["token"]
        parts = jwt.split(".")
        assert len(parts) == 3, f"Refreshed token must be a valid JWT"

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
