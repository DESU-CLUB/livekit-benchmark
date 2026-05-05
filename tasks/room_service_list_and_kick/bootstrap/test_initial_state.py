import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-admin")
PACKAGE_JSON = PROJECT_DIR / "package.json"


def test_project_dir_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"


def test_node_installed():
    assert shutil.which("node") is not None, "node is not installed or not on PATH"


def test_npm_installed():
    assert shutil.which("npm") is not None, "npm is not installed or not on PATH"


def test_package_json_exists():
    assert PACKAGE_JSON.exists(), f"{PACKAGE_JSON} does not exist"


def test_livekit_server_sdk_installed():
    node_modules = PROJECT_DIR / "node_modules" / "livekit-server-sdk"
    assert node_modules.is_dir(), "livekit-server-sdk must be installed in node_modules"


def test_list_and_kick_script_not_yet_created():
    script = PROJECT_DIR / "list_and_kick.mjs"
    assert not script.exists(), "list_and_kick.mjs should not exist yet (pre-task state)"


def test_output_log_not_yet_created():
    log_file = PROJECT_DIR / "output.log"
    assert not log_file.exists(), "output.log should not exist yet (pre-task state)"
