import asyncio
import os
from datetime import datetime

from livekit import api


LOG_PATH = "/home/user/livekit-admin/output.log"
ROOM_NAME = "demo-room"
PARTICIPANT_IDENTITY = "user-123"


def _format_message(message: str) -> str:
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    return f"[{timestamp}Z] {message}"


async def remove_participant() -> str:
    livekit_url = os.environ.get("LIVEKIT_URL")
    livekit_api_key = os.environ.get("LIVEKIT_API_KEY")
    livekit_api_secret = os.environ.get("LIVEKIT_API_SECRET")

    if not livekit_url or not livekit_api_key or not livekit_api_secret:
        return _format_message(
            "Missing LIVEKIT_URL, LIVEKIT_API_KEY, or LIVEKIT_API_SECRET in environment."
        )

    try:
        async with api.LiveKitAPI(
            livekit_url, livekit_api_key, livekit_api_secret
        ) as lkapi:
            await lkapi.room.remove_participant(
                api.RoomParticipantIdentity(room=ROOM_NAME, identity=PARTICIPANT_IDENTITY)
            )
        return _format_message(
            f"Removed participant '{PARTICIPANT_IDENTITY}' from room '{ROOM_NAME}'."
        )
    except Exception as exc:  # noqa: BLE001 - intentional broad catch for graceful handling
        return _format_message(
            f"Failed to remove participant '{PARTICIPANT_IDENTITY}' from room '{ROOM_NAME}': {exc}"
        )


async def main() -> None:
    result = await remove_participant()
    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(result + "\n")


if __name__ == "__main__":
    asyncio.run(main())
