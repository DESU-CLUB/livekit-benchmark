import asyncio
from livekit import api
from livekit.protocol.models import ParticipantPermission


async def main():
    async with api.LiveKitAPI() as lkapi:
        await lkapi.room.update_participant(
            api.UpdateParticipantRequest(
                room="stage-room",
                identity="speaker-1",
                permission=ParticipantPermission(
                    can_publish=True,
                    can_subscribe=True,
                    can_publish_data=True
                )
            )
        )
    
    with open("output.log", "a") as f:
        f.write("Permissions updated\n")
    
    print("Permissions updated")


if __name__ == "__main__":
    asyncio.run(main())