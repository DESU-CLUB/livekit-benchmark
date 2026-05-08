const express = require('express');
const Database = require('better-sqlite3');
const { WebhookReceiver } = require('livekit-server-sdk');

const app = express();
const port = 4000;

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

const insertEvent = db.prepare('INSERT INTO participant_events (event, room, identity, created_at) VALUES (?, ?, ?, ?)');
const getEvents = db.prepare('SELECT * FROM participant_events');

const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret';
const receiver = new WebhookReceiver(apiKey, apiSecret);

app.post('/webhook', express.raw({ type: 'application/webhook+json' }), async (req, res) => {
  try {
    const authHeader = req.get('Authorization');
    const event = await receiver.receive(req.body.toString('utf8'), authHeader);
    
    if (event.event === 'participant_joined') {
      const roomName = event.room ? event.room.name : null;
      const identity = event.participant ? event.participant.identity : null;
      insertEvent.run(event.event, roomName, identity, new Date().toISOString());
    }
    
    res.status(200).send('OK');
  } catch (error) {
    console.error('Error processing webhook:', error);
    res.status(400).send('Bad Request');
  }
});

app.get('/events', (req, res) => {
  try {
    const events = getEvents.all();
    res.json(events);
  } catch (error) {
    console.error('Error fetching events:', error);
    res.status(500).send('Internal Server Error');
  }
});

app.listen(port, () => {
  console.log(`LiveKit webhook server running on port ${port}`);
});
