#!/usr/bin/env python3
"""
LiveKit Room Broadcast Script

This script lists all active LiveKit rooms and broadcasts a system message
to each one using the Room Service send_data API.
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from livekit import api
from livekit.api import (
    LiveKitAPI,
    ListRoomsRequest,
    SendDataRequest,
)

# Load environment variables from .env.local
load_dotenv(".env.local")

# Configure logging
LOG_FILE = "broadcast.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def get_livekit_client() -> Optional[LiveKitAPI]:
    """
    Initialize and return a LiveKit API client.
    
    Returns:
        LiveKitAPI: Configured API client, or None if credentials are missing.
    """
    url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    if not all([url, api_key, api_secret]):
        logger.error("Missing required environment variables. Please ensure LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET are set.")
        return None
    
    try:
        client = LiveKitAPI(url, api_key, api_secret)
        logger.info(f"Successfully initialized LiveKit API client for URL: {url}")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize LiveKit API client: {e}")
        return None


def list_active_rooms(client: LiveKitAPI) -> list:
    """
    List all active LiveKit rooms.
    
    Args:
        client: LiveKitAPI client instance.
        
    Returns:
        list: List of active room names.
    """
    try:
        logger.info("Fetching list of active rooms...")
        rooms = client.room.list_rooms(ListRoomsRequest())
        room_names = [room.name for room in rooms]
        logger.info(f"Found {len(room_names)} active room(s): {room_names}")
        return room_names
    except Exception as e:
        logger.error(f"Failed to list rooms: {e}")
        return []


def broadcast_message(client: LiveKitAPI, room_name: str, message: str) -> bool:
    """
    Broadcast a message to a specific LiveKit room.
    
    Args:
        client: LiveKitAPI client instance.
        room_name: Name of the room to broadcast to.
        message: Message content to broadcast.
        
    Returns:
        bool: True if broadcast was successful, False otherwise.
    """
    try:
        # Convert message to bytes for transmission
        payload = message.encode("utf-8")
        
        logger.info(f"Broadcasting message to room '{room_name}': {message}")
        
        # Send data to the room with reliable delivery
        # kind: 0 = RELIABLE, 1 = LOSSY
        client.room.send_data(
            SendDataRequest(
                room=room_name,
                data=payload,
                kind=0,  # RELIABLE delivery
            )
        )
        
        logger.info(f"Successfully broadcast message to room '{room_name}'")
        return True
    except Exception as e:
        logger.error(f"Failed to broadcast message to room '{room_name}': {e}")
        return False


def broadcast_to_all_rooms(message: str) -> dict:
    """
    Broadcast a message to all active LiveKit rooms.
    
    Args:
        message: Message content to broadcast to all rooms.
        
    Returns:
        dict: Summary of broadcast results with success/failure counts.
    """
    logger.info(f"Starting broadcast to all active rooms. Message: {message}")
    
    # Initialize LiveKit client
    client = get_livekit_client()
    if not client:
        logger.error("Failed to initialize LiveKit client. Aborting broadcast.")
        return {"success": 0, "failed": 0, "total": 0}
    
    try:
        # Get list of active rooms
        room_names = list_active_rooms(client)
        
        if not room_names:
            logger.info("No active rooms found. Nothing to broadcast.")
            return {"success": 0, "failed": 0, "total": 0}
        
        # Broadcast to each room
        success_count = 0
        failed_count = 0
        
        for room_name in room_names:
            if broadcast_message(client, room_name, message):
                success_count += 1
            else:
                failed_count += 1
        
        # Log summary
        total = success_count + failed_count
        logger.info(
            f"Broadcast completed. Success: {success_count}/{total}, Failed: {failed_count}/{total}"
        )
        
        return {
            "success": success_count,
            "failed": failed_count,
            "total": total,
        }
        
    finally:
        # Close the client connection
        client.close()
        logger.info("LiveKit API client closed.")


def main():
    """
    Main entry point for the broadcast script.
    """
    # Default system message
    default_message = "SYSTEM: Scheduled maintenance will begin in 30 minutes. Please save your work."
    
    # Get message from command line argument or use default
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else default_message
    
    logger.info(f"Broadcast script started at {datetime.now().isoformat()}")
    
    # Perform broadcast
    results = broadcast_to_all_rooms(message)
    
    # Exit with appropriate code
    if results["failed"] > 0:
        logger.warning(f"Broadcast completed with {results['failed']} failure(s)")
        sys.exit(1)
    else:
        logger.info("Broadcast completed successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()