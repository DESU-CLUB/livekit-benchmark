import os
import shutil
import subprocess
import pytest
from pathlib import Path

HOME = Path("/home/user")
PROJECT_DIR = HOME / "livekit-broadcast"
ENV_FILE = PROJECT_DIR / ".env.local"


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"


def test_env_local_exists():
    assert ENV_FILE.is_file(), f".env.local not found at {ENV_FILE}"


def test_env_local_has_livekit_url():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_URL" in content, ".env.local must contain LIVEKIT_URL"


def test_env_local_has_api_key():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_KEY" in content, ".env.local must contain LIVEKIT_API_KEY"


def test_env_local_has_api_secret():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_SECRET" in content, ".env.local must contain LIVEKIT_API_SECRET"


def test_python3_installed():
    assert shutil.which("python3") is not None, "python3 must be installed"


def test_livekit_server_sdk_installed():
    result = subprocess.run(
        ["python3", "-c", "from livekit import api"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"livekit-server-sdk Python package must be installed: {result.stderr}"
    )
