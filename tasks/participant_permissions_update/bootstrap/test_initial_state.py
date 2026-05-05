import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
ENV_FILE = PROJECT_DIR / ".env.local"


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"


def test_env_local_file_exists():
    assert ENV_FILE.is_file(), f".env.local file not found at {ENV_FILE}"


def test_env_local_contains_api_key():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_KEY" in content, ".env.local must contain LIVEKIT_API_KEY"


def test_env_local_contains_api_secret():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_SECRET" in content, ".env.local must contain LIVEKIT_API_SECRET"


def test_python3_available():
    assert shutil.which("python3") is not None, "python3 must be installed"


def test_livekit_server_sdk_installed():
    result = subprocess.run(
        ["python3", "-c", "import livekit.api"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "livekit-server-sdk must be installed (python3 -c 'import livekit.api')"
    )
