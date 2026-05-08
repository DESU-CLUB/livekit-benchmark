import os
from dotenv import load_dotenv

from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import deepgram, silero

load_dotenv(dotenv_path=".env.local")


class DeepgramAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful voice assistant. "
                "Respond clearly and concisely to the user."
            ),
        )


async def entrypoint(ctx: JobContext) -> None:
    await ctx.connect()

    session = AgentSession(
        stt=deepgram.STT(
            model="nova-3",
            api_key=os.environ["DEEPGRAM_API_KEY"],
        ),
        vad=silero.VAD.load(),
    )

    await session.start(
        agent=DeepgramAgent(),
        room=ctx.room,
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="deepgram-agent",
        )
    )
