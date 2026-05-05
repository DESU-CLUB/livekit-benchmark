import { RoomServiceClient } from 'livekit-server-sdk';
import fs from 'node:fs/promises';

const url = process.env.LIVEKIT_URL;
const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

if (!url || !apiKey || !apiSecret) {
  console.error('LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET must be set');
  process.exit(1);
}

const svc = new RoomServiceClient(url, apiKey, apiSecret);

async function updateMetadata() {
  try {
    await svc.updateRoomMetadata('conference-room', JSON.stringify({
      status: 'active',
      updated_at: new Date().toISOString(),
    }));

    await fs.appendFile('output.log', 'Metadata updated successfully\n');
  } catch (error) {
    console.error('Error updating metadata:', error);
    process.exit(1);
  }
}

updateMetadata();
