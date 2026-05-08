from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession
from livekit.plugins import openai as lk_openai


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice assistant.")


server = AgentServer()


@server.rtc_session(agent_name="realtime-agent")
async def realtime_agent_session(ctx: agents.JobContext) -> None:
    session = AgentSession(llm=lk_openai.realtime.RealtimeModel(voice="coral"))
    await session.start(ctx.room, Assistant())
    await session.generate_reply(text="Hello! How can I help you today?")


if __name__ == "__main__":
    agents.cli.run_app(server)
