import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
SCRIPT_FILE = PROJECT_DIR / "mute_track.mjs"
LOG_FILE = PROJECT_DIR / "output.log"


def test_mute_track_script_exists():
    assert SCRIPT_FILE.is_file(), f"mute_track.mjs not found at {SCRIPT_FILE}"


def test_script_uses_room_service_client():
    source = SCRIPT_FILE.read_text()
    assert "RoomServiceClient" in source, (
        "mute_track.mjs must import and use RoomServiceClient"
    )


def test_script_calls_mute_published_track():
    source = SCRIPT_FILE.read_text()
    assert "mutePublishedTrack" in source, (
        "mute_track.mjs must call mutePublishedTrack"
    )


def test_script_uses_process_argv():
    source = SCRIPT_FILE.read_text()
    assert "process.argv" in source, (
        "mute_track.mjs must use process.argv to read CLI arguments"
    )


def test_script_reads_env_vars():
    source = SCRIPT_FILE.read_text()
    assert "LIVEKIT_URL" in source or "process.env" in source, (
        "mute_track.mjs must read LIVEKIT credentials from environment variables"
    )


def test_output_log_exists():
    assert LOG_FILE.is_file(), f"output.log not found at {LOG_FILE}"


def test_output_log_contains_mute_message():
    content = LOG_FILE.read_text()
    assert "Track muted:" in content, (
        "output.log must contain 'Track muted:' followed by the track SID"
    )
