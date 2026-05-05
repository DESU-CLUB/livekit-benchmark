import logging
from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, inference
from livekit.plugins import silero

class WeatherAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a weather assistant. You can check the weather for users."
        )

    @agents.function_tool
    def get_weather(self, location: str) -> str:
        """Get the weather for a location"""
        return f"The weather in {location} is sunny and 72°F."

server = AgentServer()

@server.rtc_session(agent_name="weather-agent")
async def entrypoint(room: agents.Room):
    # Creates an AgentSession with inference.STT, inference.LLM, inference.TTS, and silero.VAD.load()
    session = AgentSession(
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=silero.VAD.load(),
    )

    # Starts the session with the room and a WeatherAssistant instance
    await session.start(room, WeatherAssistant())

    # Generates an initial reply greeting the user
    session.generate_reply("Hello! I'm your weather assistant. How can I help you today?")

if __name__ == "__main__":
    agents.cli.run_app(server)
