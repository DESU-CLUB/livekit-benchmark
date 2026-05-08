from __future__ import annotations

from datetime import datetime, timezone

import livekit.agents as agents
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents.llm import ChatContext, ChatMessage, OpenAI
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import silero


@agents.function_tool
async def get_current_time() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%H:%M:%S UTC")


@agents.function_tool
async def get_current_date() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d")


@agents.agent(name="assistant-agent")
class Assistant(VoicePipelineAgent):
    def __init__(self) -> None:
        chat_ctx = ChatContext(
            messages=[
                ChatMessage(
                    role="system",
                    text=(
                        "You are Assistant, a friendly and concise voice agent. "
                        "Answer in short sentences and use the available tools "
                        "when a user asks for the current time or date."
                    ),
                )
            ]
        )
        super().__init__(
            vad=silero.VAD.load(),
            stt=silero.STT(),
            llm=OpenAI(model="gpt-4o-mini"),
            tts=silero.TTS(),
            chat_ctx=chat_ctx,
            tools=[get_current_time, get_current_date],
        )


async def entrypoint(ctx: JobContext) -> None:
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    assistant = Assistant()
    await assistant.start(ctx.room)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, agent_name="assistant-agent"))
