const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');

const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

const receiver = new WebhookReceiver(apiKey, apiSecret);

const app = express();
const port = 4000;

app.use(express.raw({ type: 'application/webhook+json' }));

app.post('/webhook', async (req, res) => {
  const authHeader = req.get('Authorization');
  if (!authHeader) {
    return res.status(401).send('Unauthorized');
  }

  try {
    const event = await receiver.receive(req.body, authHeader);
    fs.appendFileSync('/home/user/livekit-webhook/events.log', event.event + '\n');
    res.status(200).send('OK');
  } catch (e) {
    res.status(401).send('Unauthorized');
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
