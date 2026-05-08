import asyncio
import logging
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, inference
from livekit.plugins import silero

load_dotenv(dotenv_path=".env.local")

logger = logging.getLogger("weather-agent")
logger.setLevel(logging.INFO)

class WeatherAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful weather assistant. You can check the weather for users using the get_weather tool."
        )

    @agents.function_tool
    def get_weather(self, location: str) -> str:
        """Get the current weather for a location."""
        return f"The weather in {location} is sunny and 72°F."

server = AgentServer()

@server.rtc_session(agent_name="weather-agent")
async def session(room, ctx):
    agent_session = AgentSession(
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=silero.VAD.load()
    )
    
    agent = WeatherAssistant()
    await agent_session.start(room, agent)
    await agent_session.generate_reply("Hello! I am your weather assistant. How can I help you today?")

if __name__ == "__main__":
    agents.cli.run_app(server)
