import logging

from dotenv import load_dotenv
from livekit.agents import (
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
)
from livekit.agents.voice import Agent
from livekit.plugins import deepgram, silero

load_dotenv(dotenv_path=".env.local")

logger = logging.getLogger("deepgram-agent")


class DeepgramAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a basic voice agent using Deepgram STT directly."
        )


server = AgentServer()


def prewarm(proc: JobProcess) -> None:
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="deepgram-agent")
async def entrypoint(ctx: JobContext) -> None:
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }
    
    session = AgentSession(
        stt=deepgram.STT(),
        vad=ctx.proc.userdata["vad"],
    )

    await session.start(
        agent=DeepgramAgent(),
        room=ctx.room,
    )


if __name__ == "__main__":
    cli.run_app(server)
