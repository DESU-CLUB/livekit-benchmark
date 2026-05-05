import os
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-agent")
PYPROJECT_FILE = PROJECT_DIR / "pyproject.toml"
AGENT_FILE = PROJECT_DIR / "src" / "agent.py"
ENV_FILE = PROJECT_DIR / ".env.local"
VENV_DIR = PROJECT_DIR / ".venv"


def test_pyproject_toml_exists():
    assert PYPROJECT_FILE.is_file(), f"pyproject.toml not found at {PYPROJECT_FILE}"


def test_pyproject_has_livekit_agents_dep():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-agents" in content, (
        "pyproject.toml must declare livekit-agents as a dependency"
    )


def test_pyproject_has_silero_dep():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-plugins-silero" in content, (
        "pyproject.toml must declare livekit-plugins-silero as a dependency"
    )


def test_pyproject_has_python_dotenv_dep():
    content = PYPROJECT_FILE.read_text()
    assert "python-dotenv" in content, (
        "pyproject.toml must declare python-dotenv as a dependency"
    )


def test_agent_file_exists():
    assert AGENT_FILE.is_file(), f"src/agent.py not found at {AGENT_FILE}"


def test_agent_uses_turn_handling_options():
    source = AGENT_FILE.read_text()
    assert "TurnHandlingOptions" in source, (
        "src/agent.py must import and use TurnHandlingOptions"
    )


def test_agent_uses_multilingual_model():
    source = AGENT_FILE.read_text()
    assert "MultilingualModel" in source, (
        "src/agent.py must import and use MultilingualModel"
    )


def test_agent_uses_turn_detection_multilingual():
    source = AGENT_FILE.read_text()
    assert "turn_detection=MultilingualModel()" in source, (
        "src/agent.py must pass turn_detection=MultilingualModel() to TurnHandlingOptions"
    )


def test_agent_name_is_turn_aware_agent():
    source = AGENT_FILE.read_text()
    assert "turn-aware-agent" in source, (
        "src/agent.py must set agent_name='turn-aware-agent'"
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


def test_venv_exists_after_uv_sync():
    assert VENV_DIR.is_dir(), (
        f".venv directory not found at {VENV_DIR} — run 'uv sync' to install dependencies"
    )
