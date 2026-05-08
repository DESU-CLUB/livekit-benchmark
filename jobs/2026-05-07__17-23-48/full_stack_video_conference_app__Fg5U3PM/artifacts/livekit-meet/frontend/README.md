# LiveKit Meet Frontend

React + Vite frontend for LiveKit video conferencing application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your backend server URL
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on port 5173.

## Build

To build for production:
```bash
npm run build
```

To preview the production build:
```bash
npm run preview
```

## Features

- Join video conferences by entering your name and room name
- Full-featured video conference UI with:
  - Video and audio controls
  - Screen sharing
  - Chat functionality
  - Participant grid view
- Responsive design for all screen sizes

## Environment Variables

- `VITE_SERVER_URL`: URL of the backend token server (default: http://localhost:3001)

## Usage

1. Open the application in your browser
2. Enter your name and a room name
3. Click "Join Room"
4. Share the room name with others to join the same video conference