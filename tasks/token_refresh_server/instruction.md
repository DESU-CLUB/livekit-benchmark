## Background
LiveKit access tokens are JWTs with a configurable TTL. For security, production applications issue short-lived tokens (e.g. 30 minutes) and provide a refresh endpoint so clients can renew them before expiry without re-authenticating. The `AccessToken` constructor accepts a `ttl` option as a duration string like `'30m'`.

## Requirements
Build a Node.js token server that issues short-lived tokens with a 30-minute TTL and provides a `/refresh` endpoint.

## Implementation Guide
See `instruction.md` for full details.

## Constraints
- Project path: `/home/user/livekit-token-server`
- Port: `3000`
- Start command: `node server.js`
- `express` and `livekit-server-sdk` npm packages are already installed
- Token TTL must be `'30m'`
- All three endpoints: `GET /token`, `POST /refresh`, `GET /health`

## Integrations
- **LiveKit Node.js Server SDK**: `AccessToken` with `ttl` option
- **Express**: HTTP framework
