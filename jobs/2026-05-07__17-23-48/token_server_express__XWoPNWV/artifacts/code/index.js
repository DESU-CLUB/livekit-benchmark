const express = require('express');
const { AccessToken, VideoGrants } = require('livekit-server-sdk');

// Read credentials from environment variables
const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

// Create Express app
const app = express();
const PORT = 3000;

// GET /token endpoint
app.get('/token', (req, res) => {
  const { room, identity } = req.query;

  // Validate required parameters
  if (!room || !identity) {
    return res.status(400).json({
      error: 'Missing required parameters: room and identity are required'
    });
  }

  try {
    // Create access token with the given identity
    const token = new AccessToken(apiKey, apiSecret, {
      identity: identity,
    });

    // Add video grants
    token.addGrant(new VideoGrants({
      roomJoin: true,
      room: room,
      canPublish: true,
      canSubscribe: true,
    }));

    // Generate and return the JWT
    const jwt = token.toJwt();
    res.json({ token: jwt });
  } catch (error) {
    console.error('Error generating token:', error);
    res.status(500).json({
      error: 'Failed to generate token'
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`LiveKit token server listening on port ${PORT}`);
});