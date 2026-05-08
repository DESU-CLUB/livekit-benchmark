#!/usr/bin/env python3
import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict

from livekit.api import DataPacketKind, ListRoomsRequest, LiveKitAPI, SendDataRequest

ENV_PATH = Path(__file__).with_name(".env.local")
LOG_PATH = Path(__file__).with_name("broadcast.log")


def load_env(path: Path) -> Dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing env file: {path}")

    env: Dict[str, str] = {}
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        env[key.strip()] = value.strip().strip("\"'")
    return env


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler(sys.stdout),
        ],
    )


async def broadcast(message: str) -> None:
    env = load_env(ENV_PATH)
    api_key = env.get("LIVEKIT_API_KEY")
    api_secret = env.get("LIVEKIT_API_SECRET")
    api_url = env.get("LIVEKIT_URL")

    if not api_key or not api_secret or not api_url:
        raise RuntimeError("LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and LIVEKIT_URL are required")

    api = LiveKitAPI(api_url, api_key, api_secret)
    try:
        logging.info("Listing active rooms...")
        rooms_response = await api.room.list_rooms(ListRoomsRequest())
        rooms = rooms_response.rooms or []

        if not rooms:
            logging.info("No active rooms found.")
            return

        logging.info("Found %d active room(s).", len(rooms))
        for room in rooms:
            logging.info("Broadcasting to room '%s'", room.name)
            await api.room.send_data(
                SendDataRequest(
                    room=room.name,
                    data=message.encode("utf-8"),
                    kind=DataPacketKind.DATA_PACKET_KIND_RELIABLE,
                )
            )
        logging.info("Broadcast complete.")
    finally:
        await api.aclose()


async def main() -> None:
    configure_logging()
    message = "System notification: scheduled maintenance will begin soon."
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    logging.info("Using message: %s", message)
    await broadcast(message)


if __name__ == "__main__":
    asyncio.run(main())
