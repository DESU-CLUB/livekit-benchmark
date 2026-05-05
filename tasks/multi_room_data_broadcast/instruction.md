## Background
LiveKit's Room Service API allows server-side applications to send data messages to participants in any active room. A common use case is broadcasting system notifications (e.g., maintenance warnings) to all active rooms simultaneously. The `send_data` method accepts a `SendDataRequest` with the room name, binary payload, and packet kind (`DATA_PACKET_KIND_RELIABLE` for guaranteed delivery).

## Requirements
Write a Python script that lists all active LiveKit rooms and broadcasts a system message to each one using the Room Service `send_data` API.

## Implementation Guide
See `instruction.md` for full details.

## Constraints
- Project path: `/home/user/livekit-broadcast`
- Script file: `/home/user/livekit-broadcast/broadcast.py`
- Log file: `/home/user/livekit-broadcast/broadcast.log`
- `.env.local` is pre-created with `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `LIVEKIT_URL`
- `livekit-server-sdk` (Python) is already installed

## Integrations
- **LiveKit Python Server SDK**: `livekit.api` — `LiveKitAPI`, `ListRoomsRequest`, `SendDataRequest`, `DataPacketKind`
