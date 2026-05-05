import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
PACKAGE_JSON = PROJECT_DIR / "package.json"
NODE_MODULES = PROJECT_DIR / "node_modules" / "livekit-server-sdk"


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"


def test_package_json_exists():
    assert PACKAGE_JSON.is_file(), f"package.json not found at {PACKAGE_JSON}"


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


def test_livekit_server_sdk_installed():
    assert NODE_MODULES.is_dir(), (
        f"livekit-server-sdk not found in node_modules at {NODE_MODULES}"
    )
