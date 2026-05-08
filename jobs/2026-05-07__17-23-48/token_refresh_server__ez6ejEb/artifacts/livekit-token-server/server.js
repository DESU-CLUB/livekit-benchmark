const express = require('express');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
const PORT = 3000;

// Environment variables for LiveKit credentials
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'secret';

// Middleware
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Get token endpoint - issues a short-lived token with 30-minute TTL
app.get('/token', (req, res) => {
  try {
    const { identity, roomName } = req.query;

    if (!identity) {
      return res.status(400).json({ error: 'identity is required' });
    }

    // Create an access token with 30-minute TTL
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: identity,
      ttl: '30m', // 30 minutes TTL
    });

    // Add video grants
    if (roomName) {
      token.addGrant({
        room: roomName,
        roomJoin: true,
        canPublish: true,
        canSubscribe: true,
      });
    }

    // Generate the JWT token
    const jwt = token.toJwt();

    res.json({
      token: jwt,
      identity: identity,
      roomName: roomName || null,
      expiresIn: 1800, // 30 minutes in seconds
    });
  } catch (error) {
    console.error('Error generating token:', error);
    res.status(500).json({ error: 'Failed to generate token' });
  }
});

// Refresh token endpoint - allows clients to renew their token
app.post('/refresh', (req, res) => {
  try {
    const { identity, roomName } = req.body;

    if (!identity) {
      return res.status(400).json({ error: 'identity is required' });
    }

    // Create a new access token with 30-minute TTL
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: identity,
      ttl: '30m', // 30 minutes TTL
    });

    // Add video grants if roomName is provided
    if (roomName) {
      token.addGrant({
        room: roomName,
        roomJoin: true,
        canPublish: true,
        canSubscribe: true,
      });
    }

    // Generate the new JWT token
    const jwt = token.toJwt();

    res.json({
      token: jwt,
      identity: identity,
      roomName: roomName || null,
      expiresIn: 1800, // 30 minutes in seconds
      refreshedAt: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Error refreshing token:', error);
    res.status(500).json({ error: 'Failed to refresh token' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`LiveKit Token Server running on port ${PORT}`);
  console.log(`Endpoints:`);
  console.log(`  GET  /token   - Issue a new token`);
  console.log(`  POST /refresh - Refresh an existing token`);
  console.log(`  GET  /health  - Health check`);
});

module.exports = app;