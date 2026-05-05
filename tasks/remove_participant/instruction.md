## Background
LiveKit's Python server SDK provides an async API client `api.LiveKitAPI()` that exposes room management operations. The `room.remove_participant()` method can forcibly disconnect a specific participant from a room by their identity string.

## Requirements
Write a Python script that uses the LiveKit Python server SDK to remove a participant from a room and log the result.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-admin`.
2. Source the `.env.local` file to load `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET`.
3. Create a Python script named `remove_participant.py` that:
   - Imports `asyncio` and `livekit.api` (as `api`).
   - Reads credentials from environment variables.
   - Uses `async with api.LiveKitAPI() as lkapi:` to create an API client.
   - Calls `await lkapi.room.remove_participant(api.RoomParticipantIdentity(room='demo-room', identity='user-123'))`.
   - Handles exceptions gracefully (e.g., participant or room not found).
   - Writes a result message to `/home/user/livekit-admin/output.log`.
4. Run the script: `python3 remove_participant.py`

## Constraints
- Project path: `/home/user/livekit-admin`
- Log file: `/home/user/livekit-admin/output.log`
- Script name: `remove_participant.py`
- Target room: `demo-room`
- Target identity: `user-123`
- `livekit-server-sdk` pip package is already installed
- The script must not crash if the participant or room does not exist

## Integrations
- **LiveKit Python Server SDK**: `api.LiveKitAPI().room.remove_participant()`
