const express = require('express');
const { RoomServiceClient } = require('livekit-server-sdk');

const app = express();
app.use(express.json());

const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

const roomService = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

// In-memory state tracking: identity -> canPublish (boolean)
const handRaiseState = new Map();

/**
 * POST /hand-raise
 * Body: { "room": "<room-name>", "identity": "<participant-identity>" }
 */
app.post('/hand-raise', async (req, res) => {
  const { room, identity } = req.body;

  if (!room || !identity) {
    return res.status(400).json({ error: 'room and identity are required' });
  }

  try {
    const currentState = handRaiseState.get(identity) || false;
    const newCanPublish = !currentState;

    await roomService.updateParticipant(room, identity, undefined, {
      canPublish: newCanPublish,
      canSubscribe: true,
    });

    handRaiseState.set(identity, newCanPublish);

    res.json({ identity, canPublish: newCanPublish });
  } catch (error) {
    console.error('Error updating participant:', error);
    res.status(500).json({ error: 'Failed to update participant permissions' });
  }
});

/**
 * GET /hands-up
 * Returns a list of identities where canPublish is true
 */
app.get('/hands-up', (req, res) => {
  const handsUp = [];
  for (const [identity, canPublish] of handRaiseState.entries()) {
    if (canPublish) {
      handsUp.push(identity);
    }
  }
  res.json(handsUp);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
