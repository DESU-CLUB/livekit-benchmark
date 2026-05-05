## Background

LiveKit Agents supports function tools, allowing an LLM to invoke Python functions during a voice conversation. This enables agents to fetch live data, perform lookups, or trigger side effects mid-conversation.

## Requirements

Build a LiveKit Python voice agent that defines a function tool for weather lookups and registers it with an `Agent` subclass so the LLM can call it during a conversation.

## Implementation Guide

1. Navigate to the project directory `/home/user/livekit-agent`.
2. Create `pyproject.toml` with:
   - `name = "livekit-weather-agent"`
   - `requires-python = ">=3.11"`
   - Dependencies: `livekit-agents[codecs,turn-detector]`, `livekit-plugins-silero`, `python-dotenv`
3. Create `.env.local` with placeholder values:
   ```
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   LIVEKIT_URL=wss://your-livekit-server
   ```
4. Create `src/agent.py` with:
   - Import `agents` from `livekit`, import `AgentServer`, `AgentSession`, `Agent`, `inference` from `livekit.agents`
   - Import `silero` from `livekit.plugins`
   - Define `WeatherAssistant(Agent)` with instructions about checking the weather for users
   - Inside `WeatherAssistant`, define a method `get_weather(self, location: str) -> str` decorated with `@agents.function_tool` that returns `"The weather in {location} is sunny and 72°F."`
   - Create an `AgentServer` instance
   - Define an `@server.rtc_session(agent_name="weather-agent")` async function that:
     - Creates an `AgentSession` with `inference.STT`, `inference.LLM`, `inference.TTS`, and `silero.VAD.load()`
     - Starts the session with the room and a `WeatherAssistant` instance
     - Generates an initial reply greeting the user
   - Include `if __name__ == "__main__":` block calling `agents.cli.run_app(server)`
5. Run `uv sync` to install dependencies and create the `.venv`.

## Constraints

- Project path: `/home/user/livekit-agent`
- All files must be created under `/home/user/livekit-agent`

## Integrations

- LiveKit Agents Python SDK
