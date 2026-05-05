## Background
LiveKit Agents supports equipping voice agents with callable tools using the `@agents.function_tool` decorator. The LLM can invoke these tools during a conversation to fetch live data, such as the current time or date. A production-ready agent project uses `uv` for dependency management and declares all dependencies in `pyproject.toml`.

## Requirements
Build a Python voice agent with a custom system prompt and two function tools: `get_current_time` and `get_current_date`.

## Implementation Guide
See `instruction.md` for full details.

## Constraints
- Project path: `/home/user/livekit-agent`
- Use `uv` as the package manager (already installed)
- Agent file: `src/agent.py`
- Agent class name: `Assistant`
- Agent name (in decorator): `assistant-agent`
- Function tools: `get_current_time` and `get_current_date`

## Integrations
- **LiveKit Agents Python**: `livekit-agents[codecs,turn-detector]` pip package
- **LiveKit Silero Plugin**: `livekit-plugins-silero` pip package
