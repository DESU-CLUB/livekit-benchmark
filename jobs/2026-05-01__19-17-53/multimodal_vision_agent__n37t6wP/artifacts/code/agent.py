import asyncio
import logging
from dotenv import load_dotenv
from livekit import rtc, agents
from livekit.agents import AgentServer, AgentSession, Agent, JobContext, WorkerOptions, cli, llm
from livekit.plugins import openai, silero

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("vision-agent")
logger.setLevel(logging.INFO)

server = AgentServer()

class VisionAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a vision assistant. Describe what you see in the video."
        )
        self._video_stream: rtc.VideoStream | None = None

    @property
    def video_stream(self) -> rtc.VideoStream | None:
        return self._video_stream

    @video_stream.setter
    def video_stream(self, stream: rtc.VideoStream | None):
        self._video_stream = stream

    async def describe_scene(self, session: AgentSession):
        if not self._video_stream:
            logger.info("No video stream available to describe")
            return

        # Get the latest frame from the video stream
        async for frame_event in self._video_stream:
            frame = frame_event.frame
            
            # Use the session to chat with the LLM about the frame
            # This is a conceptual implementation based on the requirements
            await session.chat.send_message(
                llm.ChatMessage(
                    role="user",
                    content=[
                        "Please describe what you see in this frame.",
                        llm.ChatImage(image=frame)
                    ]
                )
            )
            logger.info("Vision Assistant description requested")
            break # Just process one frame

@server.rtc_session(agent_name="vision-agent")
async def vision_agent_handler(ctx: JobContext):
    logger.info("starting vision-agent session")
    
    assistant = VisionAssistant()

    @ctx.room.on("track_subscribed")
    def on_track_subscribed(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.RemoteParticipant):
        if track.kind == rtc.TrackKind.KIND_VIDEO:
            logger.info(f"Subscribed to video track: {track.sid} from {participant.identity}")
            assistant.video_stream = rtc.VideoStream(track)

    # Create AgentSession with STT, LLM, TTS, VAD
    session = AgentSession(
        stt=silero.STT(), # Using silero as a common choice if not specified
        llm=openai.LLM(model="gpt-4o"),
        tts=openai.TTS(),
        vad=silero.VAD()
    )

    async def periodic_description():
        while True:
            await asyncio.sleep(5)
            await assistant.describe_scene(session)

    asyncio.create_task(periodic_description())

    await ctx.connect()
    await session.start(room=ctx.room, agent=assistant)

if __name__ == "__main__":
    agents.cli.run_app(server)
