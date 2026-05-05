import { RoomServiceClient } from 'livekit-server-sdk';
import fs from 'node:fs/promises';

const url = process.env.LIVEKIT_URL?.replace('wss://', 'https://');
const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;
const roomName = 'main-room';

if (!url || !apiKey || !apiSecret) {
  console.error('Error: LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET must be set');
  process.exit(1);
}

const svc = new RoomServiceClient(url, apiKey, apiSecret);

async function listParticipants() {
  try {
    const participants = await svc.listParticipants(roomName);
    await fs.writeFile('participants.json', JSON.stringify(participants, null, 2));
    console.log(`Successfully wrote participants to participants.json`);
  } catch (error) {
    console.error('Error listing participants:', error.message || error);
    process.exit(1);
  }
}

listParticipants();
