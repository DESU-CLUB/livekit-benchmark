const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

const receiver = new WebhookReceiver(LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

const app = express();

const LOG_FILE = path.join(__dirname, 'events.log');

app.use(express.raw({ type: 'application/webhook+json' }));

app.post('/webhook', async (req, res) => {
  const authHeader = req.headers['authorization'];

  try {
    const event = await receiver.receive(req.body, authHeader);
    fs.appendFileSync(LOG_FILE, event.event + '\n');
    res.sendStatus(200);
  } catch (err) {
    res.sendStatus(401);
  }
});

app.listen(4000, () => {
  console.log('LiveKit webhook server listening on port 4000');
});
