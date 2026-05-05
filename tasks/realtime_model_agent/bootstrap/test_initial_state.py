import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-agent")


def test_project_dir_exists():
    assert PROJECT_DIR.is_dir(), f"Project directory {PROJECT_DIR} does not exist"


def test_uv_installed():
    assert shutil.which("uv") is not None, "uv is not installed or not on PATH"


def test_python3_installed():
    assert shutil.which("python3") is not None, "python3 is not installed or not on PATH"


def test_agent_file_not_yet_created():
    agent_file = PROJECT_DIR / "src" / "agent.py"
    assert not agent_file.exists(), "src/agent.py should not exist yet (pre-task state)"


def test_pyproject_toml_not_yet_created():
    pyproject = PROJECT_DIR / "pyproject.toml"
    assert not pyproject.exists(), "pyproject.toml should not exist yet (pre-task state)"


def test_venv_not_yet_created():
    venv = PROJECT_DIR / ".venv"
    assert not venv.exists(), ".venv should not exist yet (pre-task state)"
