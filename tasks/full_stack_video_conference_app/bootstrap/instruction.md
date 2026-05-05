# Build a Full-Stack Video Conferencing App

Build a video conferencing application with a Node.js backend and a React frontend.

## Backend

Create a Node.js Express server at `/home/user/livekit-meet/backend`:

- Install dependencies: `express`, `livekit-server-sdk`, `cors`
- Create `index.js` that:
  - Listens on port **3001**
  - Exposes `GET /token?room=<room>&identity=<identity>` using `AccessToken` from `livekit-server-sdk`
  - Returns `{ token: "<jwt>" }`
  - Reads `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from environment variables
  - Enables CORS so the frontend can call it

## Frontend

Create a React + Vite app at `/home/user/livekit-meet/frontend`:

- Use `npm create vite@latest frontend -- --template react` (or equivalent)
- Install dependencies: `@livekit/components-react`, `livekit-client`
- The main page (`App.jsx` or `App.tsx`) should:
  - Fetch a token from `http://localhost:3001/token?room=my-room&identity=user-<random>`
  - Render a `LiveKitRoom` component that connects to the LiveKit server using `VITE_SERVER_URL` (from `.env` or hardcoded for dev)
  - Place a `VideoConference` component inside `LiveKitRoom`
- Create a `.env` file in the frontend with `VITE_SERVER_URL=<your LiveKit server URL>`

## Start Commands

- Backend: `cd /home/user/livekit-meet/backend && node index.js`
- Frontend: `cd /home/user/livekit-meet/frontend && npm run dev -- --host 0.0.0.0 --port 5173`
