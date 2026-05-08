FROM ubuntu:24.04

LABEL Author="DESU-CLUB"
LABEL Description="LiveKit camera-only token restriction task environment"

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

# Install LiveKit Python server SDK
RUN pip3 install livekit-api --break-system-packages

# Create project directory with pre-existing .env.local
RUN mkdir -p /home/user/livekit-token

RUN printf 'LIVEKIT_API_KEY=test-key\nLIVEKIT_API_SECRET=test-secret\n' \
    > /home/user/livekit-token/.env.local

WORKDIR /home/user

CMD sleep infinity
