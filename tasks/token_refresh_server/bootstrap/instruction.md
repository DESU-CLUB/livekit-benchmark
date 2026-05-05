# Build a LiveKit Token Refresh Server

Build a Node.js token server at `/home/user/livekit-token-server` that issues short-lived tokens and supports token refresh.

## Requirements

Create `server.js` that:

1. **Listens on port 3000.**

2. **`GET /token?room=<room>&identity=<identity>`**
   - Issues an `AccessToken` with TTL of `'30m'`
   - Grants: `roomJoin: true`, `canPublish: true`, `canSubscribe: true`
   - Returns: `{ token, identity, room, expiresIn: '30m' }`

3. **`POST /refresh`**
   - Request body (JSON): `{ room, identity }`
   - Issues a fresh `AccessToken` with the same grants and TTL
   - Returns: `{ token, identity, room, refreshed: true }`

4. **`GET /health`** — returns `{ status: 'ok' }` with HTTP 200.

5. Reads `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from environment variables.

## Implementation

```js
const express = require('express');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
app.use(express.json());

const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

function createToken(identity, room) {
  const at = new AccessToken(apiKey, apiSecret, {
    identity,
    ttl: '30m',
  });
  at.addGrant({ roomJoin: true, room, canPublish: true, canSubscribe: true });
  return at.toJwt();
}

app.get('/token', async (req, res) => {
  const { room, identity } = req.query;
  const token = await createToken(identity, room);
  res.json({ token, identity, room, expiresIn: '30m' });
});

app.post('/refresh', async (req, res) => {
  const { room, identity } = req.body;
  const token = await createToken(identity, room);
  res.json({ token, identity, room, refreshed: true });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(3000, () => console.log('Token server listening on port 3000'));
```
