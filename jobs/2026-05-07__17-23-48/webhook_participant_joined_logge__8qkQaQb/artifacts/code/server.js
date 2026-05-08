const express = require('express');
const Database = require('better-sqlite3');
const { WebhookReceiver } = require('livekit-server-sdk');

const app = express();

// Open/create SQLite database
const db = new Database('events.db');

// Create participant_events table if it doesn't exist
db.exec(`
  CREATE TABLE IF NOT EXISTS participant_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    room TEXT,
    identity TEXT,
    created_at TEXT
  )
`);

// Initialize WebhookReceiver with environment variables or fallback
const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret';
const receiver = new WebhookReceiver(apiKey, apiSecret);

// POST /webhook endpoint - receives and validates LiveKit webhook events
app.post('/webhook', express.raw({ type: 'application/webhook+json' }), (req, res) => {
  try {
    // Validate webhook using WebhookReceiver
    const event = receiver.receive(req.body, req.get('Authorization'));
    
    // Check if event is participant_joined
    if (event.event === 'participant_joined') {
      // Insert record into database
      const stmt = db.prepare(`
        INSERT INTO participant_events (event, room, identity, created_at)
        VALUES (?, ?, ?, ?)
      `);
      
      stmt.run(
        event.event,
        event.room.name,
        event.participant.identity,
        new Date().toISOString()
      );
    }
    
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook validation error:', error);
    res.status(400).send('Invalid webhook');
  }
});

// GET /events endpoint - query all stored events
app.get('/events', (req, res) => {
  const stmt = db.prepare('SELECT * FROM participant_events');
  const events = stmt.all();
  res.json(events);
});

// Start server on port 4000
app.listen(4000, () => {
  console.log('LiveKit webhook server running on port 4000');
});