import asyncio

from livekit import api
from livekit.protocol.models import ParticipantPermission


async def main() -> None:
    async with api.LiveKitAPI() as lkapi:
        await lkapi.room.update_participant(
            api.UpdateParticipantRequest(
                room="stage-room",
                identity="speaker-1",
                permission=ParticipantPermission(
                    can_publish=True,
                    can_subscribe=True,
                    can_publish_data=True,
                ),
            )
        )

    with open("output.log", "a", encoding="utf-8") as output_log:
        output_log.write("Permissions updated\n")

    print("Permissions updated")


if __name__ == "__main__":
    asyncio.run(main())
