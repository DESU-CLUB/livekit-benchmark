from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    TurnHandlingOptions,
    agents,
    inference,
)
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

server = AgentServer()

# MultilingualModel reduces false positives for end-of-turn detection
# by using a trained model instead of relying solely on VAD silence duration.
# This prevents the agent from interrupting mid-sentence.


class Assistant(Agent):
    instructions = "You are a helpful voice assistant. Listen carefully before responding."


@server.rtc_session(agent_name="turn-aware-agent")
async def turn_aware_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=silero.VAD.load(),
        turn_handling=TurnHandlingOptions(turn_detection=MultilingualModel()),
    )

    await session.start(room=ctx.room, agent=Assistant())


if __name__ == "__main__":
    agents.cli.run_app(server)