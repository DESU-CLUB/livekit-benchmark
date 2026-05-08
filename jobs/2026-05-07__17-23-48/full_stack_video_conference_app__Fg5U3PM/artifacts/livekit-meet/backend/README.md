# LiveKit Meet Backend

Token server for LiveKit video conferencing application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your LiveKit server credentials
```

3. Start the server:
```bash
npm start
```

The server will run on port 3001.

## API Endpoints

### GET /token

Generates a LiveKit access token for joining a video room.

**Query Parameters:**
- `room` (required): The room name to join
- `identity` (required): Unique identifier for the participant

**Response:**
```json
{
  "token": "jwt_token_here",
  "url": "ws://localhost:7880",
  "room": "my-room",
  "identity": "user123"
}
```

**Example:**
```bash
curl "http://localhost:3001/token?room=my-room&identity=user123"
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "LiveKit token server is running"
}
```