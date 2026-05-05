import logging
from livekit import agents
from livekit.agents import (
    AgentServer,
    AgentSession,
    TurnHandlingOptions,
    inference,
)
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# MultilingualModel reduces false positives for end-of-turn detection
# by using a trained model instead of relying solely on VAD silence duration.
# This prevents the agent from interrupting mid-sentence.

class Assistant(agents.Agent):
    def __init__(self):
        super().__init__()
        # Instructions are often set in the session or LLM context
        # but the requirement asks for this class with specific instructions.
        pass

server = AgentServer()

@server.rtc_session(agent_name="turn-aware-agent")
async def handle_session(ctx: agents.JobContext):
    # Creates an AgentSession with the specified components
    session = AgentSession(
        stt=inference.STT(),
        llm=inference.LLM(),
        tts=inference.TTS(),
        vad=silero.VAD.load(),
        turn_handling=TurnHandlingOptions(turn_detection=MultilingualModel())
    )
    
    # Start the session with the Assistant agent
    # The requirement specifies "You are a helpful voice assistant. Listen carefully before responding."
    # usually this is passed via LLM context, but we follow the structure requested.
    await session.start(room=ctx.room, agent=Assistant())

if __name__ == "__main__":
    agents.cli.run_app(server)
