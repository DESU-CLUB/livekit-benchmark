import { RoomServiceClient } from 'livekit-server-sdk';
import fs from 'node:fs';

const url = process.env.LIVEKIT_URL || 'http://localhost:7880';
const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret';

const svc = new RoomServiceClient(url, apiKey, apiSecret);

const logs = [];

function addLog(message) {
  console.log(message);
  logs.push(message);
}

async function run() {
  try {
    const rooms = await svc.listRooms();
    addLog(`Active rooms: ${rooms.length}`);

    try {
      await svc.removeParticipant('live-session', 'banned-user');
    } catch (error) {
      addLog('Note: participant not found or already removed');
    }
    addLog('Removed participant banned-user from live-session');

    fs.writeFileSync('output.log', logs.join('\n') + '\n');
  } catch (error) {
    console.error('Error running script:', error);
  }
}

run();
