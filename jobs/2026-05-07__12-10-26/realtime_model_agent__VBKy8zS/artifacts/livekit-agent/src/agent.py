from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent
from livekit.plugins import openai as lk_openai


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice assistant.")


server = AgentServer()


@server.rtc_session(agent_name="realtime-agent")
async def session_handler(ctx: agents.JobContext) -> None:
    session = AgentSession(
        llm=lk_openai.realtime.RealtimeModel(voice="coral"),
    )

    await session.start(ctx.room, agent=Assistant())

    await session.generate_reply(
        instructions="Greet the user with a friendly welcome message."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
