## Background
LiveKit supports dynamic participant permissions that can be changed at runtime using the `RoomServiceClient`. A common use case is a "hand raise" feature in video conferencing: participants start with `canPublish: false` (view-only), and when they raise their hand, the host grants them publish permission. The `updateParticipant` method accepts a `ParticipantPermission` object to toggle track publishing rights.

## Requirements
Build a Node.js/Express HTTP server that implements a hand-raise feature with in-memory state tracking and dynamic permission updates via the LiveKit Room Service API.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-permissions`.
2. Create a file named `server.js` that:
   - Imports `express` from `express`.
   - Imports `RoomServiceClient` from `livekit-server-sdk`.
   - Reads `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` from `process.env`.
   - Creates a `RoomServiceClient` instance: `new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)`.
   - Declares an in-memory `Map` named `handRaiseState` to track which participant identities have `canPublish: true`.
   - Uses `express.json()` middleware.
   - Implements `POST /hand-raise`:
     - Accepts JSON body `{ "room": "<room-name>", "identity": "<participant-identity>" }`.
     - Returns HTTP 400 if `room` or `identity` is missing.
     - Reads current state from `handRaiseState`. If not in map, default is `false`.
     - Toggles the state: new `canPublish` = `!currentState`.
     - Calls `roomService.updateParticipant(room, identity, undefined, { canPublish: newCanPublish, canSubscribe: true })`.
     - Updates `handRaiseState` with the new value.
     - Returns JSON `{ "identity": "<identity>", "canPublish": <boolean> }`.
   - Implements `GET /hands-up`:
     - Iterates over `handRaiseState` and returns a JSON array of identities where `canPublish` is `true`.
   - Listens on port `3000`.
3. Start the server: `node server.js`

## Constraints
- Project path: `/home/user/livekit-permissions`
- Port: `3000`
- Start command: `node server.js`
- `express` and `livekit-server-sdk` npm packages are already installed
- Use an in-memory `Map` to track hand raise state (no database)
- Do not hardcode credentials; read from environment variables

## Integrations
- **LiveKit Node.js Server SDK**: `RoomServiceClient.updateParticipant` for dynamic permission updates
- **Express**: HTTP framework
