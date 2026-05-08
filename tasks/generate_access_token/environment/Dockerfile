FROM ubuntu:24.04

LABEL Author="DESU-CLUB"
LABEL Description="LiveKit generate_access_token task environment"

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

RUN mkdir -p /home/user/livekit-token

RUN printf 'LIVEKIT_API_KEY=test-api-key\nLIVEKIT_API_SECRET=test-api-secret\n' \
    > /home/user/livekit-token/.env.local

WORKDIR /home/user/livekit-token

CMD ["sleep", "infinity"]
