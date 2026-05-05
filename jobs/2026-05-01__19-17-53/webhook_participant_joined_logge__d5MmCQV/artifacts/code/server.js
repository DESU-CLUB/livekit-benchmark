const express = require('express');
const Database = require('better-sqlite3');
const { WebhookReceiver } = require('livekit-server-sdk');

const app = express();
const port = 4000;

// Opens/creates a SQLite database at events.db
const db = new Database('events.db');

// Creates the participant_events table if it does not exist
db.prepare(`
  CREATE TABLE IF NOT EXISTS participant_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    room TEXT,
    identity TEXT,
    created_at TEXT
  )
`).run();

// Initializes WebhookReceiver with LIVEKIT_API_KEY and LIVEKIT_API_SECRET from environment (fall back to "devkey" / "devsecret")
const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret';
const receiver = new WebhookReceiver(apiKey, apiSecret);

// Registers express.raw({ type: 'application/webhook+json' }) as middleware on the POST /webhook route
app.post('/webhook', express.raw({ type: 'application/webhook+json' }), async (req, res) => {
  try {
    // calls receiver.receive(req.body, req.get('Authorization')) to validate
    // req.body is a Buffer when using express.raw
    const event = await receiver.receive(req.body, req.get('Authorization'));
    
    // checks event.event === 'participant_joined'
    if (event.event === 'participant_joined') {
      const insert = db.prepare('INSERT INTO participant_events (event, room, identity, created_at) VALUES (?, ?, ?, ?)');
      insert.run(
        event.event,
        event.room?.name || '',
        event.participant?.identity || '',
        new Date().toISOString()
      );
    }
    
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook validation failed:', error);
    res.status(401).send('Unauthorized');
  }
});

// GET /events: queries all rows from participant_events and returns them as a JSON array
app.get('/events', (req, res) => {
  const rows = db.prepare('SELECT * FROM participant_events').all();
  res.json(rows);
});

// Starts the server listening on port 4000
app.listen(port, () => {
  // Logs "LiveKit webhook server running on port 4000" on startup
  console.log(`LiveKit webhook server running on port ${port}`);
});
