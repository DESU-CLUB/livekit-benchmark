import json
import os
import shutil
import subprocess
import time
import urllib.request
import urllib.error
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-webhook")
SCRIPT_FILE = PROJECT_DIR / "server.js"
EVENTS_LOG = PROJECT_DIR / "events.log"
SERVER_PORT = 4000
SERVER_URL = f"http://localhost:{SERVER_PORT}"


def test_server_js_exists():
    assert SCRIPT_FILE.is_file(), f"server.js not found at {SCRIPT_FILE}"


def test_script_uses_webhook_receiver():
    source = SCRIPT_FILE.read_text()
    assert "WebhookReceiver" in source, (
        "server.js must use WebhookReceiver from livekit-server-sdk"
    )


def test_script_uses_express_raw_middleware():
    source = SCRIPT_FILE.read_text()
    assert "express.raw" in source, (
        "server.js must use express.raw() middleware for raw body parsing on webhook route"
    )


def test_script_references_events_log():
    source = SCRIPT_FILE.read_text()
    assert "events.log" in source, (
        "server.js must reference events.log for logging webhook events"
    )


def test_script_listens_on_port_4000():
    source = SCRIPT_FILE.read_text()
    assert "4000" in source, "server.js must listen on port 4000"


def test_script_has_room_started_handler():
    source = SCRIPT_FILE.read_text()
    assert "room_started" in source, (
        "server.js must handle the room_started event"
    )


def test_script_has_room_finished_handler():
    source = SCRIPT_FILE.read_text()
    assert "room_finished" in source, (
        "server.js must handle the room_finished event"
    )


def test_script_has_participant_joined_handler():
    source = SCRIPT_FILE.read_text()
    assert "participant_joined" in source, (
        "server.js must handle the participant_joined event"
    )


def test_script_has_participant_left_handler():
    source = SCRIPT_FILE.read_text()
    assert "participant_left" in source, (
        "server.js must handle the participant_left event"
    )


def test_script_has_track_published_handler():
    source = SCRIPT_FILE.read_text()
    assert "track_published" in source, (
        "server.js must handle the track_published event"
    )


def test_health_endpoint_returns_ok():
    node_path = shutil.which("node")
    assert node_path is not None, "node must be installed"

    env = os.environ.copy()
    env.setdefault("LIVEKIT_API_KEY", "test-api-key")
    env.setdefault("LIVEKIT_API_SECRET", "test-api-secret")

    proc = subprocess.Popen(
        [node_path, "server.js"],
        cwd=str(PROJECT_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)

        health_url = f"{SERVER_URL}/health"
        try:
            with urllib.request.urlopen(health_url, timeout=5) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            pytest.fail(f"GET /health returned HTTP {e.code}: {body}")

        assert status == 200, f"Expected HTTP 200, got {status}"

        data = json.loads(body)
        assert data.get("status") == "ok", f"Expected {{status: 'ok'}}, got {data}"

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_unauthorized_webhook_returns_401():
    node_path = shutil.which("node")
    assert node_path is not None, "node must be installed"

    env = os.environ.copy()
    env.setdefault("LIVEKIT_API_KEY", "test-api-key")
    env.setdefault("LIVEKIT_API_SECRET", "test-api-secret")

    proc = subprocess.Popen(
        [node_path, "server.js"],
        cwd=str(PROJECT_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)

        webhook_url = f"{SERVER_URL}/webhook"
        request = urllib.request.Request(
            webhook_url,
            data=b'{"event":"room_started","room":{}}',
            headers={
                "Content-Type": "application/webhook+json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=5) as resp:
                status = resp.status
        except urllib.error.HTTPError as e:
            status = e.code

        assert status == 401, (
            f"POST /webhook with no/invalid Authorization header must return 401, got {status}"
        )

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
