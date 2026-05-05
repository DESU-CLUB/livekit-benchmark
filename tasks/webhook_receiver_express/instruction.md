# LiveKit Webhook Receiver (Express)

## Background
LiveKit can send webhook events to a server endpoint when things happen in rooms (e.g., participant joined, participant left, track published, room finished). The `WebhookReceiver` class in the Node.js server SDK validates the webhook signature using your API secret and decodes the event payload. It requires the raw request body (not parsed JSON), so Express must be configured with `express.raw({ type: 'application/webhook+json' })` middleware.

## Requirements
Build a Node.js/Express server that receives LiveKit webhook events, validates their signatures, and logs event names to a file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-webhook`.
2. Create a file named `server.js` that:
   - Imports `express` and `WebhookReceiver` from `livekit-server-sdk`.
   - Reads `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from environment variables.
   - Creates an Express app listening on port `4000`.
   - Applies `express.raw({ type: 'application/webhook+json' })` middleware **before** the route.
   - Implements `POST /webhook`:
     - Gets the `Authorization` header.
     - Calls `receiver.receive(body, authHeader)` where `body` is the raw buffer (`req.body`) and `authHeader` is the Authorization header value.
     - On validation success: appends the event's `event` field to `/home/user/livekit-webhook/events.log` (one event name per line).
     - On validation failure or error: returns HTTP `401`.
3. Start the server: `node server.js`

## Constraints
- Project path: `/home/user/livekit-webhook`
- Log file: `/home/user/livekit-webhook/events.log`
- Port: `4000`
- Start command: `node server.js`
- `express` and `livekit-server-sdk` npm packages are already installed
- Must use `express.raw({ type: 'application/webhook+json' })` for body parsing
- Must use `WebhookReceiver` for signature validation

## Integrations
- **LiveKit Node.js Server SDK**: `WebhookReceiver` for signature validation and event decoding
- **Express**: HTTP framework
