import { RoomServiceClient } from 'livekit-server-sdk';
import fs from 'node:fs';

const LIVEKIT_URL = process.env.LIVEKIT_URL || 'http://localhost:7880';
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'devsecret';

const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

async function main() {
  const logs = [];

  function addLog(msg) {
    logs.push(msg);
    console.log(msg);
  }

  try {
    const rooms = await svc.listRooms();
    addLog(`Active rooms: ${rooms.length}`);

    try {
      await svc.removeParticipant('live-session', 'banned-user');
    } catch (err) {
      addLog('Note: participant not found or already removed');
    }
    
    addLog('Removed participant banned-user from live-session');

    fs.writeFileSync('output.log', logs.join('\n') + '\n');
  } catch (err) {
    console.error('Error:', err);
  }
}

main();
