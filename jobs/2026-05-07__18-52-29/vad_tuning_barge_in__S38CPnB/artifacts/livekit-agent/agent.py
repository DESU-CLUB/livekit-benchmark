import json
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, AgentServer
from livekit.agents import cli, inference
from livekit.plugins import silero


load_dotenv(".env.local")


def load_vad_config() -> dict:
    config_path = Path(__file__).resolve().parents[1] / "vad_config.json"
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice assistant.")


server = AgentServer()


@server.rtc_session(agent_name="barge-in-agent")
async def assistant_session(session: AgentSession) -> None:
    vad_config = load_vad_config()
    vad = silero.VAD.load(
        min_silence_duration=vad_config["min_silence_duration"],
        min_speech_duration=vad_config["min_speech_duration"],
        activation_threshold=vad_config["activation_threshold"],
    )

    await session.start(
        Assistant(),
        vad=vad,
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
    )


if __name__ == "__main__":
    cli.run_app(server)
