import os
from livekit.api import AccessToken, VideoGrants

# Parse .env.local manually
env_file = ".env.local"
if os.path.exists(env_file):
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

api_key = os.getenv("LIVEKIT_API_KEY")
api_secret = os.getenv("LIVEKIT_API_SECRET")

grant = VideoGrants(
    room_join=True,
    room="broadcast",
    can_publish=True,
    can_subscribe=True,
    can_publish_sources=["camera"]
)

token = AccessToken(api_key, api_secret)
token.with_identity("video-only-user")
token.with_grants(grant)

jwt = token.to_jwt()

with open("token.txt", "w") as f:
    f.write(jwt)

print("Token written to token.txt")
