'use strict';

const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

// ─── Configuration ────────────────────────────────────────────────────────────
const PORT = 4000;
const LOG_FILE = path.join(__dirname, 'events.log');
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'devsecret';

// ─── Logging ──────────────────────────────────────────────────────────────────
const logStream = fs.createWriteStream(LOG_FILE, { flags: 'a' });

function logEvent(eventType, data) {
  const entry = {
    timestamp: new Date().toISOString(),
    event: eventType,
    data,
  };
  const line = JSON.stringify(entry) + '\n';
  logStream.write(line);
  console.log(`[${entry.timestamp}] ${eventType}`, JSON.stringify(data, null, 2));
}

// ─── WebhookReceiver ──────────────────────────────────────────────────────────
const receiver = new WebhookReceiver(LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

// ─── Event Handlers ───────────────────────────────────────────────────────────

function handleRoomStarted(event) {
  const room = event.room;
  logEvent('room_started', {
    roomName: room?.name,
    roomSid: room?.sid,
    creationTime: room?.creationTime,
  });
}

function handleRoomFinished(event) {
  const room = event.room;
  logEvent('room_finished', {
    roomName: room?.name,
    roomSid: room?.sid,
    numParticipants: room?.numParticipants,
  });
}

function handleParticipantJoined(event) {
  const participant = event.participant;
  const room = event.room;
  logEvent('participant_joined', {
    roomName: room?.name,
    roomSid: room?.sid,
    participantIdentity: participant?.identity,
    participantSid: participant?.sid,
    participantName: participant?.name,
  });
}

function handleParticipantLeft(event) {
  const participant = event.participant;
  const room = event.room;
  logEvent('participant_left', {
    roomName: room?.name,
    roomSid: room?.sid,
    participantIdentity: participant?.identity,
    participantSid: participant?.sid,
  });
}

function handleTrackPublished(event) {
  const track = event.track;
  const participant = event.participant;
  const room = event.room;
  logEvent('track_published', {
    roomName: room?.name,
    participantIdentity: participant?.identity,
    trackSid: track?.sid,
    trackType: track?.type,
    trackSource: track?.source,
    mimeType: track?.mimeType,
  });
}

function handleTrackUnpublished(event) {
  const track = event.track;
  const participant = event.participant;
  const room = event.room;
  logEvent('track_unpublished', {
    roomName: room?.name,
    participantIdentity: participant?.identity,
    trackSid: track?.sid,
    trackType: track?.type,
  });
}

function handleEgressStarted(event) {
  const egress = event.egressInfo;
  logEvent('egress_started', {
    egressId: egress?.egressId,
    roomId: egress?.roomId,
    roomName: egress?.roomName,
    status: egress?.status,
  });
}

function handleEgressUpdated(event) {
  const egress = event.egressInfo;
  logEvent('egress_updated', {
    egressId: egress?.egressId,
    roomName: egress?.roomName,
    status: egress?.status,
  });
}

function handleEgressEnded(event) {
  const egress = event.egressInfo;
  logEvent('egress_ended', {
    egressId: egress?.egressId,
    roomName: egress?.roomName,
    status: egress?.status,
    error: egress?.error,
  });
}

function handleIngressStarted(event) {
  const ingress = event.ingressInfo;
  logEvent('ingress_started', {
    ingressId: ingress?.ingressId,
    roomName: ingress?.roomName,
    streamKey: ingress?.streamKey,
    state: ingress?.state,
  });
}

function handleIngressEnded(event) {
  const ingress = event.ingressInfo;
  logEvent('ingress_ended', {
    ingressId: ingress?.ingressId,
    roomName: ingress?.roomName,
    state: ingress?.state,
  });
}

// Map LiveKit event types to handler functions
// Values come from the WebhookEvent.event string field in the SDK
const EVENT_HANDLERS = {
  'room_started':          handleRoomStarted,
  'room_finished':         handleRoomFinished,
  'participant_joined':    handleParticipantJoined,
  'participant_left':      handleParticipantLeft,
  'track_published':       handleTrackPublished,
  'track_unpublished':     handleTrackUnpublished,
  'egress_started':        handleEgressStarted,
  'egress_updated':        handleEgressUpdated,
  'egress_ended':          handleEgressEnded,
  'ingress_started':       handleIngressStarted,
  'ingress_ended':         handleIngressEnded,
};

// ─── Express App ──────────────────────────────────────────────────────────────
const app = express();

// Webhook route — must use express.raw() to preserve the raw body for
// HMAC signature verification. express.json() must NOT be applied globally
// before this route.
app.post(
  '/webhook',
  express.raw({ type: 'application/webhook+json' }),
  async (req, res) => {
    const authHeader = req.headers['authorization'];

    // express.raw() gives us a Buffer; receiver.receive() needs a string
    const body = req.body instanceof Buffer ? req.body.toString('utf8') : req.body;

    let event;
    try {
      // Validates the Authorization header JWT signature using the API secret
      event = await receiver.receive(body, authHeader);
    } catch (err) {
      console.error('Webhook signature validation failed:', err.message);
      return res.status(401).json({ error: 'Invalid webhook signature' });
    }

    const eventType = event.event;
    const handler = EVENT_HANDLERS[eventType];

    if (handler) {
      try {
        handler(event);
      } catch (err) {
        console.error(`Error in handler for ${eventType}:`, err);
        // Still acknowledge receipt to LiveKit so it does not retry
      }
    } else {
      // Log unknown / future event types rather than silently dropping them
      logEvent('unknown_event', { eventType, event });
    }

    return res.status(200).json({ received: true });
  }
);

// Health-check endpoint
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', port: PORT });
});

// ─── Start Server ─────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`LiveKit webhook server listening on port ${PORT}`);
  console.log(`Logging events to: ${LOG_FILE}`);
  console.log(`API key: ${LIVEKIT_API_KEY}`);
});
