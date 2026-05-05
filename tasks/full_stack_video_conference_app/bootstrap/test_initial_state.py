import os
import shutil
import subprocess
import pytest
from pathlib import Path

HOME = Path("/home/user")
PROJECT_DIR = HOME / "livekit-meet"


def test_node_installed():
    assert shutil.which("node") is not None, "node must be installed"


def test_node_version_is_20_or_higher():
    result = subprocess.run(
        ["node", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "node --version failed"
    version_str = result.stdout.strip().lstrip("v")
    major = int(version_str.split(".")[0])
    assert major >= 20, f"Node.js version must be >= 20, got {result.stdout.strip()}"


def test_npm_installed():
    assert shutil.which("npm") is not None, "npm must be installed"


def test_home_user_exists():
    assert HOME.is_dir(), f"/home/user directory does not exist"


def test_project_dir_does_not_exist_yet():
    # The agent should create this from scratch
    assert not PROJECT_DIR.exists() or not (PROJECT_DIR / "backend").exists(), (
        "Backend should not exist before the agent runs"
    )
