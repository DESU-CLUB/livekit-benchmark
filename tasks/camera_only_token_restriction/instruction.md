## Background

LiveKit access tokens support granular publish permissions through `can_publish_sources`, allowing you to restrict a participant to only publishing specific track types (e.g., camera only, no microphone or screen share). This is useful for broadcast scenarios where mics are muted by default.

## Requirements

Write a Python script that generates an access token for a participant restricted to publishing only camera tracks, and write the JWT to a file.

## Implementation Guide

1. Navigate to `/home/user/livekit-token`.
2. Create `camera_token.py` that:
   - Loads `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from `.env.local` (use `python-dotenv` or manual parsing, or read via `os.environ`)
   - Imports `AccessToken` and `VideoGrants` from `livekit.api` (Python server SDK)
   - Creates an `AccessToken` with the API key and secret
   - Sets `identity` to `"video-only-user"`
   - Adds a grant with `room_join=True`, `room="broadcast"`, `can_publish=True`, `can_subscribe=True`, `can_publish_sources=["camera"]`
   - Awaits (or calls synchronously) `to_jwt()` / `AccessToken.to_jwt()` to produce the JWT string
   - Writes the JWT to `token.txt`
   - Prints `"Token written to token.txt"` to stdout
3. Run the script with `python3 camera_token.py`.

## Constraints

- Project path: `/home/user/livekit-token`
- Log file: `/home/user/livekit-token/token.txt`
- Pre-existing `.env.local` has `LIVEKIT_API_KEY=test-key` and `LIVEKIT_API_SECRET=test-secret`

## Integrations

- LiveKit Server SDK (Python)
