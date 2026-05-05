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


def test_pyproject_has_openai_dep():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-plugins-openai" in content, (
        "pyproject.toml must declare livekit-plugins-openai as a dependency"
    )


def test_pyproject_has_python_dotenv_dep():
    content = PYPROJECT_FILE.read_text()
    assert "python-dotenv" in content, (
        "pyproject.toml must declare python-dotenv as a dependency"
    )


def test_agent_file_exists():
    assert AGENT_FILE.is_file(), f"src/agent.py not found at {AGENT_FILE}"


def test_agent_uses_agent_server():
    source = AGENT_FILE.read_text()
    assert "AgentServer" in source, "src/agent.py must use AgentServer"


def test_agent_uses_rtc_session_decorator():
    source = AGENT_FILE.read_text()
    assert "rtc_session" in source, (
        "src/agent.py must use @server.rtc_session decorator"
    )


def test_agent_name_is_my_voice_agent():
    source = AGENT_FILE.read_text()
    assert "my-voice-agent" in source, (
        "src/agent.py must set agent_name='my-voice-agent'"
    )


def test_agent_uses_inference_stt():
    source = AGENT_FILE.read_text()
    assert "inference.STT" in source, "src/agent.py must use inference.STT"


def test_agent_uses_deepgram_nova3():
    source = AGENT_FILE.read_text()
    assert "deepgram/nova-3" in source, (
        "src/agent.py must use model='deepgram/nova-3' for STT"
    )


def test_agent_uses_inference_llm():
    source = AGENT_FILE.read_text()
    assert "inference.LLM" in source, "src/agent.py must use inference.LLM"


def test_agent_uses_gpt4o():
    source = AGENT_FILE.read_text()
    assert "openai/gpt-4o" in source, (
        "src/agent.py must use model='openai/gpt-4o' for LLM"
    )


def test_agent_uses_inference_tts():
    source = AGENT_FILE.read_text()
    assert "inference.TTS" in source, "src/agent.py must use inference.TTS"


def test_agent_uses_cartesia_sonic3():
    source = AGENT_FILE.read_text()
    assert "cartesia/sonic-3" in source, (
        "src/agent.py must use model='cartesia/sonic-3' for TTS"
    )


def test_agent_uses_silero_vad():
    source = AGENT_FILE.read_text()
    assert "silero.VAD.load()" in source, (
        "src/agent.py must use silero.VAD.load() for VAD"
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
