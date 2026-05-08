import agents
from livekit.agents import AgentServer, AgentSession, Agent
from livekit.plugins import openai as lk_openai


class Assistant(Agent):
    instructions = "You are a helpful voice assistant."


server = AgentServer()


@server.rtc_session(agent_name="realtime-agent")
async def handler(ctx: agents.JobContext):
    session = AgentSession(
        llm=lk_openai.realtime.RealtimeModel(voice="coral")
    )
    await session.start(ctx.room, Assistant())
    
    # Generate an initial greeting
    await session.generate_reply()


if __name__ == "__main__":
    agents.cli.run_app(server)