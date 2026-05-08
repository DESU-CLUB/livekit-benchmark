const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

const receiver = new WebhookReceiver(apiKey, apiSecret);

const app = express();

app.use(express.raw({ type: 'application/webhook+json' }));

app.post('/webhook', async (req, res) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
      return res.status(401).send('Missing Authorization header');
    }

    const event = await receiver.receive(req.body, authHeader);
    
    fs.appendFileSync('/home/user/livekit-webhook/events.log', event.event + '\n');
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook validation failed:', error);
    res.status(401).send('Unauthorized');
  }
});

const PORT = 4000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
