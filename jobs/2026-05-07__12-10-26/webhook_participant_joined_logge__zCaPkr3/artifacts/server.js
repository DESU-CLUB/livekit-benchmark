import express from 'express';
import Database from 'better-sqlite3';
import { WebhookReceiver } from 'livekit-server-sdk';

// Open / create SQLite database
const db = new Database('events.db');

// Create table if it doesn't exist
db.exec(`
  CREATE TABLE IF NOT EXISTS participant_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    room TEXT,
    identity TEXT,
    created_at TEXT
  )
`);

// Prepare statements
const insertEvent = db.prepare(
  'INSERT INTO participant_events (event, room, identity, created_at) VALUES (?, ?, ?, ?)'
);
const selectAllEvents = db.prepare('SELECT * FROM participant_events');

// Initialize WebhookReceiver with API key/secret from environment
const apiKey = process.env.LIVEKIT_API_KEY ?? 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET ?? 'devsecret';
const receiver = new WebhookReceiver(apiKey, apiSecret);

const app = express();

// POST /webhook — raw body required for signature validation
app.post(
  '/webhook',
  express.raw({ type: 'application/webhook+json' }),
  async (req, res) => {
    try {
      const event = await receiver.receive(req.body, req.get('Authorization'));

      if (event.event === 'participant_joined') {
        insertEvent.run(
          event.event,
          event.room?.name ?? null,
          event.participant?.identity ?? null,
          new Date().toISOString()
        );
      }

      res.json({ status: 'ok' });
    } catch (err) {
      console.error('Webhook validation failed:', err.message);
      res.status(400).json({ error: 'Invalid webhook' });
    }
  }
);

// GET /events — return all stored participant events
app.get('/events', (_req, res) => {
  const rows = selectAllEvents.all();
  res.json(rows);
});

// Start server
app.listen(4000, () => {
  console.log('LiveKit webhook server running on port 4000');
});
