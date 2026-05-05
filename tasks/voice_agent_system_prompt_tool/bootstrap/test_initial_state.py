import os
import shutil
import subprocess
import pytest
from pathlib import Path

HOME = Path("/home/user")
PROJECT_DIR = HOME / "livekit-agent"


def test_home_user_exists():
    assert HOME.is_dir(), "/home/user directory does not exist"


def test_python3_installed():
    assert shutil.which("python3") is not None, "python3 must be installed"


def test_python_version_is_311_or_higher():
    result = subprocess.run(
        ["python3", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "python3 --version failed"
    version_str = result.stdout.strip().split()[-1]
    major, minor = version_str.split(".")[:2]
    assert (int(major), int(minor)) >= (3, 11), (
        f"Python version must be >= 3.11, got {version_str}"
    )


def test_uv_installed():
    assert shutil.which("uv") is not None, "uv must be installed"


def test_project_dir_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"
