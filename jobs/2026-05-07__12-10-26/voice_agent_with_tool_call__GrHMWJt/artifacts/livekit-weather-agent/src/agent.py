from dotenv import load_dotenv

load_dotenv(".env.local")

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, inference
from livekit.plugins import silero


class WeatherAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful weather assistant. "
                "You help users check the current weather for any location they ask about. "
                "When a user asks about the weather somewhere, use the get_weather tool to look it up "
                "and relay the information in a friendly, conversational way."
            )
        )

    @agents.function_tool
    async def get_weather(self, location: str) -> str:
        """Look up the current weather for a given location.

        Args:
            location: The city or location to get weather for.
        """
        return f"The weather in {location} is sunny and 72°F."


server = AgentServer()


@server.rtc_session(agent_name="weather-agent")
async def handle_session(session: AgentSession, room) -> None:
    await session.start(
        agent=WeatherAssistant(),
        room=room,
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=silero.VAD.load(),
    )

    await session.generate_reply(
        instructions="Greet the user and let them know you can help them check the weather for any location."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
