import asyncio
import os
import livekit.api as api

LOG_FILE = "/home/user/livekit-admin/output.log"
ROOM = "demo-room"
IDENTITY = "user-123"


async def remove_participant():
    url = os.environ.get("LIVEKIT_URL")
    api_key = os.environ.get("LIVEKIT_API_KEY")
    api_secret = os.environ.get("LIVEKIT_API_SECRET")

    if not all([url, api_key, api_secret]):
        msg = "ERROR: Missing one or more required environment variables (LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)."
        print(msg)
        with open(LOG_FILE, "w") as f:
            f.write(msg + "\n")
        return

    try:
        async with api.LiveKitAPI(
            url=url,
            api_key=api_key,
            api_secret=api_secret,
        ) as lkapi:
            await lkapi.room.remove_participant(
                api.RoomParticipantIdentity(room=ROOM, identity=IDENTITY)
            )
            msg = f"SUCCESS: Participant '{IDENTITY}' removed from room '{ROOM}'."
            print(msg)
            with open(LOG_FILE, "w") as f:
                f.write(msg + "\n")

    except Exception as e:
        err_str = str(e).lower()
        # Treat "not found" errors as a non-fatal expected condition
        # Covers TwirpError (code=not_found) and plain-text variants
        if "not_found" in err_str or "not found" in err_str or "no participant" in err_str:
            msg = (
                f"INFO: Could not remove participant '{IDENTITY}' from room '{ROOM}': "
                f"participant or room does not exist. ({e})"
            )
        else:
            msg = f"ERROR: Failed to remove participant '{IDENTITY}' from room '{ROOM}': {e}"
        print(msg)
        with open(LOG_FILE, "w") as f:
            f.write(msg + "\n")


if __name__ == "__main__":
    asyncio.run(remove_participant())
