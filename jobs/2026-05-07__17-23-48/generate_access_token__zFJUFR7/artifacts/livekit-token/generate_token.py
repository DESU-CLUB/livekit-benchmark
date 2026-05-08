import os
from livekit import api

# Read API credentials from environment variables
api_key = os.environ.get('LIVEKIT_API_KEY')
api_secret = os.environ.get('LIVEKIT_API_SECRET')

if not api_key or not api_secret:
    raise ValueError('LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set in environment variables')

# Create access token with identity test-user
token = api.AccessToken(api_key, api_secret)
token = token.with_identity('test-user')

# Add video grants with specified permissions
token = token.with_grants(
    api.VideoGrants(
        room_join=True,
        room='test-room',
        can_publish=True,
        can_subscribe=True
    )
)

# Generate JWT string
jwt_token = token.to_jwt()

# Write token to file
with open('token.txt', 'w') as f:
    f.write(jwt_token)

print('Token successfully generated and saved to token.txt')