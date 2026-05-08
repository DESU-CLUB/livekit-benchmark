import asyncio

from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import Agent, AgentServer, AgentSession
from livekit.agents.llm import ChatImage, ChatMessage, ChatRole
from livekit.plugins import openai, silero

load_dotenv(".env.local")

server = AgentServer()


class VisionAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a vision assistant. Describe what you see in the video."
        )
        self.latest_frame: rtc.VideoFrame | None = None

    async def consume_video(self, stream: rtc.VideoStream) -> None:
        async for frame in stream:
            self.latest_frame = frame

    async def describe_scene(self) -> None:
        if self.latest_frame is None or getattr(self, "session", None) is None:
            return

        message = ChatMessage(
            role=ChatRole.USER,
            content=[
                "Describe the scene in the video frame.",
                ChatImage(image=self.latest_frame),
            ],
        )
        response = await self.session.llm.chat(messages=[message])
        description = getattr(getattr(response, "message", None), "content", None)
        if description:
            print(f"Scene description: {description}")


@server.rtc_session(agent_name="vision-agent")
async def handle_session(ctx: agents.JobContext) -> None:
    assistant = VisionAssistant()

    @ctx.room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        _publication: rtc.RemoteTrackPublication,
        _participant: rtc.RemoteParticipant,
    ) -> None:
        if track.kind == rtc.TrackKind.KIND_VIDEO:
            stream = rtc.VideoStream(track)
            asyncio.create_task(assistant.consume_video(stream))

    session = AgentSession(
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(),
        vad=silero.VAD(),
    )

    async def scene_loop() -> None:
        while True:
            await assistant.describe_scene()
            await asyncio.sleep(5)

    asyncio.create_task(scene_loop())

    await ctx.connect()
    await session.start(room=ctx.room, agent=assistant)


if __name__ == "__main__":
    agents.cli.run_app(server)
