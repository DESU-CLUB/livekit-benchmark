const express = require('express');
const { AccessToken, VideoGrants } = require('livekit-server-sdk');

const app = express();
const port = 3000;

const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

app.get('/token', async (req, res) => {
  const { room, identity } = req.query;

  if (!room || !identity) {
    return res.status(400).json({ error: 'room and identity query parameters are required' });
  }

  if (!apiKey || !apiSecret) {
    return res.status(500).json({ error: 'LiveKit API key or secret not configured' });
  }

  const at = new AccessToken(apiKey, apiSecret, {
    identity: identity,
  });

  at.addGrant({
    roomJoin: true,
    room: room,
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
