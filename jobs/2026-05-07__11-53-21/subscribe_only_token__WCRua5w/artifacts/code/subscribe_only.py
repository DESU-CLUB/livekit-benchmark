import os
from livekit import api

def main():
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    token = api.AccessToken(api_key, api_secret)
    token.with_identity("viewer-1")
    token.with_grants(api.VideoGrants(
        room_join=True,
        room="broadcast-room",
        can_publish=False,
        can_subscribe=True
    ))
    
    jwt = token.to_jwt()

    with open("token.txt", "w") as f:
        f.write(jwt)

    print("Subscribe-only token generated")

if __name__ == "__main__":
    main()
