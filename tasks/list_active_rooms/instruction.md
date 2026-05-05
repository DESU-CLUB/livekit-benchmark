# LiveKit List Active Rooms (CLI)

## Background
LiveKit provides a CLI tool (`lk`) that allows developers to interact with a LiveKit server from the command line. One common administrative task is listing all active rooms on the server. The output can be captured and saved as JSON for further processing or monitoring.

## Requirements
Use the LiveKit CLI to list all active rooms on the LiveKit server and save the output to a JSON file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-rooms`.
2. Source the `.env.local` file to load `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` into your environment.
3. Run the following CLI command and redirect its output to `rooms.json`:
   ```
   lk room list --api-key $LIVEKIT_API_KEY --api-secret $LIVEKIT_API_SECRET --url $LIVEKIT_URL --json > rooms.json
   ```
4. Verify that `rooms.json` was created and contains valid JSON.

## Constraints
- Project path: `/home/user/livekit-rooms`
- Output file: `/home/user/livekit-rooms/rooms.json`
- Must use the `lk` CLI tool (already installed at `/usr/local/bin/lk`)
- Use the env vars from `.env.local`

## Integrations
- **LiveKit CLI** (`lk`): Room listing via `lk room list --json`
