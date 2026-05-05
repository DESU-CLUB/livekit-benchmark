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


def test_pyproject_has_silero_plugin():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-plugins-silero" in content, (
        "pyproject.toml must declare livekit-plugins-silero as a dependency"
    )


def test_agent_defines_assistant_class():
    source = AGENT_FILE.read_text()
    assert "Assistant" in source, "src/agent.py must define an Assistant class"


def test_agent_has_assistant_agent_name():
    source = AGENT_FILE.read_text()
    assert "assistant-agent" in source, (
        "src/agent.py must register the agent with name 'assistant-agent'"
    )


def test_agent_has_function_tool_decorator():
    source = AGENT_FILE.read_text()
    assert "@agents.function_tool" in source or "@function_tool" in source, (
        "src/agent.py must use @agents.function_tool or @function_tool decorator"
    )


def test_agent_has_get_current_time():
    source = AGENT_FILE.read_text()
    assert "get_current_time" in source, (
        "src/agent.py must define a get_current_time function tool"
    )


def test_agent_has_get_current_date():
    source = AGENT_FILE.read_text()
    assert "get_current_date" in source, (
        "src/agent.py must define a get_current_date function tool"
    )


def test_agent_uses_agent_session():
    source = AGENT_FILE.read_text()
    assert "AgentSession" in source, "src/agent.py must use AgentSession"


def test_agent_uses_silero_vad():
    source = AGENT_FILE.read_text()
    assert "silero" in source, "src/agent.py must use silero VAD"


def test_agent_uses_rtc_session_decorator():
    source = AGENT_FILE.read_text()
    assert "rtc_session" in source, (
        "src/agent.py must use @server.rtc_session decorator"
    )


def test_agent_has_system_prompt():
    source = AGENT_FILE.read_text()
    assert "instructions" in source, (
        "Assistant class must define an instructions (system prompt)"
    )


def test_env_local_has_livekit_keys():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_URL" in content, ".env.local must contain LIVEKIT_URL"
    assert "LIVEKIT_API_KEY" in content, ".env.local must contain LIVEKIT_API_KEY"
    assert "LIVEKIT_API_SECRET" in content, ".env.local must contain LIVEKIT_API_SECRET"


def test_venv_has_python_binary():
    python_bin = VENV_DIR / "bin" / "python"
    python_bin3 = VENV_DIR / "bin" / "python3"
    assert python_bin.exists() or python_bin3.exists(), (
        ".venv must contain a python executable"
    )
