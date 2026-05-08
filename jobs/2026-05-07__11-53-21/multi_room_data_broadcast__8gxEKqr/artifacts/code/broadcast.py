import os
import sys
import json
import asyncio
import logging
from dotenv import load_dotenv
from livekit.api import LiveKitAPI, ListRoomsRequest, SendDataRequest, DataPacket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/user/livekit-broadcast/broadcast.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def main():
    # Load environment variables from .env.local
    load_dotenv('/home/user/livekit-broadcast/.env.local')
    
    url = os.getenv('LIVEKIT_URL')
    api_key = os.getenv('LIVEKIT_API_KEY')
    api_secret = os.getenv('LIVEKIT_API_SECRET')
    
    if not url or not api_key or not api_secret:
        logger.error("Missing required environment variables (LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)")
        return

    # Message to broadcast
    message = {
        "type": "system_notification",
        "message": "System maintenance will begin shortly. Please save your work."
    }
    payload = json.dumps(message).encode('utf-8')

    # Initialize the LiveKit API client
    api = LiveKitAPI(url, api_key, api_secret)
    
    try:
        # List all active rooms
        logger.info("Fetching active rooms...")
        list_req = ListRoomsRequest()
        rooms_response = await api.room.list_rooms(list_req)
        
        rooms = rooms_response.rooms
        logger.info(f"Found {len(rooms)} active room(s).")
        
        # Broadcast the message to each room
        for room in rooms:
            logger.info(f"Sending message to room: {room.name}")
            send_req = SendDataRequest(
                room=room.name,
                data=payload,
                kind=DataPacket.Kind.RELIABLE
            )
            await api.room.send_data(send_req)
            logger.info(f"Message sent to room: {room.name}")
            
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        await api.aclose()

if __name__ == "__main__":
    asyncio.run(main())
