Evaluation Dataset Research: LiveKit

## 1. Library Overview

*   **Description**: LiveKit is an open-source framework and cloud platform for building realtime voice, video, and AI applications. It provides a high-performance WebRTC Selective Forwarding Unit (SFU) and a specialized "Agents" framework for building low-latency AI assistants.

*   **Ecosystem Role**: It acts as the realtime media infrastructure layer. It replaces traditional WebRTC stacks with a simplified API and provides pre-built integrations for STT (Speech-to-Text), LLMs, and TTS (Text-to-Speech) specifically optimized for conversational AI.

*   **Project Setup**:

    *   **CLI**: `lk agent init <name> --template agent-starter-python` (or `agent-starter-node`).

    *   **Installation**:

        *   **Python**: `uv sync` (requires Python 3.10+).

        *   **Node.js**: `pnpm install` (requires Node 20+).

    *   **Configuration**: Requires `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` in a `.env.local` file.

    *   **Models**: Run `uv run src/agent.py download-files` to download local models like Silero VAD.

## 2. Core Primitives & APIs

### Core Concepts

*   **Room**: The top-level container for a realtime session.*   **Participant**: A user or agent in a room. Can be `LocalParticipant` or `RemoteParticipant`.

*   **Track**: A stream of audio, video, or data.

*   **AgentSession**: A high-level orchestration object for AI agents that connects STT, LLM, and TTS.

### Basic Usage (Client-side JS)

```typescript

import { Room, RoomEvent } from 'livekit-client';

const room = new Room();

await room.connect('ws://localhost:7880', token);

// Publish camera and mic

await room.localParticipant.setCameraEnabled(true);

await room.localParticipant.setMicrophoneEnabled(true);

// Handle new participants

room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {

  if (track.kind === 'video') {

    // Attach to DOM

    track.attach(document.getElementById('video-element'));

  }

});

```

*   [Connecting Docs](https://docs.livekit.io/intro/basics/connect.md)

### Agent Framework (Python)

```python

from livekit import agents

from livekit.agents import AgentServer, AgentSession, inference, TurnHandlingOptions

from livekit.plugins import silero, openai, cartesia

@server.rtc_session(agent_name="my-agent")

async def my_agent(ctx: agents.JobContext):

    session = AgentSession(

        stt=inference.STT(model="deepgram/nova-3"),

        llm=inference.LLM(model="openai/gpt-4o"),

        tts=inference.TTS(model="cartesia/sonic-3"),

        vad=silero.VAD.load(),

    )

    await session.start(room=ctx.room, agent=MyAssistant())

    await session.generate_reply(instructions="Greet the user.")

```

*   [Agents Framework Docs](https://docs.livekit.io/agents.md)

## 3. Real-World Use Cases & Templates

*   **Voice AI Assistants**: Customer support bots, IVR systems, and personal assistants.

    *   Template: [Agent Starter Python](https://github.com/livekit-examples/agent-starter-python)

*   **Video Conferencing**: Zoom-like applications with gallery views and screen sharing.

    *   Template: [LiveKit Meet](https://github.com/livekit-examples/meet)

*   **Multi-modal AI**: Agents that can "see" via video tracks and respond via voice.

    *   [Vision Guide](https://docs.livekit.io/agents/multimodality/vision.md)

*   **Livestreaming**: One-to-many broadcasts with sub-second latency.

    *   Template: [Livestream Example](https://github.com/livekit-examples/livestream)

## 4. Developer Friction Points

1.  **Token Generation**: Tokens must be generated on a secure backend using the API Secret. Developers often struggle with the initial handshake and ensuring the token has the correct `video: true` or `roomJoin: true` permissions.

    *   [Token Docs](https://docs.livekit.io/frontends/authentication/tokens.md)

2.  **WebRTC Connectivity (NAT/Firewalls)**: In self-hosted environments, setting up ICE/TURN servers correctly is a major pain point. Misconfiguration leads to "Signal connected but no media" issues.

    *   [Connection Reliability Docs](https://docs.livekit.io/intro/basics/connect.md#connection-reliability)

3.  **Interruption Handling**: In voice AI, managing "barge-in" (user speaking over the agent) requires fine-tuning Voice Activity Detection (VAD) and turn-detection models.

    *   [Turn Detection Guide](https://docs.livekit.io/agents/logic/turns.md)

4.  **Webhooks Security**: Validating the `Authorization` header in webhooks requires raw body access in frameworks like Express, which often conflicts with standard JSON body parsers.

    *   [Webhooks Docs](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events.md)

## 5. Evaluation Ideas

1.  **Basic Assistant**: Implement a voice agent that uses a specific system prompt and handles a simple tool call (e.g., "What's the weather?").

2.  **Multi-modal Vision**: Create an agent that subscribes to a video track and describes the scene every 5 seconds.

3.  **Custom Webhook Handler**: Build a backend endpoint that receives `participant_joined` events and logs them to a database.

4.  **Token Server**: Create a simple Node.js/Express API that generates a LiveKit access token for a given room and identity.

5.  **Room Management**: Use the Room Service API to list all active rooms and kick a specific participant by identity.

6.  **Egress Recording**: Trigger a room recording (Egress) when a specific data message is received from a participant.

7.  **Dynamic Permissions**: Implement a "hand raise" feature where a participant's track subscription permissions are updated when they send a specific data message.

8.  **Telephony Bridge**: Set up a SIP inbound trunk that connects a phone call to a LiveKit AI agent.

## 6. Sources

1.  [LiveKit Overview](https://docs.livekit.io/intro/overview/): Official introduction to the platform.

2.  [LiveKit llms.txt](https://docs.livekit.io/llms.txt): Structured index for LLM consumption.

3.  [LiveKit llms-full.txt](https://docs.livekit.io/llms-full.txt): Full documentation text for deep context.

4.  [Connecting to LiveKit](https://docs.livekit.io/intro/basics/connect.md): Details on Room connection and SDK installation.

5.  [Voice AI Quickstart](https://docs.livekit.io/agents/start/voice-ai.md): Guide for building the first AI agent.

6.  [Media Publishing](https://docs.livekit.io/transport/media/publish.md): API details for publishing tracks from clients and backends.

7.  [Webhooks & Events](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events.md): Server-side notification and client-side event handling.

8.  [Coding Agent Support](https://docs.livekit.io/intro/coding-agents.md): Best practices for AI-assisted development with LiveKit.
