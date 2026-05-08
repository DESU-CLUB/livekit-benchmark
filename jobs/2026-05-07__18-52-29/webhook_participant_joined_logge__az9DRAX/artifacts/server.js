const express = require('express');
const Database = require('better-sqlite3');
const { WebhookReceiver } = require('livekit-server-sdk');

const app = express();
const db = new Database('events.db');

db.exec(`
  CREATE TABLE IF NOT EXISTS participant_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    room TEXT,
    identity TEXT,
    created_at TEXT
  )
`);

const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret';
const receiver = new WebhookReceiver(apiKey, apiSecret);

const insertEvent = db.prepare(
  'INSERT INTO participant_events (event, room, identity, created_at) VALUES (?, ?, ?, ?)'
);
const selectEvents = db.prepare('SELECT * FROM participant_events ORDER BY id');

app.post(
  '/webhook',
  express.raw({ type: 'application/webhook+json' }),
  (req, res) => {
    try {
      const authHeader = req.get('Authorization');
      const event = receiver.receive(req.body, authHeader);

      if (event.event === 'participant_joined') {
        insertEvent.run(
          event.event,
          event.room?.name || null,
          event.participant?.identity || null,
          new Date().toISOString()
        );
      }

      res.status(200).json({ received: true });
    } catch (error) {
      res.status(401).json({ error: error.message });
    }
  }
);

app.get('/events', (req, res) => {
  const events = selectEvents.all();
  res.json(events);
});

app.listen(4000, () => {
  console.log('LiveKit webhook server running on port 4000');
});
