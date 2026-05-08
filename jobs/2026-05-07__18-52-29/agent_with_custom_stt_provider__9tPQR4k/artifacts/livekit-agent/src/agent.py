from __future__ import annotations

import asyncio
import os
from pathlib import Path

from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.plugins import deepgram, silero

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env.local"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        os.environ.setdefault(key, value)


def _require_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


async def _transcribe_track(
    stt: deepgram.STT,
    track: rtc.Track,
    participant: rtc.RemoteParticipant,
) -> None:
    stt_stream = stt.stream()
    audio_stream = rtc.AudioStream(track)

    async for audio_event in audio_stream:
        if audio_event.frame is None:
            continue
        await stt_stream.push_frame(audio_event.frame)

        async for event in stt_stream:
            if not getattr(event, "is_final", False):
                continue
            text = getattr(event, "text", "").strip()
            if text:
                identity = participant.identity or "participant"
                print(f"{identity}: {text}")


@cli.agent(name="deepgram-agent")
async def entrypoint(ctx: JobContext) -> None:
    _load_env_file(ENV_PATH)
    api_key = _require_env("DEEPGRAM_API_KEY")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    stt = deepgram.STT(api_key=api_key, model="nova-3")
    silero.VAD.load()

    @ctx.room.on("track_subscribed")
    def _on_track_subscribed(
        track: rtc.Track,
        _publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant,
    ) -> None:
        if track.kind != rtc.TrackKind.KIND_AUDIO:
            return
        asyncio.create_task(_transcribe_track(stt, track, participant))


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
