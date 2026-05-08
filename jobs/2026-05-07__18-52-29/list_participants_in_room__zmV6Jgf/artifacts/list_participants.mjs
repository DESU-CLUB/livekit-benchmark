import { RoomServiceClient } from 'livekit-server-sdk';
import { writeFile } from 'node:fs/promises';

const { LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET } = process.env;

if (!LIVEKIT_URL || !LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
  console.error(
    'Missing LiveKit environment variables. Please set LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET.'
  );
  process.exit(1);
}

const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

try {
  const participants = await svc.listParticipants('main-room');
  const output = JSON.stringify(participants, null, 2);
  await writeFile('participants.json', output, 'utf8');
  console.log('Saved participants to participants.json');
} catch (error) {
  console.error('Failed to list participants:', error);
  process.exit(1);
}
