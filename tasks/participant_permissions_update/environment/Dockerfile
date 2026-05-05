FROM ubuntu:24.04

LABEL Author="DESU-CLUB"
LABEL Description="LiveKit participant_permissions_update task environment"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    python3-pytest \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages livekit-server-sdk

RUN mkdir -p /home/user/livekit-admin

RUN printf 'LIVEKIT_API_KEY=test-key\nLIVEKIT_API_SECRET=test-secret\nLIVEKIT_URL=wss://test.livekit.cloud\n' \
    > /home/user/livekit-admin/.env.local

WORKDIR /home/user/livekit-admin

CMD ["sleep", "infinity"]
