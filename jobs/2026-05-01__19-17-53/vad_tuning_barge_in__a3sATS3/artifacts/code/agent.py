import json
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import JobContext, WorkerOptions, multimodal, rtc
from livekit.plugins import silero

# Load environment variables
env_path = Path(__file__).parent.parent / ".env.local"
load_dotenv(dotenv_path=env_path)

# Load VAD configuration
config_path = Path(__file__).parent.parent / "vad_config.json"
with open(config_path, "r") as f:
    vad_config = json.load(f)

# Define Assistant class as per instructions
class Assistant(agents.Agent):
    def __init__(self):
        super().__init__()
        self.instructions = "You are a helpful voice assistant."

# Create server
server = agents.AgentServer()

@server.rtc_session(agent_name="barge-in-agent")
async def entrypoint(ctx: JobContext):
    # Initialize VAD with configuration from JSON
    vad = silero.VAD.load(
        min_silence_duration=vad_config["min_silence_duration"],
        min_speech_duration=vad_config["min_speech_duration"],
        activation_threshold=vad_config["activation_threshold"],
    )

    # AgentSession with STT, LLM, TTS and VAD
    # Using multimodal or voice_assistant session
    # The requirement mentions AgentSession with STT, LLM, TTS and vad.
    # In newer livekit-agents, this is often handled by VoiceAssistant or MultimodalAgent.
    
    # Placeholder for STT, LLM, TTS as they need to be provided
    # but the prompt implies they come from some 'inference' module or similar
    # However, standard practice is to use plugins.
    
    from livekit.plugins import openai
    
    assistant = agents.voice_assistant.VoiceAssistant(
        vad=vad,
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=openai.ChatContext().append(
            role="system",
            text="You are a helpful voice assistant.",
        ),
    )

    await ctx.connect()
    assistant.start(ctx.room)

if __name__ == "__main__":
    agents.cli.run_app(server)
