import datetime
import logging

from livekit.agents import (
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    function_tool,
    inference,
)
from livekit.agents.voice import Agent
from livekit.plugins import silero

logger = logging.getLogger("assistant-agent")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful and concise voice assistant. "
                "You can provide the current time and date when asked."
            ),
        )

    @function_tool
    def get_current_time(self) -> str:
        """Get the current time in the user's timezone."""
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")

    @function_tool
    def get_current_date(self) -> str:
        """Get the current date in the user's timezone."""
        now = datetime.datetime.now()
        return now.strftime("%A, %B %d, %Y")


server = AgentServer()

def prewarm(proc: JobProcess) -> None:
    proc.userdata["vad"] = silero.VAD.load()

server.setup_fnc = prewarm

@server.rtc_session(agent_name="assistant-agent")
async def entrypoint(ctx: JobContext) -> None:
    session = AgentSession(
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=ctx.proc.userdata["vad"],
    )

    await session.start(
        agent=Assistant(),
        room=ctx.room,
    )

if __name__ == "__main__":
    cli.run_app(server)
