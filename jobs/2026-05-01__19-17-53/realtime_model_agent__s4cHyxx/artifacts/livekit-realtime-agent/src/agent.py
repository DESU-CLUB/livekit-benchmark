import logging
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import (
    Agent,
    AgentSession,
    AgentServer,
    JobContext,
    JobProcess,
)
from livekit.plugins import openai as lk_openai

load_dotenv(dotenv_path=".env.local")

logger = logging.getLogger("realtime-agent")
logger.setLevel(logging.INFO)


class Assistant(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant.")


server = AgentServer()


@server.rtc_session(agent_name="realtime-agent")
async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    
    # OpenAI Realtime Model
    model = lk_openai.realtime.RealtimeModel(voice="coral")
    
    # Agent Session
    session = AgentSession(llm=model)
    
    # Assistant instance
    assistant = Assistant()
    
    # Start the session
    await session.start(ctx.room, assistant)
    
    # Generate initial greeting
    await session.say("Hello! How can I help you today?")


if __name__ == "__main__":
    agents.cli.run_app(server)
