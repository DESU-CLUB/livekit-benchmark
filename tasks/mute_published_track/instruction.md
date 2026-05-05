## Background
LiveKit's server API allows operators to mute or unmute any participant's published track without requiring client-side cooperation. This is commonly used in moderated broadcasts, webinars, or classrooms where a host needs to silence a disruptive participant. The `RoomServiceClient.mutePublishedTrack` method accepts a room name, participant identity, track SID, and a boolean muted flag.

## Requirements
Write a Node.js script that accepts room name, participant identity, and track SID as CLI arguments and uses `RoomServiceClient` to mute the specified track.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-admin`.
2. Create `mute_track.mjs` that:
   - Imports `RoomServiceClient` from `livekit-server-sdk`.
   - Reads `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` from environment variables.
   - Parses CLI arguments from `process.argv`: `room` = argv[2], `identity` = argv[3], `trackSid` = argv[4].
   - Validates that all three arguments are provided; if not, prints a usage message to stderr and exits with code 1.
   - Creates a `RoomServiceClient` instance.
   - Calls `await svc.mutePublishedTrack(room, identity, trackSid, true)` to mute the track.
   - Appends `"Track muted: <trackSid>\n"` to `output.log` in the project directory (where `<trackSid>` is the actual track SID argument).
   - Also prints `"Track muted: <trackSid>"` to stdout.
   - Handles errors gracefully by logging them to stderr and exiting with code 1.
3. Run the script with test arguments: `node mute_track.mjs test-room test-user TR_abc123`

## Constraints
- Project path: `/home/user/livekit-admin`
- Log file: `/home/user/livekit-admin/output.log`
- The script must be named `mute_track.mjs`
- CLI argument order: `node mute_track.mjs <room> <identity> <trackSid>`
- Use `livekit-server-sdk` (already installed)
- Must use `process.argv` to read parameters

## Integrations
- **LiveKit Node.js Server SDK**: `RoomServiceClient.mutePublishedTrack`
