FROM ubuntu:24.04

LABEL Author="DESU-CLUB"
LABEL Description="LiveKit RoomServiceClient list rooms and kick participant task environment"

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

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create project directory and install required packages
RUN mkdir -p /home/user/livekit-admin

WORKDIR /home/user/livekit-admin

RUN npm init -y && \
    npm install livekit-server-sdk

WORKDIR /home/user

CMD sleep infinity
