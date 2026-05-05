## Background
LiveKit access tokens encode participant permissions as part of the JWT payload. A common use case is issuing a subscribe-only token to viewers or listeners who should receive audio/video from a room but must not be allowed to publish their own tracks. The `livekit-server-sdk` Python package exposes the `can_publish` and `can_subscribe` fields inside `api.VideoGrants`.

## Requirements
Write a Python script that generates a subscribe-only LiveKit JWT token for a specific participant and room, then saves it to a file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-token`.
2. Source `.env.local` to load `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` into your environment.
3. Create `subscribe_only.py` that:
   - Reads `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from environment variables.
   - Uses `livekit.api.AccessToken` with identity `viewer-1`.
   - Calls `.with_grants(api.VideoGrants(room_join=True, room="broadcast-room", can_publish=False, can_subscribe=True))`.
   - Calls `.to_jwt()` to generate the JWT string.
   - Writes the JWT string to `token.txt` in the project directory.
   - Prints `"Subscribe-only token generated"` to stdout.
4. Run the script: `python3 subscribe_only.py`

## Constraints
- Project path: `/home/user/livekit-token`
- Log file: `/home/user/livekit-token/token.txt`
- The script must be named `subscribe_only.py`
- Participant identity must be `viewer-1`
- Room name must be `broadcast-room`
- Publishing must be disabled (`can_publish=False`)
- Subscribing must be enabled (`can_subscribe=True`)
- Use only the `livekit-server-sdk` package (already installed)

## Integrations
- **LiveKit Python Server SDK**: Token generation via `livekit.api.AccessToken`
