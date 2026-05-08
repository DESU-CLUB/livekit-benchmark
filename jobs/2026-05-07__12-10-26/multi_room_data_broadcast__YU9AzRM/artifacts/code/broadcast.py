"""
broadcast.py — Broadcast a system message to all active LiveKit rooms.

Reads credentials from .env.local, lists all active rooms via the LiveKit
Room Service API, and sends a binary data message to each room using
send_data with RELIABLE delivery.
"""

import asyncio
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from livekit import api
from livekit.api import room_service

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
ENV_FILE = BASE_DIR / ".env.local"
LOG_FILE = BASE_DIR / "broadcast.log"

MESSAGE = "System notice: scheduled maintenance in 15 minutes. Please save your work."

# DataPacket kind value: 0 = RELIABLE, 1 = LOSSY
DATA_PACKET_KIND_RELIABLE = 0

# ---------------------------------------------------------------------------
# Logging — write to both the log file and stdout
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_env() -> tuple[str, str, str]:
    """Load LiveKit credentials from .env.local and return (url, key, secret)."""
    load_dotenv(ENV_FILE)

    url = os.getenv("LIVEKIT_URL", "").strip()
    key = os.getenv("LIVEKIT_API_KEY", "").strip()
    secret = os.getenv("LIVEKIT_API_SECRET", "").strip()

    missing = [name for name, val in [("LIVEKIT_URL", url),
                                       ("LIVEKIT_API_KEY", key),
                                       ("LIVEKIT_API_SECRET", secret)]
               if not val]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}"
        )

    return url, key, secret


# ---------------------------------------------------------------------------
# Core broadcast logic
# ---------------------------------------------------------------------------

async def broadcast(message: str) -> None:
    """List all active rooms and send *message* to each one."""
    url, key, secret = load_env()

    logger.info("Connecting to LiveKit server: %s", url)

    async with api.LiveKitAPI(url=url, api_key=key, api_secret=secret) as lk:
        # 1. List active rooms
        list_response = await lk.room.list_rooms(
            room_service.ListRoomsRequest()
        )
        rooms = list_response.rooms

        if not rooms:
            logger.info("No active rooms found — nothing to broadcast.")
            return

        logger.info("Found %d active room(s).", len(rooms))

        # 2. Encode the message as UTF-8 bytes
        payload: bytes = message.encode("utf-8")

        # 3. Send to each room
        success_count = 0
        failure_count = 0

        for room in rooms:
            room_name: str = room.name
            try:
                await lk.room.send_data(
                    room_service.SendDataRequest(
                        room=room_name,
                        data=payload,
                        kind=DATA_PACKET_KIND_RELIABLE,
                    )
                )
                logger.info("Broadcast sent to room '%s'.", room_name)
                success_count += 1
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "Failed to send broadcast to room '%s': %s",
                    room_name,
                    exc,
                )
                failure_count += 1

        logger.info(
            "Broadcast complete — success: %d, failed: %d.",
            success_count,
            failure_count,
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    started_at = datetime.now(timezone.utc).isoformat()
    logger.info("=== LiveKit broadcast started at %s ===", started_at)
    logger.info("Message: %s", MESSAGE)

    try:
        asyncio.run(broadcast(MESSAGE))
    except Exception as exc:
        logger.exception("Broadcast failed with an unexpected error: %s", exc)
        raise


if __name__ == "__main__":
    main()
