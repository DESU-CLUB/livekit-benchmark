'use strict';

const express = require('express');
const { AccessToken, TokenVerifier } = require('livekit-server-sdk');

const app = express();
app.use(express.json());

const PORT = 3000;
const TOKEN_TTL = '30m';

// Read API credentials from environment variables with sensible defaults for local dev
const LIVEKIT_API_KEY    = process.env.LIVEKIT_API_KEY    || 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'devsecret0123456789abcdefghijklm'; // ≥32 chars

/**
 * Build and sign a new AccessToken for the given identity and room.
 * TTL is always 30 minutes.
 */
async function buildToken(identity, room, name) {
  const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
    identity,
    name: name || identity,
    ttl: TOKEN_TTL,
  });

  at.addGrant({
    roomJoin: true,
    room,
    canPublish: true,
    canSubscribe: true,
  });

  return at.toJwt();
}

// ---------------------------------------------------------------------------
// GET /token
// Query params: identity (required), room (required), name (optional)
// Returns a short-lived (30 min) JWT for the requested room.
// ---------------------------------------------------------------------------
app.get('/token', async (req, res) => {
  const { identity, room, name } = req.query;

  if (!identity || !room) {
    return res.status(400).json({
      error: 'Missing required query parameters: identity, room',
    });
  }

  try {
    const token = await buildToken(identity, room, name);
    return res.json({ token, ttl: TOKEN_TTL });
  } catch (err) {
    console.error('Error generating token:', err);
    return res.status(500).json({ error: 'Failed to generate token' });
  }
});

// ---------------------------------------------------------------------------
// POST /refresh
// Body (JSON): { token: "<existing JWT>", room?: "<room name>" }
// Verifies the existing token, then issues a fresh 30-minute token using the
// same identity and room claim. The caller may optionally override the room.
// ---------------------------------------------------------------------------
app.post('/refresh', async (req, res) => {
  const { token, room: roomOverride } = req.body || {};

  if (!token) {
    return res.status(400).json({ error: 'Missing required body field: token' });
  }

  try {
    const verifier = new TokenVerifier(LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

    // clockTolerance of '1m' allows tokens that expired up to 60 s ago to
    // still be refreshed, giving clients a small grace window.
    const claims = await verifier.verify(token, '1m');

    const identity = claims.sub;
    const room     = roomOverride || claims.video?.room;
    const name     = claims.name;

    if (!identity) {
      return res.status(400).json({ error: 'Token is missing identity (sub) claim' });
    }
    if (!room) {
      return res.status(400).json({
        error: 'Could not determine room from token; provide "room" in the request body',
      });
    }

    const newToken = await buildToken(identity, room, name);
    return res.json({ token: newToken, ttl: TOKEN_TTL });
  } catch (err) {
    // Distinguish verification failures from unexpected errors
    const isAuthError =
      err.code === 'ERR_JWT_EXPIRED' ||
      err.code === 'ERR_JWS_SIGNATURE_VERIFICATION_FAILED' ||
      err.code === 'ERR_JWT_INVALID' ||
      err.message?.toLowerCase().includes('expired') ||
      err.message?.toLowerCase().includes('invalid') ||
      err.message?.toLowerCase().includes('signature');

    if (isAuthError) {
      return res.status(401).json({ error: 'Token verification failed: ' + err.message });
    }

    console.error('Error refreshing token:', err);
    return res.status(500).json({ error: 'Failed to refresh token' });
  }
});

// ---------------------------------------------------------------------------
// GET /health
// Simple liveness check; returns 200 with service status.
// ---------------------------------------------------------------------------
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'livekit-token-server' });
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
app.listen(PORT, () => {
  console.log(`LiveKit token server listening on port ${PORT}`);
  console.log(`  GET  /token   – issue a new ${TOKEN_TTL} token`);
  console.log(`  POST /refresh – refresh an existing token`);
  console.log(`  GET  /health  – liveness check`);
});
