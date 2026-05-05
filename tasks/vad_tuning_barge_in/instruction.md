## Background
Voice Activity Detection (VAD) is a critical component of voice agents that determines when a user has stopped speaking. Tuning VAD parameters affects how quickly the agent responds (barge-in behavior) and how sensitive it is to brief pauses. The Silero VAD plugin for LiveKit exposes `min_silence_duration`, `min_speech_duration`, and `activation_threshold` parameters. Loading these from an external config file allows tuning without code changes.

## Requirements
Create a Python LiveKit voice agent with externally-configurable VAD settings optimized for low-latency barge-in, reading parameters from a JSON config file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-agent`.
2. Create `pyproject.toml` with:
   - Project name `livekit-agent`, version `0.1.0`, requires Python `>=3.11`.
   - Dependencies: `livekit-agents[codecs,turn-detector]`, `livekit-plugins-silero`, `python-dotenv`.
3. Create `.env.local` in the project root with placeholder values:
   - `LIVEKIT_URL=wss://your-livekit-server.livekit.cloud`
   - `LIVEKIT_API_KEY=your-api-key`
   - `LIVEKIT_API_SECRET=your-api-secret`
4. Create `vad_config.json` in the project root:
   ```json
   {
     "min_silence_duration": 0.2,
     "min_speech_duration": 0.05,
     "activation_threshold": 0.4
   }
   ```
5. Create the directory `src/` and file `src/agent.py` that:
   - Loads `.env.local` using `python-dotenv`.
   - Reads `vad_config.json` from the project root using `json.load()`.
   - Creates `server = AgentServer()`.
   - Defines an `Assistant(Agent)` class with instructions `"You are a helpful voice assistant."`.
   - Creates a `silero.VAD.load()` instance passing `min_silence_duration`, `min_speech_duration`, and `activation_threshold` from the loaded config as keyword arguments.
   - Creates an `AgentSession` with STT (`inference.STT`), LLM (`inference.LLM`), TTS (`inference.TTS`), and `vad` from the config.
   - Registers the session with `@server.rtc_session(agent_name="barge-in-agent")`.
   - Has `if __name__ == "__main__": agents.cli.run_app(server)` entry point.
6. Run `uv sync` to install dependencies.

## Constraints
- Project path: `/home/user/livekit-agent`
- Use `uv` as the package manager (already installed)
- Agent name must be `"barge-in-agent"`
- `vad_config.json` must have keys: `min_silence_duration`, `min_speech_duration`, `activation_threshold`
- VAD must be configured from `vad_config.json` (read at runtime, not hardcoded)
- `min_silence_duration`: `0.2`, `min_speech_duration`: `0.05`, `activation_threshold`: `0.4`

## Integrations
- **LiveKit Agents Python**: `livekit-agents[codecs,turn-detector]` pip package
- **LiveKit Silero Plugin**: `livekit-plugins-silero` pip package
