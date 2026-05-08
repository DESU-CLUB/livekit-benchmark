import { RoomServiceClient } from 'livekit-server-sdk';
import fs from 'fs/promises';

async function main() {
  const url = process.env.LIVEKIT_URL;
  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;

  if (!url || !apiKey || !apiSecret) {
    console.error('Missing LiveKit environment variables: LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET');
    process.exit(1);
  }

  const svc = new RoomServiceClient(url, apiKey, apiSecret);

  try {
    let participants = [];
    try {
      participants = await svc.listParticipants('main-room');
    } catch (e) {
      if (e?.status === 404 || e?.code === 'not_found' || (e?.message && e.message.includes('not exist'))) {
        participants = [];
      } else {
        throw e;
      }
    }
    await fs.writeFile('participants.json', JSON.stringify(participants, null, 2));
    console.log('Participants saved to participants.json');
  } catch (error) {
    console.error('Failed to list participants:', error);
    process.exit(1);
  }
}

main();
