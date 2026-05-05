import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-rooms")
ENV_FILE = PROJECT_DIR / ".env.local"


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"


def test_env_local_file_exists():
    assert ENV_FILE.is_file(), f".env.local file not found at {ENV_FILE}"


def test_env_local_contains_livekit_url():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_URL" in content, ".env.local must contain LIVEKIT_URL"


def test_env_local_contains_api_key():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_KEY" in content, ".env.local must contain LIVEKIT_API_KEY"


def test_env_local_contains_api_secret():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_SECRET" in content, ".env.local must contain LIVEKIT_API_SECRET"


def test_lk_cli_installed():
    assert shutil.which("lk") is not None, "lk CLI must be installed and on PATH"


def test_lk_cli_is_executable():
    lk_path = shutil.which("lk")
    assert lk_path is not None
    result = subprocess.run(
        [lk_path, "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"lk --version failed: {result.stderr}"
