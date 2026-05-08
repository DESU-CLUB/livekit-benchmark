import { RoomServiceClient } from 'livekit-server-sdk';
import { appendFile } from 'fs/promises';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

if (!LIVEKIT_URL || !LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
  console.error('Error: LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET environment variables must be set.');
  process.exit(1);
}

const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

const metadata = JSON.stringify({ status: 'active', updated_at: new Date().toISOString() });
const logFile = resolve(__dirname, 'output.log');

try {
  await svc.updateRoomMetadata('conference-room', metadata);
  await appendFile(logFile, 'Metadata updated successfully\n');
  console.log('Metadata updated successfully');
} catch (err) {
  console.error('Error updating room metadata:', err);
  process.exit(1);
}
