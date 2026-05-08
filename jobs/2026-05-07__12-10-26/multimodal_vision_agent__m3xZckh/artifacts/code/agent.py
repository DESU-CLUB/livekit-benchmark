import asyncio

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, silero


# ---------------------------------------------------------------------------
# Global server instance
# ---------------------------------------------------------------------------
server = AgentServer()

# Module-level reference to the latest video stream so describe_scene can use it
_video_stream: rtc.VideoStream | None = None


# ---------------------------------------------------------------------------
# Assistant definition
# ---------------------------------------------------------------------------
class VisionAssistant(Agent):
    """A voice + vision assistant that periodically describes what it sees."""

    def __init__(self) -> None:
        super().__init__(
            instructions="You are a vision assistant. Describe what you see in the video."
        )

    async def describe_scene(self) -> None:
        """Capture the latest video frame and ask the LLM to describe the scene."""
        global _video_stream

        if _video_stream is None:
            return

        # Grab one frame from the video stream
        frame_event: rtc.VideoFrameEvent | None = None
        async for event in _video_stream:
            frame_event = event
            break  # we only need a single frame

        if frame_event is None:
            return

        # Build a chat message that includes the captured image and ask the LLM
        # to describe what it sees.
        image_content = agents.llm.ChatImage(image=frame_event.frame)
        chat_message = agents.llm.ChatMessage(
            role="user",
            content=[
                image_content,
                "Please describe what you see in this video frame.",
            ],
        )

        # Use the session's LLM directly to get a description, then speak it.
        session: AgentSession = self.session  # type: ignore[attr-defined]
        response = await session.llm.chat(
            chat_ctx=agents.llm.ChatContext(messages=[chat_message])
        )

        description_parts: list[str] = []
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                description_parts.append(content)

        description = "".join(description_parts).strip()
        if description:
            await session.say(description)


# ---------------------------------------------------------------------------
# RTC session handler
# ---------------------------------------------------------------------------
@server.rtc_session(agent_name="vision-agent")
async def handle_rtc_session(ctx: agents.JobContext) -> None:
    global _video_stream

    # ------------------------------------------------------------------
    # Track-subscription handler: watch for incoming video tracks
    # ------------------------------------------------------------------
    @ctx.room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant,
    ) -> None:
        global _video_stream

        if track.kind == rtc.TrackKind.KIND_VIDEO:
            # Replace any existing stream with the newly subscribed track
            _video_stream = rtc.VideoStream(track)

    # ------------------------------------------------------------------
    # Build the agent session with STT / LLM / TTS / VAD
    # ------------------------------------------------------------------
    session = AgentSession(
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o"),
        tts=openai.TTS(),
        vad=silero.VAD.load(),
    )

    assistant = VisionAssistant()

    # ------------------------------------------------------------------
    # Periodic loop: every 5 seconds, capture a frame and describe it
    # ------------------------------------------------------------------
    async def periodic_describe() -> None:
        while True:
            await asyncio.sleep(5)
            try:
                await assistant.describe_scene()
            except Exception as exc:  # pragma: no cover
                print(f"[vision-agent] describe_scene error: {exc}")

    asyncio.create_task(periodic_describe())

    # ------------------------------------------------------------------
    # Connect to the room and start the session
    # ------------------------------------------------------------------
    await ctx.connect()
    await session.start(room=ctx.room, agent=assistant)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agents.cli.run_app(server)
