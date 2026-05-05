import json
import os
import shutil
import subprocess
import time
import urllib.request
import urllib.error
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-permissions")
SCRIPT_FILE = PROJECT_DIR / "server.js"
SERVER_PORT = 3000
SERVER_URL = f"http://localhost:{SERVER_PORT}"


def test_server_js_exists():
    assert SCRIPT_FILE.is_file(), f"server.js not found at {SCRIPT_FILE}"


def test_script_uses_room_service_client():
    source = SCRIPT_FILE.read_text()
    assert "RoomServiceClient" in source, (
        "server.js must use RoomServiceClient from livekit-server-sdk"
    )


def test_script_uses_update_participant():
    source = SCRIPT_FILE.read_text()
    assert "updateParticipant" in source, (
        "server.js must call updateParticipant to change participant permissions"
    )


def test_script_references_can_publish():
    source = SCRIPT_FILE.read_text()
    assert "canPublish" in source, (
        "server.js must reference canPublish in participant permission update"
    )


def test_script_uses_map_for_state():
    source = SCRIPT_FILE.read_text()
    assert "Map" in source, (
        "server.js must use a Map to track in-memory hand raise state"
    )


def test_script_listens_on_port_3000():
    source = SCRIPT_FILE.read_text()
    assert "3000" in source, "server.js must listen on port 3000"


def test_script_has_hand_raise_route():
    source = SCRIPT_FILE.read_text()
    assert "/hand-raise" in source, (
        "server.js must define a POST /hand-raise route"
    )


def test_script_has_hands_up_route():
    source = SCRIPT_FILE.read_text()
    assert "/hands-up" in source, (
        "server.js must define a GET /hands-up route"
    )


def test_hands_up_returns_json_array():
    node_path = shutil.which("node")
    assert node_path is not None, "node must be installed"

    env = os.environ.copy()
    env.setdefault("LIVEKIT_URL", "wss://test.livekit.cloud")
    env.setdefault("LIVEKIT_API_KEY", "test-api-key")
    env.setdefault("LIVEKIT_API_SECRET", "test-api-secret-that-is-long-enough-32chars")

    proc = subprocess.Popen(
        [node_path, "server.js"],
        cwd=str(PROJECT_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)

        try:
            with urllib.request.urlopen(
                f"{SERVER_URL}/hands-up", timeout=5
            ) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            pytest.fail(f"GET /hands-up returned HTTP {e.code}: {body}")

        assert status == 200, f"Expected HTTP 200, got {status}"

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {body[:200]}")

        assert isinstance(data, list), (
            f"GET /hands-up must return a JSON array, got: {type(data).__name__}"
        )

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_hand_raise_returns_400_without_identity():
    node_path = shutil.which("node")
    assert node_path is not None, "node must be installed"

    env = os.environ.copy()
    env.setdefault("LIVEKIT_URL", "wss://test.livekit.cloud")
    env.setdefault("LIVEKIT_API_KEY", "test-api-key")
    env.setdefault("LIVEKIT_API_SECRET", "test-api-secret-that-is-long-enough-32chars")

    proc = subprocess.Popen(
        [node_path, "server.js"],
        cwd=str(PROJECT_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)

        payload = json.dumps({"room": "my-room"}).encode()
        request = urllib.request.Request(
            f"{SERVER_URL}/hand-raise",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        status = None
        try:
            with urllib.request.urlopen(request, timeout=5) as resp:
                status = resp.status
        except urllib.error.HTTPError as e:
            status = e.code

        assert status == 400, (
            f"POST /hand-raise without 'identity' must return 400, got {status}"
        )

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
