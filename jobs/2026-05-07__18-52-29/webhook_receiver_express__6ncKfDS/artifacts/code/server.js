const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');

const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

if (!apiKey || !apiSecret) {
  console.error('Missing LIVEKIT_API_KEY or LIVEKIT_API_SECRET environment variables');
  process.exit(1);
}

const receiver = new WebhookReceiver(apiKey, apiSecret);
const app = express();
const port = 4000;

app.use(express.raw({ type: 'application/webhook+json' }));

app.post('/webhook', (req, res) => {
  const authHeader = req.get('Authorization');

  try {
    const event = receiver.receive(req.body, authHeader);
    fs.appendFileSync('/home/user/livekit-webhook/events.log', `${event.event}\n`);
    res.status(200).send('OK');
  } catch (error) {
    res.status(401).send('Unauthorized');
  }
});

app.listen(port, () => {
  console.log(`LiveKit webhook receiver listening on port ${port}`);
});
