'use strict';

const express = require('express');
const { AccessToken } = require('livekit-server-sdk');

const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

const app = express();

app.get('/token', async (req, res) => {
  const { room, identity } = req.query;

  if (!room || !identity) {
    return res.status(400).json({ error: 'Missing required query parameters: room and identity' });
  }

  const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { identity });

  at.addGrant({
    roomJoin: true,
    room,
    canPublish: true,
    canSubscribe: true,
  });

  const token = await at.toJwt();

  return res.json({ token });
});

app.listen(3000, () => {
  console.log('LiveKit token server listening on port 3000');
});
