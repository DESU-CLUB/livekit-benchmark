## Background

LiveKit supports embedding a `RoomConfiguration` inside an access token so that when a participant joins and creates a room, an agent is automatically dispatched to that room. This is useful for building AI-powered rooms where an agent is always present.

## Requirements

Create a Node.js script that generates an access token with a `RoomConfiguration` that instructs LiveKit to dispatch `my-agent` when the room is created. The generated JWT must be written to a log file.

## Implementation Guide

1. Navigate to `/home/user/livekit-admin`.
2. Create `dispatch_token.mjs` that:
   - Reads `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` from environment variables (fall back to `"devkey"` and `"devsecret"` for local testing)
   - Imports `AccessToken` from `livekit-server-sdk`
   - Imports `RoomConfiguration` and `RoomAgentDispatch` from `@livekit/protocol`
   - Creates an `AccessToken` with `identity: 'host-user'`
   - Calls `at.addGrant({ roomJoin: true, room: 'ai-room', canPublish: true, canSubscribe: true })`
   - Sets `at.roomConfig = new RoomConfiguration({ agents: [new RoomAgentDispatch({ agentName: "my-agent", metadata: JSON.stringify({ source: "web" }) })] })`
   - Awaits `at.toJwt()` to generate the token
   - Writes the JWT string to `token.txt`
   - Logs `"Token written to token.txt"` to stdout
3. Run the script with `node dispatch_token.mjs` to produce `token.txt`.

## Constraints

- Project path: `/home/user/livekit-admin`
- Log file: `/home/user/livekit-admin/token.txt`

## Integrations

- LiveKit Server SDK (Node.js)
- @livekit/protocol
