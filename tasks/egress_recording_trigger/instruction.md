## Background
LiveKit's Egress API allows you to record rooms to a file. The `EgressClient` from `livekit-server-sdk` provides methods to start, list, and stop egress recordings programmatically. Room composite egress captures the entire room's audio and video into a single output file. This is commonly triggered by external events such as a webhook or an admin API call.

## Requirements
Build a Node.js/Express HTTP server that exposes endpoints to start, query, and stop room composite egress recordings using the LiveKit Egress API.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-egress-server`.
2. Create a file named `server.js` that:
   - Imports `express` from `express`.
   - Imports `EgressClient`, `EncodedFileOutput`, `EncodedFileType` from `livekit-server-sdk`.
   - Reads `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` from `process.env`.
   - Creates an `EgressClient` instance: `new EgressClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)`.
   - Uses `express.json()` middleware.
   - Implements `POST /start-recording`:
     - Accepts JSON body `{ "room": "<room-name>", "filepath": "<output-path>" }`.
     - Returns HTTP 400 if `room` or `filepath` is missing.
     - Calls `egressClient.startRoomCompositeEgress(room, { file: new EncodedFileOutput({ fileType: EncodedFileType.MP4, filepath }) })`.
     - Returns JSON `{ "egressId": "<id>" }` with HTTP 200.
   - Implements `GET /egress/:egressId`:
     - Calls `egressClient.listEgress({ egressId: req.params.egressId })`.
     - Returns the first item from the result array as JSON, or HTTP 404 if not found.
   - Implements `POST /stop-recording/:egressId`:
     - Calls `egressClient.stopEgress(req.params.egressId)`.
     - Returns JSON `{ "stopped": true }`.
   - Listens on port `5000`.
3. Start the server: `node server.js`

## Constraints
- Project path: `/home/user/livekit-egress-server`
- Port: `5000`
- Start command: `node server.js`
- `express` and `livekit-server-sdk` npm packages are already installed
- Do not hardcode credentials; read from environment variables
- The `EgressClient` must be instantiated with `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`

## Integrations
- **LiveKit Node.js Server SDK**: `EgressClient`, `EncodedFileOutput`, `EncodedFileType` from `livekit-server-sdk`
- **Express**: HTTP framework
