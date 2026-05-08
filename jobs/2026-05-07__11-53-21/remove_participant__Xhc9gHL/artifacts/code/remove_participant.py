import asyncio
import os
from livekit import api

async def main():
    try:
        url = os.getenv("LIVEKIT_URL")
        api_key = os.getenv("LIVEKIT_API_KEY")
        api_secret = os.getenv("LIVEKIT_API_SECRET")

        async with api.LiveKitAPI(url, api_key, api_secret) as lkapi:
            await lkapi.room.remove_participant(
                api.RoomParticipantIdentity(room='demo-room', identity='user-123')
            )
            message = "Successfully removed participant user-123 from demo-room\n"
    except Exception as e:
        message = f"Failed to remove participant: {e}\n"
    
    with open('/home/user/livekit-admin/output.log', 'a') as f:
        f.write(message)

if __name__ == "__main__":
    asyncio.run(main())
