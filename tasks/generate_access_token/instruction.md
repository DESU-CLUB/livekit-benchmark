# LiveKit Generate Access Token (Python Server SDK)

## Background
LiveKit uses JWT access tokens to authenticate participants joining rooms. These tokens encode the participant's identity, the room they are joining, and the permissions they have (e.g., publish video/audio, subscribe to others). The `livekit-server-sdk` Python package provides the `api.AccessToken` class to generate these tokens server-side.

## Requirements
Write a Python script that generates a LiveKit JWT access token for a participant and saves it to a file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-token`.
2. Source the `.env.local` file to load `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` into your environment.
3. Create a Python script named `generate_token.py` that:
   - Reads `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from environment variables.
   - Uses `livekit.api.AccessToken` to create a token with identity `test-user`.
   - Calls `.with_grants(api.VideoGrants(room_join=True, room="test-room", can_publish=True, can_subscribe=True))`.
   - Calls `.to_jwt()` to generate the JWT string.
   - Writes the JWT string to `token.txt` in the project directory.
4. Run the script: `python3 generate_token.py`

## Constraints
- Project path: `/home/user/livekit-token`
- Output file: `/home/user/livekit-token/token.txt`
- The script must be named `generate_token.py`
- Use only the `livekit-server-sdk` package (already installed)

## Integrations
- **LiveKit Python Server SDK**: Token generation via `livekit.api.AccessToken`
