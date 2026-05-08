import asyncio
from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent
from livekit.plugins import openai as lk_openai

class Assistant(Agent):
    instructions = "You are a helpful voice assistant."

server = AgentServer()

@server.rtc_session(agent_name="realtime-agent")
async def session(ctx: agents.JobContext):
    session = AgentSession(
        llm=lk_openai.realtime.RealtimeModel(voice="coral")
    )
    await session.start(ctx.room, Assistant())
    
    # Generate an initial greeting reply
    await session.generate_reply("Hello! How can I help you today?")

if __name__ == "__main__":
    agents.cli.run_app(server)
