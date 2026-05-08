import { RoomServiceClient } from 'livekit-server-sdk';
import { writeFile } from 'fs/promises';

const { LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET } = process.env;

if (!LIVEKIT_URL || !LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
  console.error('Error: LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET environment variables must be set.');
  process.exit(1);
}

const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

try {
  let participants;
  try {
    participants = await svc.listParticipants('main-room');
  } catch (err) {
    if (err.code === 'not_found' || err.status === 404) {
      // Room does not exist yet — treat as empty participant list
      participants = [];
    } else {
      throw err;
    }
  }

  const json = JSON.stringify(participants, null, 2);
  await writeFile('participants.json', json, 'utf8');
  console.log(`Saved ${participants.length} participant(s) to participants.json`);
} catch (err) {
  console.error('Error retrieving participants:', err);
  process.exit(1);
}
