## Background
LiveKit's server-side API allows administrators to query the current state of any room, including all connected participants. `RoomServiceClient.listParticipants` returns an array of `ParticipantInfo` objects containing the participant's identity, SID, state, joined timestamp, and published tracks. This is useful for building dashboards, managing access, or recording attendance.

## Requirements
Write a Node.js script that retrieves all participants in a LiveKit room and saves the result as a JSON array to a file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-admin`.
2. Create `list_participants.mjs` that:
   - Imports `RoomServiceClient` from `livekit-server-sdk`.
   - Reads `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` from environment variables.
   - Creates a `RoomServiceClient` instance.
   - Calls `await svc.listParticipants('main-room')` to retrieve participants.
   - Serializes the result to a JSON array using `JSON.stringify(participants, null, 2)`.
   - Writes the JSON to `participants.json` in the project directory.
   - Handles errors gracefully by logging to stderr and exiting with code 1.
3. Run the script: `node list_participants.mjs`

## Constraints
- Project path: `/home/user/livekit-admin`
- Output file: `/home/user/livekit-admin/participants.json`
- The script must be named `list_participants.mjs`
- Room name must be `main-room`
- The result must be a JSON array (may be empty if no participants are present)
- Use `livekit-server-sdk` (already installed)

## Integrations
- **LiveKit Node.js Server SDK**: `RoomServiceClient.listParticipants`
