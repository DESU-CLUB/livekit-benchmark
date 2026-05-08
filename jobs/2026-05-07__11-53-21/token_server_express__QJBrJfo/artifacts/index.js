const express = require('express');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
const port = 3000;

app.get('/token', async (req, res) => {
  const { room, identity } = req.query;

  if (!room || !identity) {
    return res.status(400).json({ error: 'room and identity are required' });
  }

  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;

  const at = new AccessToken(apiKey, apiSecret, {
    identity,
  });

  at.addGrant({
    roomJoin: true,
    room,
    canPublish: true,
    canSubscribe: true,
  });

  try {
    const token = await at.toJwt();
    res.json({ token });
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate token' });
  }
});

app.listen(port, () => {
  console.log(`LiveKit token server listening on port ${port}`);
});
