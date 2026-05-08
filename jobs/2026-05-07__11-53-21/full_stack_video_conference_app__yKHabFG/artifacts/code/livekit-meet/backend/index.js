require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
app.use(cors());

const port = process.env.PORT || 3001;

app.get('/token', async (req, res) => {
  const { room, identity } = req.query;

  if (!room || !identity) {
    return res.status(400).json({ error: 'room and identity are required' });
  }

  const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
  const apiSecret = process.env.LIVEKIT_API_SECRET || 'secret';

  const at = new AccessToken(apiKey, apiSecret, {
    identity: identity,
  });

  at.addGrant({ roomJoin: true, room: room });

  try {
    const token = await at.toJwt();
    console.log("Generated token:", token);
    res.json({ token });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(port, () => {
  console.log(`Backend listening on port ${port}`);
});
