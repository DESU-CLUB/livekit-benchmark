# LiveKit Delete Room (Node.js Server SDK)

## Background
LiveKit's `RoomServiceClient` (Node.js server SDK) provides administrative APIs for managing rooms and participants. A common operational task is deleting stale or unused rooms. The `deleteRoom` method removes a room and disconnects all participants.

## Requirements
Write a Node.js script using the LiveKit server SDK to delete a specific room, and log the result to a file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-admin`.
2. Create a file named `delete_room.js` that:
   - Imports `RoomServiceClient` from `livekit-server-sdk`.
   - Reads `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` from environment variables.
   - Creates a `RoomServiceClient` instance.
   - First creates the target room via `svc.createRoom({ name: 'old-meeting-room' })` so that there is actually something to delete. Treat an "already exists" error as success.
   - Calls `svc.deleteRoom('old-meeting-room')` inside an async function.
   - Handles errors gracefully (e.g., room not found should not crash the script).
   - Appends the message `Room deleted successfully` to `/home/user/livekit-admin/output.log`.
3. Run the script: `node delete_room.js`

## Constraints
- Project path: `/home/user/livekit-admin`
- Log file: `/home/user/livekit-admin/output.log`
- Script name: `delete_room.js`
- Room to delete: `old-meeting-room`
- The script must exit with code 0 even if the room does not exist
- `livekit-server-sdk` npm package is already installed in the project

## Integrations
- **LiveKit Node.js Server SDK**: `RoomServiceClient.deleteRoom()` method
