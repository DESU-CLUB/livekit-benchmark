import os
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-agent")
AGENT_FILE = PROJECT_DIR / "src" / "agent.py"
PYPROJECT_FILE = PROJECT_DIR / "pyproject.toml"
ENV_FILE = PROJECT_DIR / ".env.local"
VENV_DIR = PROJECT_DIR / ".venv"


def test_agent_file_exists():
    assert AGENT_FILE.is_file(), f"src/agent.py not found at {AGENT_FILE}"


def test_pyproject_toml_exists():
    assert PYPROJECT_FILE.is_file(), f"pyproject.toml not found at {PYPROJECT_FILE}"


def test_env_local_exists():
    assert ENV_FILE.is_file(), f".env.local not found at {ENV_FILE}"


def test_venv_exists():
    assert VENV_DIR.is_dir(), (
        f".venv directory not found at {VENV_DIR} — run 'uv sync' to install dependencies"
    )


def test_pyproject_has_livekit_agents():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-agents" in content, (
        "pyproject.toml must declare livekit-agents as a dependency"
    )


def test_pyproject_has_deepgram_plugin():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-plugins-deepgram" in content, (
        "pyproject.toml must declare livekit-plugins-deepgram as a dependency"
    )


def test_pyproject_has_silero_plugin():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-plugins-silero" in content, (
        "pyproject.toml must declare livekit-plugins-silero as a dependency"
    )


def test_agent_imports_deepgram_plugin():
    source = AGENT_FILE.read_text()
    assert "deepgram" in source, (
        "src/agent.py must import the deepgram plugin from livekit.plugins"
    )


def test_agent_uses_deepgram_stt():
    source = AGENT_FILE.read_text()
    assert "deepgram.STT" in source, (
        "src/agent.py must use deepgram.STT() directly (not inference.STT)"
    )


def test_agent_uses_nova_3_model():
    source = AGENT_FILE.read_text()
    assert "nova-3" in source, (
        "src/agent.py must use model='nova-3' for Deepgram STT"
    )


def test_agent_has_deepgram_agent_name():
    source = AGENT_FILE.read_text()
    assert "deepgram-agent" in source, (
        "src/agent.py must register the agent with name 'deepgram-agent'"
    )


def test_agent_uses_inference_llm():
    source = AGENT_FILE.read_text()
    assert "inference.LLM" in source, (
        "src/agent.py must use inference.LLM for the language model"
    )


def test_agent_uses_inference_tts():
    source = AGENT_FILE.read_text()
    assert "inference.TTS" in source, (
        "src/agent.py must use inference.TTS for text-to-speech"
    )


def test_agent_uses_silero_vad():
    source = AGENT_FILE.read_text()
    assert "silero" in source, (
        "src/agent.py must use silero VAD"
    )


def test_agent_uses_rtc_session_decorator():
    source = AGENT_FILE.read_text()
    assert "rtc_session" in source, (
        "src/agent.py must use @server.rtc_session decorator"
    )


def test_agent_uses_agent_session():
    source = AGENT_FILE.read_text()
    assert "AgentSession" in source, "src/agent.py must use AgentSession"


def test_env_local_has_livekit_keys():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_URL" in content, ".env.local must contain LIVEKIT_URL"
    assert "LIVEKIT_API_KEY" in content, ".env.local must contain LIVEKIT_API_KEY"
    assert "LIVEKIT_API_SECRET" in content, ".env.local must contain LIVEKIT_API_SECRET"


def test_env_local_has_deepgram_api_key():
    content = ENV_FILE.read_text()
    assert "DEEPGRAM_API_KEY" in content, (
        ".env.local must contain DEEPGRAM_API_KEY"
    )


def test_venv_has_python_binary():
    python_bin = VENV_DIR / "bin" / "python"
    python_bin3 = VENV_DIR / "bin" / "python3"
    assert python_bin.exists() or python_bin3.exists(), (
        ".venv must contain a python executable"
    )
