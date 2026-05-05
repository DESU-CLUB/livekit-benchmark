import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-agent")


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


def test_uv_available():
    assert shutil.which("uv") is not None, "uv package manager must be installed"


def test_project_directory_has_no_pyproject():
    pyproject = PROJECT_DIR / "pyproject.toml"
    assert not pyproject.exists(), (
        "pyproject.toml should not exist yet — user must create it"
    )
