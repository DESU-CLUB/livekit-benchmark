import logging
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    AgentServer,
    cli,
    llm,
)
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import deepgram, openai, silero

load_dotenv(dotenv_path=".env.local")

logger = logging.getLogger("voice-agent")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

server = AgentServer(setup_fnc=prewarm)

@server.rtc_session(agent_name="deepgram-agent")
async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text="You are a voice assistant created by LiveKit. Keep your responses concise and polite.",
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    stt = deepgram.STT(model="nova-3")
    vad = ctx.proc.userdata.get("vad") or silero.VAD.load()
    llm_model = openai.LLM()
    tts = openai.TTS()

    agent = Agent(
        instructions="You are a voice assistant created by LiveKit. Keep your responses concise and polite.",
        stt=stt,
        llm=llm_model,
        tts=tts,
        vad=vad,
        chat_ctx=initial_ctx,
    )

    session = AgentSession(
        stt=stt,
        vad=vad,
        llm=llm_model,
        tts=tts,
    )
    
    await session.start(agent, room=ctx.room)
    await session.say("Hey, how can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(server)
