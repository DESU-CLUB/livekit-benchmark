import os
import json
import time
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-webhook")
SERVER_FILE = PROJECT_DIR / "server.js"


def test_server_js_exists():
    assert SERVER_FILE.exists(), f"{SERVER_FILE} does not exist"


def test_server_contains_participant_events_table():
    content = SERVER_FILE.read_text()
    assert "participant_events" in content, \
        "server.js must define the participant_events table"


def test_server_contains_webhook_receiver():
    content = SERVER_FILE.read_text()
    assert "WebhookReceiver" in content, \
        "server.js must use WebhookReceiver from livekit-server-sdk"


def test_server_contains_express_raw():
    content = SERVER_FILE.read_text()
    assert "express.raw" in content, \
        "server.js must use express.raw middleware for webhook parsing"


def test_server_contains_events_endpoint():
    content = SERVER_FILE.read_text()
    assert "/events" in content, \
        "server.js must define a GET /events endpoint"


def test_server_contains_participant_joined_check():
    content = SERVER_FILE.read_text()
    assert "participant_joined" in content, \
        "server.js must check for the participant_joined event type"


def test_server_contains_port_4000():
    content = SERVER_FILE.read_text()
    assert "4000" in content, \
        "server.js must listen on port 4000"


def test_server_contains_webhook_route():
    content = SERVER_FILE.read_text()
    assert "/webhook" in content, \
        "server.js must define a POST /webhook route"


def test_server_contains_better_sqlite3():
    content = SERVER_FILE.read_text()
    assert "better-sqlite3" in content or "Database" in content, \
        "server.js must use better-sqlite3 for database operations"


def test_server_contains_insert():
    content = SERVER_FILE.read_text()
    assert "INSERT" in content or "insert" in content.lower(), \
        "server.js must insert rows into the participant_events table"


def test_server_starts_and_events_endpoint_returns_json():
    # Start the server as a background process
    env = os.environ.copy()
    env["LIVEKIT_API_KEY"] = "devkey"
    env["LIVEKIT_API_SECRET"] = "devsecret"

    proc = subprocess.Popen(
        ["node", "server.js"],
        cwd=str(PROJECT_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        # Give the server time to start
        time.sleep(3)

        # Check the process is still running
        assert proc.poll() is None, \
            f"server.js crashed on startup. stderr: {proc.stderr.read().decode()[:500]}"

        # Use curl to query the /events endpoint
        result = subprocess.run(
            ["curl", "-sf", "http://localhost:4000/events"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0, \
            f"GET /events failed: {result.stderr}"

        response_text = result.stdout.strip()
        assert len(response_text) > 0, "GET /events returned empty response"

        # Verify the response is valid JSON array
        data = json.loads(response_text)
        assert isinstance(data, list), \
            f"GET /events must return a JSON array, got: {type(data)}"

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
