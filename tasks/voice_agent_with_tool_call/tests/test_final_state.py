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


def test_agent_contains_function_tool_decorator():
    content = AGENT_FILE.read_text()
    assert "@agents.function_tool" in content or "@function_tool" in content, \
        "src/agent.py must contain @agents.function_tool or @function_tool decorator"


def test_agent_contains_get_weather():
    content = AGENT_FILE.read_text()
    assert "get_weather" in content, \
        "src/agent.py must contain the get_weather function tool method"


def test_agent_contains_weather_assistant():
    content = AGENT_FILE.read_text()
    assert "WeatherAssistant" in content, \
        "src/agent.py must define the WeatherAssistant class"


def test_agent_contains_agent_session():
    content = AGENT_FILE.read_text()
    assert "AgentSession" in content, \
        "src/agent.py must use AgentSession"


def test_agent_contains_weather_agent_name():
    content = AGENT_FILE.read_text()
    assert "weather-agent" in content, \
        "src/agent.py must register the agent with name 'weather-agent'"


def test_agent_contains_rtc_session_decorator():
    content = AGENT_FILE.read_text()
    assert "rtc_session" in content, \
        "src/agent.py must use @server.rtc_session decorator"


def test_agent_contains_silero_vad():
    content = AGENT_FILE.read_text()
    assert "silero" in content, \
        "src/agent.py must use silero VAD"


def test_pyproject_contains_livekit_agents():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-agents" in content, \
        "pyproject.toml must list livekit-agents as a dependency"


def test_pyproject_contains_silero():
    content = PYPROJECT_FILE.read_text()
    assert "livekit-plugins-silero" in content, \
        "pyproject.toml must list livekit-plugins-silero as a dependency"


def test_env_local_contains_livekit_keys():
    content = ENV_FILE.read_text()
    assert "LIVEKIT_API_KEY" in content, ".env.local must contain LIVEKIT_API_KEY"
    assert "LIVEKIT_API_SECRET" in content, ".env.local must contain LIVEKIT_API_SECRET"
    assert "LIVEKIT_URL" in content, ".env.local must contain LIVEKIT_URL"


def test_get_weather_returns_sunny():
    content = AGENT_FILE.read_text()
    assert "sunny" in content, \
        "get_weather must return a string containing 'sunny'"


def test_venv_has_python():
    python_bin = VENV_DIR / "bin" / "python"
    python_bin3 = VENV_DIR / "bin" / "python3"
    assert python_bin.exists() or python_bin3.exists(), \
        ".venv must contain a python executable"
