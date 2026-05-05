## Background
A full-stack video conferencing application requires a secure backend token server and a React frontend. The backend issues LiveKit access tokens so the browser never touches API credentials. The frontend uses `@livekit/components-react` to render a complete conference UI with a single `LiveKitRoom` + `VideoConference` component pair.

## Requirements
Build a full-stack video conferencing app: a Node.js/Express token backend and a React + Vite frontend using LiveKit components.

## Implementation Guide
See `instruction.md` for full details.

## Constraints
- Backend project path: `/home/user/livekit-meet/backend` — port `3001`
- Frontend project path: `/home/user/livekit-meet/frontend` — port `5173`
- Start backend: `cd /home/user/livekit-meet/backend && node index.js`
- Start frontend: `cd /home/user/livekit-meet/frontend && npm run dev -- --host 0.0.0.0 --port 5173`
- Node.js 20+ and npm are available
- Backend must expose `GET /token?room=<room>&identity=<identity>`
- Frontend must use `VITE_SERVER_URL` env var for the LiveKit server URL

## Integrations
- **LiveKit Node.js Server SDK**: `livekit-server-sdk` npm package (backend)
- **LiveKit Components React**: `@livekit/components-react` npm package (frontend)
- **LiveKit Client**: `livekit-client` npm package (frontend)
- **Express**: HTTP framework (backend)
- **Vite + React**: Frontend build tooling
