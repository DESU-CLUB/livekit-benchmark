const express = require('express');
const { RoomServiceClient } = require('livekit-server-sdk');

// Read environment variables
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

// Create RoomServiceClient instance
const roomService = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

// In-memory Map to track hand raise state
const handRaiseState = new Map();

// Create Express app
const app = express();

// Use JSON middleware
app.use(express.json());

// POST /hand-raise endpoint
app.post('/hand-raise', async (req, res) => {
  const { room, identity } = req.body;

  // Validate required fields
  if (!room || !identity) {
    return res.status(400).json({ error: 'room and identity are required' });
  }

  try {
    // Read current state from handRaiseState, default to false
    const currentState = handRaiseState.get(identity) || false;

    // Toggle the state
    const newCanPublish = !currentState;

    // Update participant permissions via LiveKit Room Service API
    await roomService.updateParticipant(
      room,
      identity,
      undefined,
      {
        canPublish: newCanPublish,
        canSubscribe: true
      }
    );

    // Update handRaiseState with the new value
    handRaiseState.set(identity, newCanPublish);

    // Return JSON response
    res.json({
      identity: identity,
      canPublish: newCanPublish
    });
  } catch (error) {
    console.error('Error updating participant:', error);
    res.status(500).json({ error: 'Failed to update participant permissions' });
  }
});

// GET /hands-up endpoint
app.get('/hands-up', (req, res) => {
  // Iterate over handRaiseState and return array of identities where canPublish is true
  const raisedHands = [];
  for (const [identity, canPublish] of handRaiseState.entries()) {
    if (canPublish) {
      raisedHands.push(identity);
    }
  }

  res.json(raisedHands);
});

// Start server on port 3000
app.listen(3000, () => {
  console.log('Server listening on port 3000');
});