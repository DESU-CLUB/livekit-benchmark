# LiveKit Agent with Deepgram STT

A Python voice agent built with LiveKit Agents that uses the Deepgram STT plugin for speech recognition.

## Features

- Uses Deepgram's `nova-3` model for high-accuracy speech-to-text
- Direct integration with Deepgram API (no LiveKit inference service required)
- Silero TTS for text-to-speech output
- Configured via environment variables

## Setup

### Prerequisites

- Python 3.10+
- A Deepgram API key (get one at https://console.deepgram.com/)
- LiveKit Cloud account or self-hosted LiveKit server

### Installation

1. Clone or navigate to this project directory:
   ```bash
   cd /home/user/livekit-agent
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Configure your Deepgram API key in `.env.local`:
   ```bash
   # Edit .env.local and replace with your actual API key
   DEEPGRAM_API_KEY=your_deepgram_api_key_here
   ```

## Usage

Run the agent:
```bash
uv run livekit_agent/agent.py
```

The agent will connect to your LiveKit room and use Deepgram's STT for speech recognition.

## Testing

Verify the installation and configuration:

```bash
# Run the test script
uv run python test_agent.py
```

Expected output:
```
✓ All imports successful
✓ Agent function: deepgram_agent
✓ Prewarm function: prewarm
✓ DEEPGRAM_API_KEY is set

All checks passed! The agent is ready to use.
```

## Configuration

### Environment Variables

- `DEEPGRAM_API_KEY`: Your Deepgram API key (required)
- `LIVEKIT_URL`: LiveKit server URL (optional, can be passed via CLI)
- `LIVEKIT_API_KEY`: LiveKit API key (optional, can be passed via CLI)
- `LIVEKIT_API_SECRET`: LiveKit API secret (optional, can be passed via CLI)

### Deepgram STT Options

The agent is configured with the following Deepgram options:
- Model: `nova-3` (Deepgram's most accurate model)
- Language: `en-US` (English US)

You can modify these in `src/agent.py` to suit your needs.

## Project Structure

```
livekit-agent/
├── .env.local                    # Environment variables (not committed to git)
├── .gitignore                    # Git ignore rules
├── pyproject.toml                # Project configuration and dependencies
├── README.md                     # This file
├── DEEPGRAM_SETUP.md             # Detailed setup guide
├── PROJECT_SUMMARY.md            # Project summary
├── test_agent.py                 # Test script
└── livekit_agent/                # Main package directory
    ├── __init__.py              # Package initialization
    └── agent.py                 # Main agent implementation
```

## Dependencies

- `livekit-agents[codecs,turn-detector]`: LiveKit Agents framework
- `livekit-plugins-deepgram`: Deepgram STT plugin
- `livekit-plugins-silero`: Silero TTS plugin

## License

MIT