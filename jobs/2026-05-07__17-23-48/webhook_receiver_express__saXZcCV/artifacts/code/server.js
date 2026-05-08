const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

// Read API credentials from environment variables
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
  console.error('Error: LIVEKIT_API_KEY and LIVEKIT_API_SECRET environment variables must be set');
  process.exit(1);
}

// Create Express app
const app = express();
const PORT = 4000;

// Apply raw middleware BEFORE the route (required for webhook signature validation)
app.use(express.raw({ type: 'application/webhook+json' }));

// Create WebhookReceiver instance
const receiver = new WebhookReceiver(LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

// POST /webhook endpoint
app.post('/webhook', async (req, res) => {
  try {
    // Get the Authorization header
    const authHeader = req.get('Authorization');
    
    if (!authHeader) {
      console.error('Missing Authorization header');
      return res.status(401).send('Unauthorized');
    }

    // Validate webhook signature using raw body
    const event = await receiver.receive(req.body, authHeader);

    // Validation successful - log event name to events.log
    const eventName = event.event;
    const logFilePath = path.join(__dirname, 'events.log');
    
    // Append event name to log file (one event per line)
    fs.appendFileSync(logFilePath, eventName + '\n', 'utf8');
    
    console.log(`Webhook received and validated: ${eventName}`);
    res.status(200).send('OK');
    
  } catch (error) {
    console.error('Webhook validation failed:', error.message);
    res.status(401).send('Unauthorized');
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`LiveKit webhook receiver listening on port ${PORT}`);
  console.log(`Webhook endpoint: http://localhost:${PORT}/webhook`);
});