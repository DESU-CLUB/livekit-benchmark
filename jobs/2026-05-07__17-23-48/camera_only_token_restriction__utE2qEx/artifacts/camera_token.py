import os
from dotenv import load_dotenv
from livekit.api import AccessToken, VideoGrants

# Load environment variables from .env.local
load_dotenv('.env.local')

api_key = os.environ.get('LIVEKIT_API_KEY')
api_secret = os.environ.get('LIVEKIT_API_SECRET')

# Create an AccessToken with the API key and secret
token = AccessToken(api_key, api_secret)

# Set identity
token.with_identity("video-only-user")

# Add video grant with camera-only publishing permissions
token.with_grants(
    VideoGrants(
        room_join=True,
        room="broadcast",
        can_publish=True,
        can_subscribe=True,
        can_publish_sources=["camera"]
    )
)

# Generate the JWT
jwt_token = token.to_jwt()

# Write the JWT to token.txt
with open('token.txt', 'w') as f:
    f.write(jwt_token)

print("Token written to token.txt")