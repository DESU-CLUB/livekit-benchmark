# LiveKit Meet - Full-Stack Video Conferencing Application

A complete video conferencing application built with LiveKit, featuring a secure Node.js/Express backend and a modern React + Vite frontend.

## Project Structure

```
livekit-meet/
├── backend/                 # Node.js/Express token server
│   ├── index.js            # Main server file
│   ├── package.json        # Backend dependencies
│   ├── .env.example        # Environment variables template
│   └── README.md           # Backend documentation
└── frontend/               # React + Vite frontend
    ├── src/
    │   ├── App.jsx         # Main application component
    │   ├── App.css         # Application styles
    │   ├── main.jsx        # React entry point
    │   └── index.css       # Global styles
    ├── index.html          # HTML template
    ├── vite.config.js      # Vite configuration
    ├── package.json        # Frontend dependencies
    ├── .env.example        # Environment variables template
    └── README.md           # Frontend documentation
```

## Features

### Backend
- Secure token generation using LiveKit Server SDK
- RESTful API endpoint for token retrieval
- CORS enabled for cross-origin requests
- Health check endpoint
- Environment-based configuration

### Frontend
- Modern React + Vite setup
- LiveKit Components React for video conferencing UI
- Beautiful gradient design with responsive layout
- Room joining form with validation
- Full-featured video conference interface:
  - Video and audio controls
  - Screen sharing
  - Chat functionality
  - Participant grid view
  - Leave room functionality

## Prerequisites

- Node.js 20+
- npm
- LiveKit Server (running locally or remotely)

## Quick Start

### 1. Start LiveKit Server

First, ensure you have a LiveKit server running. For local development:

```bash
# Using Docker
docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882 \
  livekit/livekit-server \
  --dev \
  --keys "devkey:devsecret"
```

### 2. Start the Backend

```bash
cd /home/user/livekit-meet/backend
npm install
node index.js
```

The backend will start on port 3001.

### 3. Start the Frontend

```bash
cd /home/user/livekit-meet/frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

The frontend will be available at http://localhost:5173

## Configuration

### Backend Environment Variables

Create a `.env` file in the backend directory:

```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=devsecret
```

### Frontend Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_SERVER_URL=http://localhost:3001
```

## API Documentation

### GET /token

Generates a LiveKit access token for joining a video room.

**Query Parameters:**
- `room` (required): The room name to join
- `identity` (required): Unique identifier for the participant

**Example Request:**
```bash
curl "http://localhost:3001/token?room=my-room&identity=user123"
```

**Example Response:**
```json
{
  "token": "jwt_token_here",
  "url": "ws://localhost:7880",
  "room": "my-room",
  "identity": "user123"
}
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

## Usage

1. Open your browser and navigate to http://localhost:5173
2. Enter your name in the "Your Name" field
3. Enter a room name (e.g., "meeting-room")
4. Click "Join Room"
5. Grant browser permissions for camera and microphone
6. Share the room name with others to join the same video conference

## Security Considerations

- API keys and secrets should never be exposed to the frontend
- The backend server handles all token generation
- Use environment variables for sensitive configuration
- In production, use HTTPS and secure WebSocket connections (wss://)
- Implement proper authentication and authorization

## Technologies Used

### Backend
- **Node.js**: Runtime environment
- **Express**: Web framework
- **livekit-server-sdk**: LiveKit server SDK for token generation
- **cors**: Cross-Origin Resource Sharing middleware

### Frontend
- **React**: UI library
- **Vite**: Build tool and dev server
- **@livekit/components-react**: LiveKit React components
- **livekit-client**: LiveKit client SDK

## Development

### Backend Development

```bash
cd backend
npm install
node index.js
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Building for Production

```bash
cd frontend
npm run build
```

The production build will be in the `dist` directory.

## Troubleshooting

### Common Issues

1. **Cannot connect to LiveKit server**
   - Ensure LiveKit server is running
   - Check firewall settings
   - Verify LIVEKIT_URL in backend configuration

2. **Token generation fails**
   - Verify API key and secret are correct
   - Check backend logs for errors
   - Ensure room and identity parameters are provided

3. **Frontend cannot connect to backend**
   - Verify VITE_SERVER_URL is set correctly
   - Check CORS configuration
   - Ensure backend is running on port 3001

4. **Camera/microphone not working**
   - Grant browser permissions
   - Check device settings
   - Ensure no other application is using the devices

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues and enhancement requests!