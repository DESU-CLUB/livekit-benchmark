import json
import os
from pathlib import Path

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession, inference
from livekit.plugins import silero

# Load environment variables from .env.local
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env.local")

# Read VAD configuration from vad_config.json at project root
_config_path = Path(__file__).parent.parent / "vad_config.json"
with open(_config_path) as f:
    vad_config = json.load(f)

server = AgentServer()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice assistant.")


@server.rtc_session(agent_name="barge-in-agent")
async def handle_session(session: AgentSession) -> None:
    vad = silero.VAD.load(
        min_silence_duration=vad_config["min_silence_duration"],
        min_speech_duration=vad_config["min_speech_duration"],
        activation_threshold=vad_config["activation_threshold"],
    )

    await session.start(
        agent=Assistant(),
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=vad,
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
