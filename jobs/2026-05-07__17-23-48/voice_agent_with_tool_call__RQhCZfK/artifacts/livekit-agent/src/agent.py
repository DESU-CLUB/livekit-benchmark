from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, inference
from livekit.plugins import silero


class WeatherAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful weather assistant. Users will ask you about the weather in various locations. Use the get_weather function tool to look up weather information for the requested location."
        )

    @agents.function_tool
    def get_weather(self, location: str) -> str:
        """Get the current weather for a given location."""
        return f"The weather in {location} is sunny and 72°F."


server = AgentServer()


@server.rtc_session(agent_name="weather-agent")
async def handle_session(room: AgentSession):
    session = AgentSession(
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=silero.VAD.load(),
    )
    
    await session.start(room, WeatherAssistant())
    
    await session.say("Hello! I'm your weather assistant. Ask me about the weather in any location, and I'll help you out!")


if __name__ == "__main__":
    agents.cli.run_app(server)