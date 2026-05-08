# LiveKit Token Server

A Node.js server that issues short-lived LiveKit access tokens with a 30-minute TTL and provides a refresh endpoint.

## Features

- **Short-lived tokens**: Tokens expire after 30 minutes for enhanced security
- **Token refresh**: Clients can renew tokens without re-authenticating
- **Health check**: Monitor server status

## Installation

Dependencies are already installed:
```bash
npm install
```

## Configuration

Create a `.env` file with your LiveKit credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```
LIVEKIT_API_KEY=your_api_key_here
LIVEKIT_API_SECRET=your_api_secret_here
```

## Usage

Start the server:
```bash
node server.js
```

The server will start on port 3000.

## API Endpoints

### GET /token

Issues a new short-lived access token with a 30-minute TTL.

**Query Parameters:**
- `identity` (required): User identity for the token
- `roomName` (optional): Room name to grant access to

**Example:**
```bash
curl "http://localhost:3000/token?identity=user123&roomName=my-room"
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "identity": "user123",
  "roomName": "my-room",
  "expiresIn": 1800
}
```

### POST /refresh

Refreshes an existing token without requiring re-authentication.

**Request Body:**
- `identity` (required): User identity for the new token
- `roomName` (optional): Room name to grant access to

**Example:**
```bash
curl -X POST http://localhost:3000/refresh \
  -H "Content-Type: application/json" \
  -d '{"identity":"user123","roomName":"my-room"}'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "identity": "user123",
  "roomName": "my-room",
  "expiresIn": 1800,
  "refreshedAt": "2026-05-08T00:46:10.000Z"
}
```

### GET /health

Health check endpoint.

**Example:**
```bash
curl http://localhost:3000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-08T00:46:10.000Z"
}
```

## Security Notes

- Tokens have a 30-minute TTL for enhanced security
- Clients should call `/refresh` before token expiration
- Use environment variables for API credentials in production
- Consider adding authentication to the `/token` and `/refresh` endpoints in production

## License

MIT