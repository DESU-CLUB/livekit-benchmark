import os
from livekit import api

def main():
    api_key = os.environ.get("LIVEKIT_API_KEY")
    api_secret = os.environ.get("LIVEKIT_API_SECRET")

    token = api.AccessToken(api_key, api_secret) \
        .with_identity("test-user") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room="test-room",
            can_publish=True,
            can_subscribe=True
        ))

    jwt = token.to_jwt()

    with open("token.txt", "w") as f:
        f.write(jwt)

if __name__ == "__main__":
    main()
