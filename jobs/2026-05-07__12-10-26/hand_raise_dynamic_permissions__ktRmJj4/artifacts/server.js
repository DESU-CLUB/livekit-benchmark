const express = require('express');
const { RoomServiceClient } = require('livekit-server-sdk');

const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

const roomService = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

const handRaiseState = new Map();

const app = express();
app.use(express.json());

app.post('/hand-raise', async (req, res) => {
  const { room, identity } = req.body;

  if (!room || !identity) {
    return res.status(400).json({ error: 'room and identity are required' });
  }

  const currentState = handRaiseState.get(identity) ?? false;
  const newCanPublish = !currentState;

  await roomService.updateParticipant(room, identity, undefined, {
    canPublish: newCanPublish,
    canSubscribe: true,
  });

  handRaiseState.set(identity, newCanPublish);

  return res.json({ identity, canPublish: newCanPublish });
});

app.get('/hands-up', (req, res) => {
  const handsUp = [];
  for (const [identity, canPublish] of handRaiseState) {
    if (canPublish) {
      handsUp.push(identity);
    }
  }
  return res.json(handsUp);
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
