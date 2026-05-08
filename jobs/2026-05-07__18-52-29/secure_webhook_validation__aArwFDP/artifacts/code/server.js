const express = require('express');
const fs = require('fs');
const path = require('path');
const { WebhookReceiver } = require('livekit-server-sdk');

const PORT = 4000;
const LOG_PATH = path.resolve(__dirname, 'events.log');

const webhookApiKey =
  process.env.LIVEKIT_WEBHOOK_API_KEY || process.env.LIVEKIT_API_KEY || '';
const webhookApiSecret =
  process.env.LIVEKIT_WEBHOOK_API_SECRET || process.env.LIVEKIT_API_SECRET || '';

if (!webhookApiKey || !webhookApiSecret) {
  console.warn(
    'LIVEKIT_WEBHOOK_API_KEY/SECRET not set. Webhook verification will fail until these are provided.'
  );
}

const receiver = new WebhookReceiver(webhookApiKey, webhookApiSecret);
const app = express();

const appendLog = async (entry) => {
  const line = `${JSON.stringify(entry)}\n`;
  try {
    await fs.promises.appendFile(LOG_PATH, line, 'utf8');
  } catch (error) {
    console.error('Failed to write webhook log entry:', error);
  }
};

const logEvent = async (eventType, payload) => {
  await appendLog({
    timestamp: new Date().toISOString(),
    type: eventType,
    payload,
  });
};

const handleRoomStarted = async (event) => logEvent(event.event, event);
const handleRoomFinished = async (event) => logEvent(event.event, event);
const handleRoomMetadataUpdated = async (event) => logEvent(event.event, event);
const handleParticipantJoined = async (event) => logEvent(event.event, event);
const handleParticipantLeft = async (event) => logEvent(event.event, event);
const handleParticipantConnected = async (event) => logEvent(event.event, event);
const handleParticipantDisconnected = async (event) => logEvent(event.event, event);
const handleParticipantMetadataUpdated = async (event) => logEvent(event.event, event);
const handleTrackPublished = async (event) => logEvent(event.event, event);
const handleTrackUnpublished = async (event) => logEvent(event.event, event);
const handleTrackSubscribed = async (event) => logEvent(event.event, event);
const handleTrackUnsubscribed = async (event) => logEvent(event.event, event);
const handleTrackMuted = async (event) => logEvent(event.event, event);
const handleTrackUnmuted = async (event) => logEvent(event.event, event);
const handleEgressStarted = async (event) => logEvent(event.event, event);
const handleEgressUpdated = async (event) => logEvent(event.event, event);
const handleEgressEnded = async (event) => logEvent(event.event, event);
const handleIngressStarted = async (event) => logEvent(event.event, event);
const handleIngressEnded = async (event) => logEvent(event.event, event);
const handleUnhandled = async (event) => logEvent(event.event || 'unhandled', event);

const handlers = {
  room_started: handleRoomStarted,
  room_finished: handleRoomFinished,
  room_metadata_updated: handleRoomMetadataUpdated,
  participant_joined: handleParticipantJoined,
  participant_left: handleParticipantLeft,
  participant_connected: handleParticipantConnected,
  participant_disconnected: handleParticipantDisconnected,
  participant_metadata_updated: handleParticipantMetadataUpdated,
  track_published: handleTrackPublished,
  track_unpublished: handleTrackUnpublished,
  track_subscribed: handleTrackSubscribed,
  track_unsubscribed: handleTrackUnsubscribed,
  track_muted: handleTrackMuted,
  track_unmuted: handleTrackUnmuted,
  egress_started: handleEgressStarted,
  egress_updated: handleEgressUpdated,
  egress_ended: handleEgressEnded,
  ingress_started: handleIngressStarted,
  ingress_ended: handleIngressEnded,
};

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.post(
  '/webhook',
  express.raw({ type: 'application/webhook+json' }),
  async (req, res) => {
    const authHeader = req.headers.authorization;
    const rawBody = req.body instanceof Buffer ? req.body.toString('utf8') : '';

    try {
      const event = await receiver.receive(rawBody, authHeader);
      const handler = handlers[event.event] || handleUnhandled;
      await handler(event);
      res.status(200).json({ received: true });
    } catch (error) {
      await appendLog({
        timestamp: new Date().toISOString(),
        type: 'webhook_error',
        message: error instanceof Error ? error.message : String(error),
      });
      res.status(401).json({ received: false });
    }
  }
);

app.listen(PORT, () => {
  console.log(`LiveKit webhook server listening on port ${PORT}`);
});
