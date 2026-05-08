import json
import os
from pathlib import Path

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import inference
from livekit.plugins import silero


# Load environment variables from .env.local
load_dotenv()


# Load VAD configuration from vad_config.json
project_root = Path(__file__).parent.parent
vad_config_path = project_root / "vad_config.json"

with open(vad_config_path, "r") as f:
    vad_config = json.load(f)


# Create AgentServer
server = agents.AgentServer()


# Define the Assistant agent class
class Assistant(agents.Agent):
    instructions = "You are a helpful voice assistant."


# Create VAD instance with configuration from vad_config.json
vad = silero.VAD.load(
    min_silence_duration=vad_config["min_silence_duration"],
    min_speech_duration=vad_config["min_speech_duration"],
    activation_threshold=vad_config["activation_threshold"],
)


# Register the agent session with the server
@server.rtc_session(agent_name="barge-in-agent")
async def create_session() -> agents.AgentSession:
    return agents.AgentSession(
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=vad,
    )


if __name__ == "__main__":
    agents.cli.run_app(server)