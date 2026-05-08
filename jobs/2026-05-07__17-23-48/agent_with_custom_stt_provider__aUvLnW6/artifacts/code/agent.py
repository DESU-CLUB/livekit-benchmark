"""
LiveKit Agent using Deepgram STT plugin
"""
import os
from livekit.agents import JobProcess, cli
from livekit.agents.worker import WorkerOptions
from livekit.agents.voice import Agent
from livekit.plugins import deepgram, silero


def prewarm(proc: JobProcess):
    """Prewarm the process by loading the STT and TTS models."""
    proc.userdata["stt"] = deepgram.STT(
        model="nova-3",
        language="en-US",
    )
    proc.userdata["tts"] = silero.TTS()


async def deepgram_agent(proc: JobProcess):
    """
    Voice agent that uses Deepgram STT plugin for speech recognition.
    
    This agent is configured to use Deepgram's nova-3 model for
    speech-to-text processing, providing high accuracy and low latency.
    """
    # Get Deepgram API key from environment
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
    
    if not deepgram_api_key:
        raise ValueError(
            "DEEPGRAM_API_KEY environment variable is not set. "
            "Please set it in your .env.local file."
        )
    
    # Update STT with API key
    stt = proc.userdata["stt"]
    stt._api_key = deepgram_api_key
    
    # Initialize the agent with Deepgram STT plugin
    agent = Agent(
        instructions="You are a helpful voice assistant.",
        stt=stt,
        tts=proc.userdata["tts"],
    )
    
    # Connect the agent to the room
    await agent.start(proc.room)


if __name__ == "__main__":
    # Run the agent using CLI
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=deepgram_agent,
            prewarm_fnc=prewarm,
        )
    )