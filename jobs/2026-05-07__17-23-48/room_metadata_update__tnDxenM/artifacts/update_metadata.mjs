import { RoomServiceClient } from 'livekit-server-sdk';
import fs from 'fs/promises';
import process from 'process';

// Read credentials from environment variables
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

// Create RoomServiceClient instance
const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

try {
  // Update room metadata
  await svc.updateRoomMetadata(
    'conference-room',
    JSON.stringify({ status: 'active', updated_at: new Date().toISOString() })
  );

  // Append success message to output.log
  await fs.appendFile('/home/user/livekit-admin/output.log', 'Metadata updated successfully\n');
} catch (error) {
  // Log error to stderr and exit with code 1
  console.error(error);
  process.exit(1);
}