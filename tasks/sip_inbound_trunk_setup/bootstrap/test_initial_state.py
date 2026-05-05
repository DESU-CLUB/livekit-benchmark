import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-sip")
ENV_FILE = PROJECT_DIR / ".env.local"


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"


def test_python3_available():
    assert shutil.which("python3") is not None, "python3 must be installed"


def test_python_version_is_311_or_higher():
    result = subprocess.run(
        ["python3", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "python3 --version failed"
    version_str = result.stdout.strip().split(" ")[1]
    parts = version_str.split(".")
    major = int(parts[0])
    minor = int(parts[1])
    assert (major, minor) >= (3, 11), (
        f"Python version must be >= 3.11, got {version_str}"
    )


def test_livekit_server_sdk_installed():
    result = subprocess.run(
        ["python3", "-c", "import livekit.api"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "livekit-server-sdk (Python) must be installed — 'import livekit.api' failed"
    )


def test_python_dotenv_installed():
    result = subprocess.run(
        ["python3", "-c", "import dotenv"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "python-dotenv must be installed — 'import dotenv' failed"
    )


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


def test_setup_sip_py_does_not_exist_yet():
    setup_py = PROJECT_DIR / "setup_sip.py"
    assert not setup_py.exists(), (
        "setup_sip.py should not exist yet — user must create it"
    )
