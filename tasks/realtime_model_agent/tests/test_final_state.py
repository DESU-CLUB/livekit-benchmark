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
    assert AGENT_FILE.exists(), f"{AGENT_FILE} does not exist"


def test_pyproject_toml_exists():
    assert PYPROJECT_FILE.exists(), f"{PYPROJECT_FILE} does not exist"


def test_env_local_exists():
    assert ENV_FILE.exists(), f"{ENV_FILE} does not exist"


def test_venv_exists():
    assert VENV_DIR.is_dir(), f".venv directory does not exist at {VENV_DIR}"


def test_agent_contains_realtime_model():
    content = AGENT_FILE.read_text()
    assert "RealtimeModel" in content, \
        "src/agent.py must use RealtimeModel"


def test_agent_contains_voice_coral():
    content = AGENT_FILE.read_text()
    assert 'voice="coral"' in content or "voice='coral'" in content, \
        "src/agent.py must set voice=\"coral\" in RealtimeModel"


def test_agent_contains_rtc_session_decorator():
    content = AGENT_FILE.read_text()
    assert "rtc_session" in content, \
        "src/agent.py must use @server.rtc_session decorator"


def test_agent_contains_realtime_agent_name():
    content = AGENT_FILE.read_text()
    assert "realtime-agent" in content, \
        "src/agent.py must register the agent with name 'realtime-agent'"


def test_agent_contains_lk_openai_import():
    content = AGENT_FILE.read_text()
    assert "lk_openai" in content or "openai as lk_openai" in content, \
        "src/agent.py must import openai plugin as lk_openai"


def test_agent_contains_agent_session():
    content = AGENT_FILE.read_text()
    assert "AgentSession" in content, \
        "src/agent.py must use AgentSession"


def test_agent_uses_realtime_model_as_llm():
    content = AGENT_FILE.read_text()
    assert "lk_openai.realtime.RealtimeModel" in content or \
           ("realtime.RealtimeModel" in content), \
        "src/agent.py must use lk_openai.realtime.RealtimeModel as the llm in AgentSession"


def test_pyproject_contains_livekit_agents():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-agents" in content, \
        "pyproject.toml must list livekit-agents as a dependency"


def test_pyproject_contains_openai_plugin():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-plugins-openai" in content, \
        "pyproject.toml must list livekit-plugins-openai as a dependency"


def test_env_local_contains_livekit_keys():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_KEY" in content, ".env.local must contain LIVEKIT_API_KEY"
    assert "LIVEKIT_API_SECRET" in content, ".env.local must contain LIVEKIT_API_SECRET"
    assert "LIVEKIT_URL" in content, ".env.local must contain LIVEKIT_URL"


def test_env_local_contains_openai_api_key():
    content = ENV_FILE.read_text()
    assert "OPENAI_API_KEY" in content, ".env.local must contain OPENAI_API_KEY"


def test_venv_has_python():
    python_bin = VENV_DIR / "bin" / "python"
    python_bin3 = VENV_DIR / "bin" / "python3"
    assert python_bin.exists() or python_bin3.exists(), \
        ".venv must contain a python executable"


def test_agent_has_agent_class():
    content = AGENT_FILE.read_text()
    assert "Agent)" in content or "Agent):" in content, \
        "src/agent.py must define an Agent subclass"


def test_agent_contains_helpful_instructions():
    content = AGENT_FILE.read_text()
    assert "helpful" in content.lower(), \
        "Agent instructions should mention being helpful"
