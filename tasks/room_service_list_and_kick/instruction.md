## Background

LiveKit's `RoomServiceClient` provides server-side APIs to manage rooms and participants. Common administrative operations include listing active rooms and forcibly removing participants who violate platform policies.

## Requirements

Write a Node.js script that uses `RoomServiceClient` to list all active rooms, log the count, remove a specific participant from a target room, and write all log output to a file.

## Implementation Guide

1. Navigate to `/home/user/livekit-admin`.
2. Create `list_and_kick.mjs` that:
   - Imports `RoomServiceClient` from `livekit-server-sdk`
   - Imports `fs` from `node:fs`
   - Reads `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` from environment (fall back to `"http://localhost:7880"`, `"devkey"`, `"devsecret"`)
   - Creates a `RoomServiceClient` instance
   - Calls `svc.listRooms()` and stores the result
   - Builds a log line: `"Active rooms: N"` where `N` is `rooms.length`
   - Calls `svc.removeParticipant('live-session', 'banned-user')` inside a `try/catch` (participant may not exist)
   - In the `catch` block, logs `"Note: participant not found or already removed"`
   - After the try/catch, appends `"Removed participant banned-user from live-session"` to the log
   - Collects all log lines into an array and writes them (newline-joined) to `output.log`
   - Also prints each log line to stdout with `console.log`
3. Run the script with `node list_and_kick.mjs` to produce `output.log`.

## Constraints

- Project path: `/home/user/livekit-admin`
- Log file: `/home/user/livekit-admin/output.log`

## Integrations

- LiveKit Server SDK (Node.js)
