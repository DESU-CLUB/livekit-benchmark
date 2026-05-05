## Background
LiveKit rooms support arbitrary metadata stored as a string on the room object. This metadata is visible to all participants in the room and can be updated at any time via the server-side `RoomServiceClient`. A common pattern is to store JSON-encoded state (e.g., session status, timestamps) so that connected clients can react to room-level changes without custom signaling.

## Requirements
Write a Node.js script that uses `RoomServiceClient` to update the metadata of a LiveKit room, then log the result to a file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-admin`.
2. Create `update_metadata.mjs` that:
   - Imports `RoomServiceClient` from `livekit-server-sdk`.
   - Reads `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` from environment variables.
   - Creates a `RoomServiceClient` instance using the URL, API key, and API secret.
   - Calls `svc.updateRoomMetadata('conference-room', JSON.stringify({ status: 'active', updated_at: new Date().toISOString() }))`.
   - After the call resolves, appends `"Metadata updated successfully"` followed by a newline to `output.log` in the project directory.
   - Handles errors by logging them to stderr and exiting with code 1.
3. Run the script: `node update_metadata.mjs`

## Constraints
- Project path: `/home/user/livekit-admin`
- Log file: `/home/user/livekit-admin/output.log`
- The script must be named `update_metadata.mjs`
- Room name must be `conference-room`
- Use `livekit-server-sdk` (already installed)
- Read credentials from environment variables; do not hardcode them

## Integrations
- **LiveKit Node.js Server SDK**: `RoomServiceClient` room management
