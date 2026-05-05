import json
import os
import shutil
import subprocess
import time
import urllib.request
import urllib.error
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-egress-server")
SCRIPT_FILE = PROJECT_DIR / "server.js"
SERVER_PORT = 5000
SERVER_URL = f"http://localhost:{SERVER_PORT}"


def test_server_js_exists():
    assert SCRIPT_FILE.is_file(), f"server.js not found at {SCRIPT_FILE}"


def test_script_uses_egress_client():
    source = SCRIPT_FILE.read_text()
    assert "EgressClient" in source, (
        "server.js must use EgressClient from livekit-server-sdk"
    )


def test_script_uses_start_room_composite_egress():
    source = SCRIPT_FILE.read_text()
    assert "startRoomCompositeEgress" in source, (
        "server.js must call startRoomCompositeEgress"
    )


def test_script_uses_encoded_file_output():
    source = SCRIPT_FILE.read_text()
    assert "EncodedFileOutput" in source, (
        "server.js must use EncodedFileOutput for egress file configuration"
    )


def test_script_uses_stop_egress():
    source = SCRIPT_FILE.read_text()
    assert "stopEgress" in source, (
        "server.js must call stopEgress for the stop-recording endpoint"
    )


def test_script_listens_on_port_5000():
    source = SCRIPT_FILE.read_text()
    assert "5000" in source, "server.js must listen on port 5000"


def test_script_has_start_recording_route():
    source = SCRIPT_FILE.read_text()
    assert "/start-recording" in source, (
        "server.js must define a POST /start-recording route"
    )


def test_script_has_stop_recording_route():
    source = SCRIPT_FILE.read_text()
    assert "/stop-recording" in source, (
        "server.js must define a POST /stop-recording/:egressId route"
    )


def test_start_recording_returns_egress_id():
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

        payload = json.dumps({"room": "test-room", "filepath": "/tmp/recording.mp4"}).encode()
        request = urllib.request.Request(
            f"{SERVER_URL}/start-recording",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            pytest.fail(f"POST /start-recording returned HTTP {e.code}: {body}")

        assert status == 200, f"Expected HTTP 200, got {status}. Body: {body[:200]}"

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {body[:200]}")

        assert "egressId" in data, (
            f"Response JSON must have an 'egressId' field, got: {data}"
        )

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_start_recording_returns_400_without_room():
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

        payload = json.dumps({"filepath": "/tmp/recording.mp4"}).encode()
        request = urllib.request.Request(
            f"{SERVER_URL}/start-recording",
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
            f"POST /start-recording without 'room' must return 400, got {status}"
        )

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
