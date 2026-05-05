## Background
LiveKit Agents supports using third-party STT providers directly through plugins instead of the LiveKit inference service. The Deepgram plugin (`livekit-plugins-deepgram`) allows you to use Deepgram's `nova-3` model by providing a Deepgram API key. This gives more control over STT behavior and model selection.

## Requirements
Build a Python voice agent that uses the Deepgram STT plugin directly, configured with a Deepgram API key from the environment.

## Implementation Guide
See `instruction.md` for full details.

## Constraints
- Project path: `/home/user/livekit-agent`
- Use `uv` as the package manager
- Agent file: `src/agent.py`
- Agent name (in decorator): `deepgram-agent`
- Must import and use `deepgram.STT` from `livekit.plugins`
- `DEEPGRAM_API_KEY` must be in `.env.local`

## Integrations
- **LiveKit Agents Python**: `livekit-agents[codecs,turn-detector]` pip package
- **LiveKit Deepgram Plugin**: `livekit-plugins-deepgram` pip package
- **LiveKit Silero Plugin**: `livekit-plugins-silero` pip package
