# Build a Secure LiveKit Webhook Server

Build a production-grade Node.js webhook handler at `/home/user/livekit-webhook`.

## Requirements

Create `server.js` that:

1. **Listens on port 4000.**

2. **Uses `express.raw({type: 'application/webhook+json'})` middleware** — apply this ONLY to the `/webhook` route (do NOT use `express.json()` before it, as that will corrupt the raw body needed for signature verification).

3. **Validates the webhook signature** using `WebhookReceiver` from `livekit-server-sdk`:
   ```js
   const { WebhookReceiver } = require('livekit-server-sdk');
   const receiver = new WebhookReceiver(process.env.LIVEKIT_API_KEY, process.env.LIVEKIT_API_SECRET);
   const event = await receiver.receive(req.body, req.get('Authorization'));
   ```

4. **Handles these event types** with separate named handler functions:
   - `room_started`
   - `room_finished`
   - `participant_joined`
   - `participant_left`
   - `track_published`

5. **Returns HTTP 200** on successful signature validation, **HTTP 401** on invalid signature.

6. **Logs each event type** to `/home/user/livekit-webhook/events.log` (append mode). Each line should be: `[timestamp] EVENT_TYPE: <details>`.

7. **`GET /health`** returns `{"status": "ok"}` with HTTP 200.

## Event Router Pattern

```js
const handlers = {
  room_started: handleRoomStarted,
  room_finished: handleRoomFinished,
  participant_joined: handleParticipantJoined,
  participant_left: handleParticipantLeft,
  track_published: handleTrackPublished,
};

app.post('/webhook', express.raw({type: 'application/webhook+json'}), async (req, res) => {
  const receiver = new WebhookReceiver(apiKey, apiSecret);
  try {
    const event = await receiver.receive(req.body, req.get('Authorization'));
    const handler = handlers[event.event];
    if (handler) await handler(event);
    res.status(200).json({ received: true });
  } catch (e) {
    res.status(401).json({ error: 'Invalid signature' });
  }
});
```
