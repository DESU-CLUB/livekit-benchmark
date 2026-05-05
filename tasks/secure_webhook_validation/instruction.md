## Background
LiveKit sends signed webhook events to your server for room lifecycle and participant events. A production-grade webhook handler must validate the HMAC signature using `WebhookReceiver`, use `express.raw()` (not `express.json()`) for the webhook route to preserve the raw body for signature verification, and route different event types to dedicated handler functions.

## Requirements
Build a Node.js Express webhook server that validates LiveKit signatures, routes all major event types to handler functions, and logs events to a file.

## Implementation Guide
See `instruction.md` for full details.

## Constraints
- Project path: `/home/user/livekit-webhook`
- Port: `4000`
- Start command: `node server.js`
- Log file: `/home/user/livekit-webhook/events.log`
- `express` and `livekit-server-sdk` npm packages are already installed
- Must use `express.raw({type: 'application/webhook+json'})` for the webhook route
- Must NOT use `express.json()` globally before the webhook route

## Integrations
- **LiveKit Node.js Server SDK**: `WebhookReceiver` for signature validation
- **Express**: HTTP framework
