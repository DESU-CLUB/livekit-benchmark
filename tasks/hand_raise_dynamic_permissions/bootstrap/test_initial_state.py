import os
import shutil
import subprocess
import json
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-permissions")
PACKAGE_JSON = PROJECT_DIR / "package.json"
NODE_MODULES_EXPRESS = PROJECT_DIR / "node_modules" / "express"
NODE_MODULES_LIVEKIT = PROJECT_DIR / "node_modules" / "livekit-server-sdk"


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


def test_express_installed():
    assert NODE_MODULES_EXPRESS.is_dir(), (
        f"express not found in node_modules at {NODE_MODULES_EXPRESS}"
    )


def test_livekit_server_sdk_installed():
    assert NODE_MODULES_LIVEKIT.is_dir(), (
        f"livekit-server-sdk not found in node_modules at {NODE_MODULES_LIVEKIT}"
    )


def test_server_js_does_not_exist_yet():
    server_js = PROJECT_DIR / "server.js"
    assert not server_js.exists(), (
        "server.js should not exist yet — user must create it"
    )
