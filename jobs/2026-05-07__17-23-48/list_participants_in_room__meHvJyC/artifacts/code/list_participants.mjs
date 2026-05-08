import { RoomServiceClient } from 'livekit-server-sdk';
import { writeFileSync } from 'fs';

// Read environment variables
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

try {
  // Create RoomServiceClient instance
  const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

  // Retrieve participants from 'main-room'
  const participants = await svc.listParticipants('main-room');

  // Serialize to JSON array with pretty formatting
  const json = JSON.stringify(participants, null, 2);

  // Write to participants.json
  writeFileSync('participants.json', json);

  console.log(`Successfully retrieved ${participants.length} participant(s)`);
  console.log('Result saved to participants.json');
} catch (error) {
  console.error('Error retrieving participants:', error.message);
  process.exit(1);
}