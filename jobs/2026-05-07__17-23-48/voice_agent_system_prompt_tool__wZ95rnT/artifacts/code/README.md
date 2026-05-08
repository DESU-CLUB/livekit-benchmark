# LiveKit Voice Agent

A Python voice agent built with LiveKit Agents that provides current time and date information.

## Features

- Custom system prompt for conversational responses
- Function tools for retrieving current time and date
- Built with LiveKit Agents framework
- Uses Silero plugin for voice processing

## Requirements

- Python 3.9+
- uv package manager

## Setup

1. Install dependencies using uv:

```bash
uv sync
```

2. Run the agent:

```bash
uv run src/agent.py
```

## Function Tools

The agent provides two function tools:

- `get_current_time()`: Returns the current time in HH:MM:SS format
- `get_current_date()`: Returns the current date with day name

## Agent Configuration

- **Agent Class**: `Assistant`
- **Agent Name**: `assistant-agent`
- **System Prompt**: Custom instructions for conversational behavior

## Dependencies

- `livekit-agents[codecs,turn-detector]`: Core LiveKit Agents framework
- `livekit-plugins-silero`: Silero voice activity detection plugin