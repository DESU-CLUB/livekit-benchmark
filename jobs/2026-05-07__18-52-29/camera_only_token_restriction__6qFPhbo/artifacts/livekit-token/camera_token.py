import os
from pathlib import Path
from livekit.api import AccessToken, VideoGrants


def load_env_local(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    load_env_local(Path(".env.local"))

    api_key = os.environ.get("LIVEKIT_API_KEY")
    api_secret = os.environ.get("LIVEKIT_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError("LIVEKIT_API_KEY or LIVEKIT_API_SECRET is missing")

    token = AccessToken(api_key, api_secret).with_identity("video-only-user")
    grant = VideoGrants(
        room_join=True,
        room="broadcast",
        can_publish=True,
        can_subscribe=True,
        can_publish_sources=["camera"],
    )
    token.with_grants(grant)

    jwt = token.to_jwt()

    with open("token.txt", "w", encoding="utf-8") as token_file:
        token_file.write(jwt)

    print("Token written to token.txt")


if __name__ == "__main__":
    main()
