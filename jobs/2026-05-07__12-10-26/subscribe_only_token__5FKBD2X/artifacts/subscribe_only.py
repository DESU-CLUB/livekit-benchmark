import os
from livekit import api

LIVEKIT_API_KEY = os.environ["LIVEKIT_API_KEY"]
LIVEKIT_API_SECRET = os.environ["LIVEKIT_API_SECRET"]

token = (
    api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    .with_identity("viewer-1")
    .with_grants(
        api.VideoGrants(
            room_join=True,
            room="broadcast-room",
            can_publish=False,
            can_subscribe=True,
        )
    )
    .to_jwt()
)

with open("token.txt", "w") as f:
    f.write(token)

print("Subscribe-only token generated")
