import { RoomServiceClient } from 'livekit-server-sdk';
import { appendFile } from 'node:fs/promises';

const { LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET } = process.env;

if (!LIVEKIT_URL || !LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
  console.error('Missing LIVEKIT_URL, LIVEKIT_API_KEY, or LIVEKIT_API_SECRET environment variables.');
  process.exit(1);
}

const run = async () => {
  try {
    const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);
    const metadata = JSON.stringify({
      status: 'active',
      updated_at: new Date().toISOString(),
    });

    await svc.updateRoomMetadata('conference-room', metadata);
    await appendFile('output.log', 'Metadata updated successfully\n');
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
};

await run();
