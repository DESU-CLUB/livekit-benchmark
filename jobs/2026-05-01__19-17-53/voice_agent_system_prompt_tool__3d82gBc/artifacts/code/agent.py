import asyncio
from datetime import datetime
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero

load_dotenv()


class AssistantFunctionTools(llm.FunctionContext):
    @llm.ai_callable(description="Returns the current time")
    def get_current_time(self) -> str:
        now = datetime.now()
        return now.strftime("%H:%M:%S")

    @llm.ai_callable(description="Returns the current date")
    def get_current_date(self) -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d")


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a helpful voice assistant. Your goal is to provide concise and accurate information. "
            "You have access to tools to fetch the current time and date. Use them when asked."
        ),
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=AssistantFunctionTools(),
    )

    assistant.start(ctx.room)

    await assistant.say("Hello, how can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="assistant-agent",
        )
    )
