import os

from livekit import api


def main() -> None:
    api_key = os.environ.get("LIVEKIT_API_KEY")
    api_secret = os.environ.get("LIVEKIT_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError("LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set")

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

    with open("token.txt", "w", encoding="utf-8") as output_file:
        output_file.write(token)


if __name__ == "__main__":
    main()
