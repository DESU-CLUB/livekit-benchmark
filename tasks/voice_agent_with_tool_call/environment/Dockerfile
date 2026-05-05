FROM ubuntu:24.04

LABEL Author="DESU-CLUB"
LABEL Description="LiveKit voice agent with function tool call task environment"

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

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"

# Create project directory (empty, as pre-task state)
RUN mkdir -p /home/user/livekit-agent

WORKDIR /home/user

CMD sleep infinity
