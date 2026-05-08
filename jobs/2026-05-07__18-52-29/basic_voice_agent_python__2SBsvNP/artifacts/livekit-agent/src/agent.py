from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession, TurnHandlingOptions, inference
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

server = AgentServer()


@server.rtc_session(agent_name="my-voice-agent")
async def handle_session(ctx: agents.JobContext) -> None:
    class Assistant(Agent):
        def __init__(self) -> None:
            super().__init__(instructions="You are a helpful voice assistant.")

    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3"),
        llm=inference.LLM(model="openai/gpt-4o"),
        tts=inference.TTS(model="cartesia/sonic-3"),
        vad=silero.VAD.load(),
        turn_handling=TurnHandlingOptions(turn_detection=MultilingualModel()),
    )

    await session.start(room=ctx.room, agent=Assistant())
    await session.generate_reply(instructions="Greet the user.")


if __name__ == "__main__":
    agents.cli.run_app(server)
