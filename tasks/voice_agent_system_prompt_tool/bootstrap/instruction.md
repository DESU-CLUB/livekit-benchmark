# Build a LiveKit Voice Agent with System Prompt and Function Tools

Create a LiveKit voice agent at `/home/user/livekit-agent` using Python and `uv`.

## Project Setup

1. Initialize the project with `uv init` or create `pyproject.toml` manually.
2. Create `pyproject.toml` with:
   - Project name: `livekit-agent`
   - Python version: `>=3.11`
   - Dependencies: `livekit-agents[codecs,turn-detector]`, `livekit-plugins-silero`, `python-dotenv`

## Agent Code (`src/agent.py`)

Create `src/agent.py` with the following structure:

- Import `agents`, `AgentServer`, `AgentSession`, `Agent`, `inference` from `livekit.agents`
- Import `silero` from `livekit.plugins`
- Create `server = AgentServer()`
- Define a session handler with `@server.rtc_session(agent_name="assistant-agent")`
- Inside the handler, define an `Assistant` class extending `Agent` with:
  - `instructions`: a system prompt saying it is a helpful assistant that can tell the current time and date
  - Two method tools decorated with `@agents.function_tool`:
    - `get_current_time(self)` — returns the current time as a string (e.g. `"The current time is 14:35:22"`)
    - `get_current_date(self)` — returns today's date as a string (e.g. `"Today's date is 2024-01-15"`)
- Create an `AgentSession` with `inference.STT`, `inference.LLM`, `inference.TTS`, and `silero.VAD.load()`
- Start the session with `await session.start(room=ctx.room, agent=Assistant())`
- Entry point: `if __name__ == "__main__": agents.cli.run_app(server)`

## Environment

Create `.env.local` with placeholder values:
```
LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```

## Install Dependencies

Run `uv sync` to install all dependencies and create the `.venv`.
