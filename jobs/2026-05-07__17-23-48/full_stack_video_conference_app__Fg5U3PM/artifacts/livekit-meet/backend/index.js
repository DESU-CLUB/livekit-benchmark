const express = require('express');
const cors = require('cors');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// LiveKit configuration
// In production, these should be loaded from environment variables
const LIVEKIT_URL = process.env.LIVEKIT_URL || 'ws://localhost:7880';
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'devsecret';

// Token endpoint
app.get('/token', (req, res) => {
  try {
    const { room, identity } = req.query;

    // Validate required parameters
    if (!room || !identity) {
      return res.status(400).json({
        error: 'Missing required parameters',
        message: 'Both "room" and "identity" query parameters are required'
      });
    }

    // Create access token
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: identity,
    });

    // Add room join grant
    token.addGrant({
      room: room,
      roomJoin: true,
      canPublish: true,
      canSubscribe: true,
    });

    // Generate token string
    const jwt = token.toJwt();

    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      room: room,
      identity: identity
    });
  } catch (error) {
    console.error('Error generating token:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to generate access token'
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'LiveKit token server is running' });
});

// Start server
app.listen(PORT, () => {
  console.log(`LiveKit token server running on port ${PORT}`);
  console.log(`Token endpoint: http://localhost:${PORT}/token?room=<room>&identity=<identity>`);
});