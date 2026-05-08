import asyncio
from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent
from livekit.plugins import openai

server = AgentServer()


class VisionAssistant(Agent):
    instructions = "You are a vision assistant. Describe what you see in the video."

    async def describe_scene(self):
        pass


@server.rtc_session(agent_name="vision-agent")
async def vision_agent(ctx: agents.JobContext):
    video_stream = None

    @ctx.room.on("track_subscribed")
    def on_track_subscribed(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.RemoteParticipant):
        nonlocal video_stream
        if track.kind == rtc.TrackKind.KIND_VIDEO:
            video_stream = rtc.VideoStream(track)

    session = AgentSession(
        stt=openai.stt.STT(),
        llm=openai.llm.LLM(),
        tts=openai.tts.TTS(),
        vad=openai.vad.VAD(),
    )

    async def periodic_describe():
        while True:
            await asyncio.sleep(5)
            await VisionAssistant().describe_scene()

    asyncio.create_task(periodic_describe())

    await ctx.connect()
    await session.start(room=ctx.room, agent=VisionAssistant())


if __name__ == "__main__":
    agents.cli.run_app(server)