import { RoomServiceClient } from 'livekit-server-sdk';
import fs from 'node:fs';

const LIVEKIT_URL = process.env.LIVEKIT_URL ?? 'http://localhost:7880';
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY ?? 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET ?? 'devsecret';

const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

const logs = [];

function log(line) {
  logs.push(line);
  console.log(line);
}

const rooms = await svc.listRooms();
log(`Active rooms: ${rooms.length}`);

try {
  await svc.removeParticipant('live-session', 'banned-user');
} catch (err) {
  log('Note: participant not found or already removed');
}

log('Removed participant banned-user from live-session');

fs.writeFileSync('output.log', logs.join('\n') + '\n');
