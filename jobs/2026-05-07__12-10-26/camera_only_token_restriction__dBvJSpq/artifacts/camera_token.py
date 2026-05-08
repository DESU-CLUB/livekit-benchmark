import os

# Load .env.local manually
env_path = os.path.join(os.path.dirname(__file__), ".env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

from livekit.api import AccessToken, VideoGrants

api_key = os.environ["LIVEKIT_API_KEY"]
api_secret = os.environ["LIVEKIT_API_SECRET"]

token = (
    AccessToken(api_key, api_secret)
    .with_identity("video-only-user")
    .with_grants(
        VideoGrants(
            room_join=True,
            room="broadcast",
            can_publish=True,
            can_subscribe=True,
            can_publish_sources=["camera"],
        )
    )
)

jwt = token.to_jwt()

output_path = os.path.join(os.path.dirname(__file__), "token.txt")
with open(output_path, "w") as f:
    f.write(jwt)

print("Token written to token.txt")
