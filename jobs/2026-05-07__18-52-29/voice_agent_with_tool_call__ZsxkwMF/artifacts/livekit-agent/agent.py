from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession, inference
from livekit.plugins import silero


class WeatherAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a friendly weather assistant. Answer questions about the weather "
                "by calling the get_weather tool when a location is provided."
            )
        )

    @agents.function_tool
    def get_weather(self, location: str) -> str:
        return f"The weather in {location} is sunny and 72°F."


server = AgentServer()


@server.rtc_session(agent_name="weather-agent")
async def weather_agent_session(ctx: agents.SessionContext) -> None:
    session = AgentSession(
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=silero.VAD.load(),
    )
    await session.start(ctx.room, WeatherAssistant())
    await session.generate_reply(
        "Hi there! Ask me about the weather in any city and I'll look it up for you."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
