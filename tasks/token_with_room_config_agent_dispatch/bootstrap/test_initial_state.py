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


def test_livekit_protocol_installed():
    node_modules = PROJECT_DIR / "node_modules" / "@livekit" / "protocol"
    assert node_modules.is_dir(), "@livekit/protocol must be installed in node_modules"


def test_dispatch_token_script_not_yet_created():
    script = PROJECT_DIR / "dispatch_token.mjs"
    assert not script.exists(), "dispatch_token.mjs should not exist yet (pre-task state)"


def test_token_txt_not_yet_created():
    token_file = PROJECT_DIR / "token.txt"
    assert not token_file.exists(), "token.txt should not exist yet (pre-task state)"
