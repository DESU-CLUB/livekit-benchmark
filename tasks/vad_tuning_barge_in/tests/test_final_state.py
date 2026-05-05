import json
import os
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-agent")
PYPROJECT_FILE = PROJECT_DIR / "pyproject.toml"
AGENT_FILE = PROJECT_DIR / "src" / "agent.py"
ENV_FILE = PROJECT_DIR / ".env.local"
VAD_CONFIG_FILE = PROJECT_DIR / "vad_config.json"
VENV_DIR = PROJECT_DIR / ".venv"


def test_vad_config_json_exists():
    assert VAD_CONFIG_FILE.is_file(), (
        f"vad_config.json not found at {VAD_CONFIG_FILE}"
    )


def test_vad_config_has_min_silence_duration():
    data = json.loads(VAD_CONFIG_FILE.read_text())
    assert "min_silence_duration" in data, (
        "vad_config.json must contain 'min_silence_duration'"
    )
    assert data["min_silence_duration"] == 0.2, (
        f"vad_config.json 'min_silence_duration' must be 0.2, got: {data['min_silence_duration']}"
    )


def test_vad_config_has_min_speech_duration():
    data = json.loads(VAD_CONFIG_FILE.read_text())
    assert "min_speech_duration" in data, (
        "vad_config.json must contain 'min_speech_duration'"
    )
    assert data["min_speech_duration"] == 0.05, (
        f"vad_config.json 'min_speech_duration' must be 0.05, got: {data['min_speech_duration']}"
    )


def test_vad_config_has_activation_threshold():
    data = json.loads(VAD_CONFIG_FILE.read_text())
    assert "activation_threshold" in data, (
        "vad_config.json must contain 'activation_threshold'"
    )
    assert data["activation_threshold"] == 0.4, (
        f"vad_config.json 'activation_threshold' must be 0.4, got: {data['activation_threshold']}"
    )


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


def test_agent_file_exists():
    assert AGENT_FILE.is_file(), f"src/agent.py not found at {AGENT_FILE}"


def test_agent_reads_vad_config():
    source = AGENT_FILE.read_text()
    assert "vad_config.json" in source, (
        "src/agent.py must read 'vad_config.json' from the project root"
    )


def test_agent_uses_silero_vad_load():
    source = AGENT_FILE.read_text()
    assert "silero.VAD.load" in source, (
        "src/agent.py must call silero.VAD.load() with VAD config parameters"
    )


def test_agent_name_is_barge_in_agent():
    source = AGENT_FILE.read_text()
    assert "barge-in-agent" in source, (
        "src/agent.py must set agent_name='barge-in-agent'"
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
