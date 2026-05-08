from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import livekit.agents as agents
from livekit.agents import Agent, AgentSession, RoomInputOptions, function_tool
from livekit.plugins import silero


SYSTEM_PROMPT = """You are a helpful voice assistant named Alex. You have a warm, 
friendly, and conversational personality. Keep your responses concise and natural 
for spoken conversation. You can help users with general questions and, when asked, 
you are able to provide the current time and date."""


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_PROMPT)

    @function_tool
    async def get_current_time(self) -> str:
        """Returns the current UTC time in HH:MM:SS format."""
        now = datetime.now(timezone.utc)
        return now.strftime("%H:%M:%S UTC")

    @function_tool
    async def get_current_date(self) -> str:
        """Returns the current UTC date in YYYY-MM-DD format."""
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%d")


async def entrypoint(ctx: agents.JobContext) -> None:
    await ctx.connect()

    session = AgentSession(
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(),
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="assistant-agent",
        )
    )
