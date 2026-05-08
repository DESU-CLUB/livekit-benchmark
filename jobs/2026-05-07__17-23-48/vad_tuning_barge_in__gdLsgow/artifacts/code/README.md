# LiveKit Voice Agent with Configurable VAD

A Python LiveKit voice agent with externally-configurable Voice Activity Detection (VAD) settings optimized for low-latency barge-in behavior.

## Features

- **Configurable VAD Parameters**: Tune VAD behavior without code changes via `vad_config.json`
- **Low-Latency Barge-in**: Optimized settings for fast response times
- **Silero VAD Plugin**: Uses the high-quality Silero VAD model
- **Environment Configuration**: Secure credential management via `.env.local`

## VAD Configuration

The VAD parameters are loaded from `vad_config.json`:

```json
{
  "min_silence_duration": 0.2,
  "min_speech_duration": 0.05,
  "activation_threshold": 0.4
}
```

### Parameter Explanations

- **`min_silence_duration`** (0.2s): How long to wait after speech stops before considering it a pause. Lower values = faster barge-in but more sensitive to brief pauses.
- **`min_speech_duration`** (0.05s): Minimum duration of speech to consider it valid. Filters out very short utterances.
- **`activation_threshold`** (0.4): Sensitivity threshold for detecting speech (0.0-1.0). Lower values = more sensitive, higher values = less sensitive.

## Setup

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Configure Environment Variables**:
   Edit `.env.local` with your LiveKit credentials:
   ```
   LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

3. **Run the Agent**:
   ```bash
   uv run python src/agent.py
   ```

## Tuning VAD Parameters

To adjust the barge-in behavior:

1. Edit `vad_config.json`
2. Adjust the parameters based on your needs:
   - **For faster barge-in**: Decrease `min_silence_duration`
   - **To avoid cutting off speech**: Increase `min_silence_duration`
   - **To detect softer speech**: Decrease `activation_threshold`
   - **To ignore background noise**: Increase `activation_threshold`
3. Restart the agent to apply changes

## Project Structure

```
livekit-agent/
├── pyproject.toml          # Project dependencies
├── .env.local              # Environment variables
├── vad_config.json         # VAD configuration
├── src/
│   └── agent.py           # Agent implementation
└── README.md              # This file
```

## Requirements

- Python >= 3.11
- uv package manager
- LiveKit server connection

## License

MIT License