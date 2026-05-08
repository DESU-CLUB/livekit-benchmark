import os
from livekit import api

# Read credentials from environment variables
api_key = os.environ.get("LIVEKIT_API_KEY")
api_secret = os.environ.get("LIVEKIT_API_SECRET")

if not api_key or not api_secret:
    raise ValueError("LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set in the environment")

# Create an access token with identity and video grants
token = (
    api.AccessToken(api_key, api_secret)
    .with_identity("test-user")
    .with_grants(
        api.VideoGrants(
            room_join=True,
            room="test-room",
            can_publish=True,
            can_subscribe=True,
        )
    )
    .to_jwt()
)

# Write the JWT to token.txt
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")
with open(output_path, "w") as f:
    f.write(token)

print(f"Token written to {output_path}")
print(f"Token: {token}")
