# LiveKit Webhook Server

A production-grade Node.js Express webhook server for handling LiveKit events with HMAC signature validation.

## Features

- ✅ HMAC signature validation using LiveKit's WebhookReceiver
- ✅ Dedicated handler functions for all major event types
- ✅ Event logging to file for audit trails
- ✅ Express.raw() middleware for preserving raw body
- ✅ Health check endpoint
- ✅ Error handling and logging

## Supported Event Types

- `room_started` - When a room is created
- `room_finished` - When a room is destroyed
- `participant_joined` - When a participant joins a room
- `participant_left` - When a participant leaves a room
- `track_published` - When a participant publishes a track
- `track_unpublished` - When a participant unpublishes a track
- `track_subscribed` - When a participant subscribes to a track
- `track_unsubscribed` - When a participant unsubscribes from a track
- `egress_started` - When an egress recording starts
- `egress_ended` - When an egress recording ends
- `egress_updated` - When an egress status updates
- `participant_metadata_updated` - When participant metadata changes
- `room_metadata_updated` - When room metadata changes

## Installation

Dependencies are already installed:

```bash
npm install
```

## Configuration

Set environment variables:

```bash
export LIVEKIT_WEBHOOK_SECRET="your-webhook-secret-from-livekit"
export PORT=4000  # Optional, defaults to 4000
```

Or create a `.env` file:

```env
LIVEKIT_WEBHOOK_SECRET=your-webhook-secret
PORT=4000
```

## Usage

Start the server:

```bash
node server.js
```

The server will start on port 4000 with the following endpoints:

- **Webhook**: `http://localhost:4000/webhook`
- **Health Check**: `http://localhost:4000/health`

## LiveKit Configuration

Configure your LiveKit server to send webhooks to this endpoint:

```bash
livekit-server --webhook-url http://your-server:4000/webhook --webhook-secret your-secret
```

Or update your LiveKit configuration file:

```yaml
webhook:
  url: http://your-server:4000/webhook
  secret: your-webhook-secret
```

## Event Logging

Events are logged to `events.log` in the following format:

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "event": {
    "type": "participant_joined",
    "room": {
      "sid": "RM_xxx",
      "name": "my-room"
    },
    "participant": {
      "sid": "PA_xxx",
      "identity": "user123",
      "name": "John Doe"
    }
  }
}
```

## Security

- HMAC signature verification is mandatory for all webhook requests
- Raw body is preserved for signature validation
- Invalid signatures are rejected with 401 status
- No global JSON middleware to prevent body parsing issues

## Architecture

```
┌─────────────┐
│  LiveKit    │
└──────┬──────┘
       │
       │ Webhook with HMAC Signature
       ▼
┌─────────────────────────────────────┐
│         Express Server               │
│  ┌───────────────────────────────┐  │
│  │  express.raw() Middleware     │  │
│  └──────────────┬────────────────┘  │
│                 │                    │
│                 ▼                    │
│  ┌───────────────────────────────┐  │
│  │  WebhookReceiver.verify()     │  │
│  └──────────────┬────────────────┘  │
│                 │                    │
│                 ▼                    │
│  ┌───────────────────────────────┐  │
│  │      Event Router             │  │
│  │  (routes by event type)       │  │
│  └──────────────┬────────────────┘  │
│                 │                    │
│      ┌──────────┼──────────┐        │
│      ▼          ▼          ▼        │
│  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │ Room │  │ Track│  │Egress│      │
│  │Events│  │Events│  │Events│      │
│  └──┬───┘  └──┬───┘  └──┬───┘      │
└─────┼─────────┼─────────┼──────────┘
      │         │         │
      └─────────┼─────────┘
                ▼
        ┌───────────────┐
        │ events.log    │
        └───────────────┘
```

## Testing

Test the health endpoint:

```bash
curl http://localhost:4000/health
```

Expected response:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Troubleshooting

### Invalid webhook signature

- Ensure `LIVEKIT_WEBHOOK_SECRET` matches your LiveKit server configuration
- Check that the webhook URL is accessible from your LiveKit server
- Verify the authorization header format

### Events not being logged

- Check server logs for errors
- Verify file write permissions for `events.log`
- Ensure the webhook URL is correct in LiveKit configuration

### Server not starting

- Check if port 4000 is already in use
- Verify all dependencies are installed
- Check Node.js version compatibility

## Development

To add new event handlers:

1. Create a handler function following the naming pattern `handleEventType`
2. Add the case to the `routeEvent()` switch statement
3. Events will be automatically logged

Example:

```javascript
function handleMyNewEvent(event) {
  console.log(`[My New Event] Data: ${JSON.stringify(event)}`);
  logEvent({
    type: 'my_new_event',
    data: event
  });
}

// Add to routeEvent():
case 'my_new_event':
  handleMyNewEvent(event);
  break;
```

## License

MIT