# Build a LiveKit Voice Agent with Deepgram STT

Create a LiveKit voice agent at `/home/user/livekit-agent` that uses the Deepgram STT plugin directly.

## Project Setup

Create `pyproject.toml` with:
- Project name: `livekit-agent`
- Python version: `>=3.11`
- Dependencies:
  - `livekit-agents[codecs,turn-detector]`
  - `livekit-plugins-deepgram`
  - `livekit-plugins-silero`
  - `python-dotenv`

## Environment File (`.env.local`)

Create `.env.local` with placeholder values:
```
LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
DEEPGRAM_API_KEY=your-deepgram-api-key
```

## Agent Code (`src/agent.py`)

Create `src/agent.py` with:

```python
from livekit.agents import agents, AgentServer, AgentSession, Agent, inference
from livekit.plugins import deepgram, silero

server = AgentServer()

@server.rtc_session(agent_name="deepgram-agent")
async def session_handler(ctx):
    class Assistant(Agent):
        instructions = "You are a helpful voice assistant."

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),  # picks up DEEPGRAM_API_KEY from env
        llm=inference.LLM(model="openai/gpt-4o"),
        tts=inference.TTS(model="cartesia/sonic-3"),
        vad=silero.VAD.load(),
    )
    await session.start(room=ctx.room, agent=Assistant())

if __name__ == "__main__":
    agents.cli.run_app(server)
```

**Key difference from the standard agent**: Instead of `inference.STT(model="deepgram/nova-3")`, this agent uses `deepgram.STT(model="nova-3")` from the Deepgram plugin directly, which reads `DEEPGRAM_API_KEY` from the environment automatically.

## Install Dependencies

Run `uv sync` to install all dependencies and create the `.venv`.
