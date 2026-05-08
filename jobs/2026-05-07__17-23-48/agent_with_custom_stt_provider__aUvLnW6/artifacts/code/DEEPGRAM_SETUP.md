# Deepgram STT Plugin Setup Guide

This guide explains how to set up and use the LiveKit agent with the Deepgram STT plugin.

## Prerequisites

1. **Deepgram API Key**: Get your API key from [Deepgram Console](https://console.deepgram.com/)
2. **LiveKit Server**: Either use LiveKit Cloud or self-host a LiveKit server
3. **Python 3.10+**: Required for this project
4. **uv**: The package manager (install from https://github.com/astral-sh/uv)

## Installation Steps

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd /home/user/livekit-agent

# Install dependencies using uv
uv sync
```

### 2. Configure Environment Variables

Create or edit the `.env.local` file:

```bash
# Edit .env.local
DEEPGRAM_API_KEY=your_actual_deepgram_api_key_here
```

### 3. Verify Installation

Run the test script to verify everything is set up correctly:

```bash
uv run python test_agent.py
```

You should see output like:
```
✓ All imports successful
✓ Agent function: deepgram_agent
✓ Prewarm function: prewarm
✓ DEEPGRAM_API_KEY is set

All checks passed! The agent is ready to use.
```

## Running the Agent

### Method 1: Using CLI (Recommended)

```bash
uv run livekit_agent/agent.py
```

### Method 2: Using Environment Variables

```bash
# Set LiveKit connection details
export LIVEKIT_URL=wss://your-livekit-server.com
export LIVEKIT_API_KEY=your_livekit_api_key
export LIVEKIT_API_SECRET=your_livekit_api_secret

# Run the agent
uv run livekit_agent/agent.py
```

### Method 3: Using CLI Arguments

```bash
uv run livekit_agent/agent.py --url wss://your-livekit-server.com --api-key your_livekit_api_key --api-secret your_livekit_api_secret
```

## Configuration Options

### Deepgram STT Settings

The agent is configured with the following Deepgram settings (in `livekit_agent/agent.py`):

```python
deepgram.STT(
    model="nova-3",      # Best accuracy model
    language="en-US",    # English (US)
)
```

You can modify these settings:

- **Model Options**: `nova-2`, `nova-3`, `whisper-tiny`, `whisper-base`, etc.
- **Language Options**: Various language codes (e.g., `en-US`, `es-ES`, `fr-FR`)

### Silero TTS Settings

The agent uses Silero for text-to-speech:

```python
silero.TTS()
```

Default settings include:
- Language: English
- Voice: v3_en
- Sample rate: 24000 Hz

## Architecture

The agent follows this flow:

```
User Speech → Deepgram STT → Agent Processing → Silero TTS → Audio Output
```

### Components

1. **Deepgram STT**: Converts speech to text using Deepgram's API
2. **Agent**: Processes the transcribed text
3. **Silero TTS**: Converts text responses to speech

## Troubleshooting

### DEEPGRAM_API_KEY not set

**Error**: `DEEPGRAM_API_KEY environment variable is not set`

**Solution**: 
1. Check that `.env.local` exists
2. Verify the API key is set correctly
3. Restart your terminal or reload environment variables

### Connection Issues

**Error**: Connection refused or timeout

**Solution**:
1. Verify LiveKit server URL is correct
2. Check API key and secret
3. Ensure firewall allows WebSocket connections

### Import Errors

**Error**: `ModuleNotFoundError` or `ImportError`

**Solution**:
```bash
# Reinstall dependencies
uv sync

# Verify Python version (must be 3.10+)
python --version
```

## Testing

### Test Import

```bash
uv run python -c "from livekit_agent.agent import deepgram_agent; print('OK')"
```

### Test Deepgram Connection

```bash
# This requires a valid API key
uv run python -c "
from livekit.plugins import deepgram
import os

stt = deepgram.STT(
    api_key=os.getenv('DEEPGRAM_API_KEY'),
    model='nova-3'
)
print('Deepgram STT initialized successfully')
"
```

## Advanced Usage

### Custom Instructions

Modify the agent's instructions in `livekit_agent/agent.py`:

```python
agent = Agent(
    instructions="You are a specialized assistant for...",
    stt=stt,
    tts=proc.userdata["tts"],
)
```

### Adding LLM Support

To add language model support, install additional dependencies:

```bash
uv pip install livekit-plugins-openai
```

Then modify the agent:

```python
from livekit.plugins import openai

agent = Agent(
    instructions="You are a helpful voice assistant.",
    stt=stt,
    tts=proc.userdata["tts"],
    llm=openai.LLM(model="gpt-4o"),
)
```

## Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/overview/)
- [Deepgram Documentation](https://developers.deepgram.com/)
- [LiveKit Deepgram Plugin](https://github.com/livekit/python-plugins/tree/main/deepgram)
- [LiveKit Silero Plugin](https://github.com/livekit/python-plugins/tree/main/silero)

## Support

For issues or questions:
- Check the [LiveKit Community](https://community.livekit.io/)
- Review [LiveKit GitHub Issues](https://github.com/livekit/python-sdk/issues)
- Contact [Deepgram Support](https://deepgram.com/support)