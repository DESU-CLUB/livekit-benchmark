const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 4000;

const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'secret';
const receiver = new WebhookReceiver(apiKey, apiSecret);

const logFile = path.join(__dirname, 'events.log');

function logEvent(event) {
  const logEntry = `${new Date().toISOString()} - ${event.event} - ${JSON.stringify(event)}\n`;
  fs.appendFileSync(logFile, logEntry);
}

const handlers = {
  room_started: (event) => {
    console.log(`Room started: ${event.room?.name}`);
    logEvent(event);
  },
  room_finished: (event) => {
    console.log(`Room finished: ${event.room?.name}`);
    logEvent(event);
  },
  participant_joined: (event) => {
    console.log(`Participant joined: ${event.participant?.identity} in room ${event.room?.name}`);
    logEvent(event);
  },
  participant_left: (event) => {
    console.log(`Participant left: ${event.participant?.identity} in room ${event.room?.name}`);
    logEvent(event);
  },
  track_published: (event) => {
    console.log(`Track published: ${event.track?.sid} by ${event.participant?.identity}`);
    logEvent(event);
  },
  track_unpublished: (event) => {
    console.log(`Track unpublished: ${event.track?.sid} by ${event.participant?.identity}`);
    logEvent(event);
  },
  default: (event) => {
    console.log(`Unhandled event type: ${event.event}`);
    logEvent(event);
  }
};

app.post('/webhook', express.raw({ type: 'application/webhook+json' }), async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).send('Missing Authorization header');
  }

  try {
    const event = await receiver.receive(req.body.toString('utf8'), authHeader);
    
    const handler = handlers[event.event] || handlers.default;
    handler(event);

    res.status(200).send('OK');
  } catch (error) {
    console.error('Error validating webhook:', error.message);
    res.status(401).send('Invalid signature');
  }
});

app.listen(port, () => {
  console.log(`LiveKit webhook server listening at http://localhost:${port}`);
});