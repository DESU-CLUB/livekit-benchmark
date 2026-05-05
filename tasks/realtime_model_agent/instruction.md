## Background

LiveKit Agents supports OpenAI's Realtime API, which provides a speech-to-speech model that handles STT, LLM reasoning, and TTS in a single low-latency pipeline. This eliminates the need to wire up separate STT, LLM, and TTS components.

## Requirements

Create a Python LiveKit voice agent that uses the OpenAI Realtime Model (`lk_openai.realtime.RealtimeModel`) with voice `"coral"` instead of the standard STT-LLM-TTS pipeline.

## Implementation Guide

1. Navigate to `/home/user/livekit-agent`.
2. Create `pyproject.toml` with:
   - `name = "livekit-realtime-agent"`
   - `requires-python = ">=3.11"`
   - Dependencies: `livekit-agents[codecs]`, `livekit-plugins-openai`, `python-dotenv`
3. Create `.env.local` with placeholder values:
   ```
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   LIVEKIT_URL=wss://your-livekit-server
   OPENAI_API_KEY=your-openai-api-key
   ```
4. Create `src/agent.py` with:
   - Imports: `agents` from `livekit`, `AgentServer`, `AgentSession`, `Agent` from `livekit.agents`
   - `from livekit.plugins import openai as lk_openai`
   - An `Assistant(Agent)` class with `instructions="You are a helpful voice assistant."`
   - An `AgentServer` instance
   - `@server.rtc_session(agent_name="realtime-agent")` async function that:
     - Creates `AgentSession(llm=lk_openai.realtime.RealtimeModel(voice="coral"))`
     - Starts the session with `ctx.room` and an `Assistant()` instance
     - Generates an initial greeting reply
   - `if __name__ == "__main__":` block calling `agents.cli.run_app(server)`
5. Run `uv sync` to install dependencies and create `.venv`.

## Constraints

- Project path: `/home/user/livekit-agent`
- All files must be created under `/home/user/livekit-agent`

## Integrations

- LiveKit Agents Python SDK
- OpenAI Realtime Plugin
