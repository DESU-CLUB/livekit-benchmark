import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-token")
ENV_FILE = PROJECT_DIR / ".env.local"


def test_project_dir_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"


def test_python3_installed():
    assert shutil.which("python3") is not None, "python3 is not installed or not on PATH"


def test_env_local_exists():
    assert ENV_FILE.exists(), f".env.local does not exist at {ENV_FILE}"


def test_env_local_has_api_key():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_KEY=test-key" in content, \
        ".env.local must contain LIVEKIT_API_KEY=test-key"


def test_env_local_has_api_secret():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_SECRET=test-secret" in content, \
        ".env.local must contain LIVEKIT_API_SECRET=test-secret"


def test_livekit_server_sdk_installed():
    result = subprocess.run(
        ["python3", "-c", "import livekit.api"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, \
        "livekit-server-sdk Python package must be installed (livekit.api importable)"


def test_camera_token_script_not_yet_created():
    script = PROJECT_DIR / "camera_token.py"
    assert not script.exists(), "camera_token.py should not exist yet (pre-task state)"


def test_token_txt_not_yet_created():
    token_file = PROJECT_DIR / "token.txt"
    assert not token_file.exists(), "token.txt should not exist yet (pre-task state)"
