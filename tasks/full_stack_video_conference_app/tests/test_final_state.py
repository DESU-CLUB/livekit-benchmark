import json
import os
import re
import shutil
import socket
import subprocess
import time
import urllib.request
import urllib.error
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-meet")
BACKEND_DIR = PROJECT_DIR / "backend"
FRONTEND_DIR = PROJECT_DIR / "frontend"
BACKEND_PORT = 3001
FRONTEND_PORT = 5173


def _wait_for_port(port: int, host: str = "localhost", timeout: float = 30.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def test_backend_dir_exists():
    assert BACKEND_DIR.is_dir(), f"Backend directory not found at {BACKEND_DIR}"


def test_frontend_dir_exists():
    assert FRONTEND_DIR.is_dir(), f"Frontend directory not found at {FRONTEND_DIR}"


def test_backend_entry_point_exists():
    entry = BACKEND_DIR / "index.js"
    assert entry.is_file(), f"Backend entry point not found at {entry}"


def test_backend_uses_access_token():
    entry = BACKEND_DIR / "index.js"
    source = entry.read_text()
    assert "AccessToken" in source, "backend/index.js must use AccessToken from livekit-server-sdk"


def test_backend_listens_on_port_3001():
    entry = BACKEND_DIR / "index.js"
    source = entry.read_text()
    assert "3001" in source, "backend/index.js must listen on port 3001"


def test_frontend_has_livekit_room_component():
    # Search all js/jsx/ts/tsx files for LiveKitRoom
    found = False
    src_dir = FRONTEND_DIR / "src"
    if not src_dir.is_dir():
        src_dir = FRONTEND_DIR
    for ext in ("*.jsx", "*.tsx", "*.js", "*.ts"):
        for f in src_dir.rglob(ext):
            if "LiveKitRoom" in f.read_text():
                found = True
                break
        if found:
            break
    assert found, "Frontend source must contain LiveKitRoom component"


def test_frontend_has_video_conference_component():
    found = False
    src_dir = FRONTEND_DIR / "src"
    if not src_dir.is_dir():
        src_dir = FRONTEND_DIR
    for ext in ("*.jsx", "*.tsx", "*.js", "*.ts"):
        for f in src_dir.rglob(ext):
            if "VideoConference" in f.read_text():
                found = True
                break
        if found:
            break
    assert found, "Frontend source must contain VideoConference component"


def test_backend_token_endpoint():
    node_path = shutil.which("node")
    assert node_path is not None, "node must be installed"

    env = os.environ.copy()
    env.setdefault("LIVEKIT_API_KEY", "test-api-key")
    env.setdefault("LIVEKIT_API_SECRET", "test-api-secret-at-least-32-chars-long")
    env.setdefault("LIVEKIT_URL", "wss://test.livekit.cloud")

    proc = subprocess.Popen(
        [node_path, "index.js"],
        cwd=str(BACKEND_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        assert _wait_for_port(BACKEND_PORT, timeout=15), (
            f"Backend did not start on port {BACKEND_PORT} within 15 seconds"
        )

        token_url = f"http://localhost:{BACKEND_PORT}/token?room=test&identity=user1"
        try:
            with urllib.request.urlopen(token_url, timeout=5) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            pytest.fail(f"GET /token returned HTTP {e.code}: {body}")

        assert status == 200, f"Expected HTTP 200, got {status}"

        data = json.loads(body)
        assert "token" in data, f"Response must have a 'token' field, got: {data}"

        jwt = data["token"]
        parts = jwt.split(".")
        assert len(parts) == 3, f"Token must be a JWT with 3 parts, got: {jwt[:80]}"

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_frontend_package_json_has_livekit_components():
    pkg_json = FRONTEND_DIR / "package.json"
    assert pkg_json.is_file(), "frontend/package.json not found"
    data = json.loads(pkg_json.read_text())
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    assert "@livekit/components-react" in deps, (
        "frontend/package.json must list @livekit/components-react as a dependency"
    )


def test_frontend_package_json_has_livekit_client():
    pkg_json = FRONTEND_DIR / "package.json"
    data = json.loads(pkg_json.read_text())
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    assert "livekit-client" in deps, (
        "frontend/package.json must list livekit-client as a dependency"
    )
