FROM ubuntu:24.04

LABEL Author="DESU-CLUB"
LABEL Description="LiveKit remove_participant task environment"

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

RUN pip3 install --break-system-packages livekit-api

RUN mkdir -p /home/user/livekit-admin

RUN printf 'LIVEKIT_URL=${LIVEKIT_URL}\nLIVEKIT_API_KEY=${LIVEKIT_API_KEY}\nLIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}\n' \
    > /home/user/livekit-admin/.env.local

WORKDIR /home/user/livekit-admin

CMD ["sleep", "infinity"]
