const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 4000;
const logFile = path.join(__dirname, 'events.log');

// LIVEKIT_API_KEY and LIVEKIT_API_SECRET should be set in environment variables
const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'secret';

const receiver = new WebhookReceiver(apiKey, apiSecret);

function logEvent(event) {
  const timestamp = new Date().toISOString();
  const logEntry = `${timestamp} - ${event.event}: ${JSON.stringify(event)}\n`;
  fs.appendFileSync(logFile, logEntry);
  console.log(`Logged event: ${event.event}`);
}

// Handler functions for different event types
const handlers = {
  'room_started': (event) => {
    console.log('Room started:', event.room.name);
  },
  'room_finished': (event) => {
    console.log('Room finished:', event.room.name);
  },
  'participant_joined': (event) => {
    console.log('Participant joined:', event.participant.identity, 'in room', event.room.name);
  },
  'participant_left': (event) => {
    console.log('Participant left:', event.participant.identity, 'in room', event.room.name);
  },
  'track_published': (event) => {
    console.log('Track published:', event.track.sid, 'by', event.participant.identity);
  },
  'track_unpublished': (event) => {
    console.log('Track unpublished:', event.track.sid, 'by', event.participant.identity);
  },
  'egress_started': (event) => {
    console.log('Egress started:', event.egressInfo.egressId);
  },
  'egress_updated': (event) => {
    console.log('Egress updated:', event.egressInfo.egressId, 'status:', event.egressInfo.status);
  },
  'egress_ended': (event) => {
    console.log('Egress ended:', event.egressInfo.egressId);
  },
  'ingress_started': (event) => {
    console.log('Ingress started:', event.ingressInfo.ingressId);
  },
  'ingress_ended': (event) => {
    console.log('Ingress ended:', event.ingressInfo.ingressId);
  }
};

// Webhook route
// Use express.raw to get the raw body for signature verification
app.post('/webhook', express.raw({ type: 'application/webhook+json' }), async (req, res) => {
  try {
    const sig = req.headers['authorization'];
    if (!sig) {
      console.error('Missing authorization header');
      return res.status(400).send('Missing authorization header');
    }

    // receiver.receive returns the decoded WebhookEvent
    // It throws an error if the signature is invalid
    const event = await receiver.receive(req.body, sig);
    
    // Log the event
    logEvent(event);

    // Route to handler
    const handler = handlers[event.event];
    if (handler) {
      handler(event);
    } else {
      console.log('No handler for event type:', event.event);
    }

    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook error:', error.message);
    res.status(400).send(`Webhook Error: ${error.message}`);
  }
});

// Health check route
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

app.listen(port, () => {
  console.log(`LiveKit webhook server listening at http://localhost:${port}`);
  console.log(`Webhook endpoint: http://localhost:${port}/webhook`);
});
