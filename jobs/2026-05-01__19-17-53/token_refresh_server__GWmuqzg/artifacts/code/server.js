const express = require('express');
const { AccessToken, TokenVerifier } = require('livekit-server-sdk');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'secret';

// GET /health
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

// GET /token
app.get('/token', async (req, res) => {
  const room = req.query.room;
  const identity = req.query.identity;

  if (!room || !identity) {
    return res.status(400).json({ error: 'room and identity are required' });
  }

  const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
    identity: identity,
    ttl: '30m',
  });
  at.addGrant({ roomJoin: true, room: room });

  try {
    const token = await at.toJwt();
    res.json({ token });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST /refresh
app.post('/refresh', async (req, res) => {
  const { token } = req.body;

  if (!token) {
    return res.status(400).json({ error: 'token is required' });
  }

  try {
    const verifier = new TokenVerifier(LIVEKIT_API_KEY, LIVEKIT_API_SECRET);
    const grants = await verifier.verify(token);

    // Create a new token with the same grants but new TTL
    const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: grants.sub, // grants.sub is the identity in JWT
      ttl: '30m',
    });

    if (grants.video) {
      at.addGrant(grants.video);
    }
    if (grants.metadata) {
      at.metadata = grants.metadata;
    }
    if (grants.name) {
      at.name = grants.name;
    }
    if (grants.attributes) {
      at.attributes = grants.attributes;
    }

    const newToken = await at.toJwt();
    res.json({ token: newToken });
  } catch (error) {
    res.status(401).json({ error: 'invalid token' });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
