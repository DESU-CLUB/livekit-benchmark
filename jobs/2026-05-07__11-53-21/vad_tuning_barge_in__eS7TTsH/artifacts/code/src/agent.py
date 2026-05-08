import json
import os
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, JobContext, inference
from livekit.plugins import silero

# Load environment variables from .env.local
load_dotenv(".env.local")

# Read VAD configuration
with open("vad_config.json", "r") as f:
    vad_config = json.load(f)

server = AgentServer()

class Assistant(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant.")

@server.rtc_session(agent_name="barge-in-agent")
async def handle_session(ctx: JobContext):
    await ctx.connect()
    
    vad = silero.VAD.load(
        min_silence_duration=vad_config["min_silence_duration"],
        min_speech_duration=vad_config["min_speech_duration"],
        activation_threshold=vad_config["activation_threshold"]
    )
    
    session = AgentSession(
        stt=inference.STT,
        llm=inference.LLM,
        tts=inference.TTS,
        vad=vad
    )
    
    agent = Assistant()
    await session.start(agent, room=ctx.room)

if __name__ == "__main__":
    agents.cli.run_app(server)
