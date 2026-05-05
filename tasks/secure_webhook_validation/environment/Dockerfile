FROM ubuntu:24.04

LABEL Author="DESU-CLUB"
LABEL Description="LiveKit secure_webhook_validation task environment"

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

RUN mkdir -p /home/user/livekit-webhook

WORKDIR /home/user/livekit-webhook

RUN echo '{"name":"livekit-webhook","version":"1.0.0","type":"commonjs"}' > package.json \
    && npm install express livekit-server-sdk

CMD ["sleep", "infinity"]
