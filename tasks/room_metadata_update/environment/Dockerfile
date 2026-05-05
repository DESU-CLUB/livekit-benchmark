FROM ubuntu:24.04

LABEL Author="DESU-CLUB"
LABEL Description="LiveKit room_metadata_update task environment"

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

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/livekit-admin

WORKDIR /home/user/livekit-admin

RUN echo '{"name":"livekit-admin","version":"1.0.0","type":"module"}' > package.json \
    && npm install livekit-server-sdk

CMD ["sleep", "infinity"]
