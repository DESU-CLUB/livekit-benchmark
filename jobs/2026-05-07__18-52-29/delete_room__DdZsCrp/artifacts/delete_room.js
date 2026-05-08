const { RoomServiceClient } = require('livekit-server-sdk');

const livekitUrl = process.env.LIVEKIT_URL;
const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

if (!livekitUrl || !apiKey || !apiSecret) {
  console.error('Missing LIVEKIT_URL, LIVEKIT_API_KEY, or LIVEKIT_API_SECRET environment variables.');
  process.exit(0);
}

const svc = new RoomServiceClient(livekitUrl, apiKey, apiSecret);

const roomName = 'old-meeting-room';

async function ensureRoomExists() {
  try {
    await svc.createRoom({ name: roomName });
  } catch (error) {
    if (error?.message?.toLowerCase?.().includes('already exists')) {
      return;
    }
    console.warn('Room creation failed:', error?.message || error);
  }
}

async function deleteRoom() {
  try {
    await ensureRoomExists();
    await svc.deleteRoom(roomName);
  } catch (error) {
    console.warn('Room deletion failed:', error?.message || error);
  }
}

deleteRoom()
  .then(async () => {
    const { promises: fs } = require('fs');
    await fs.appendFile('/home/user/livekit-admin/output.log', 'Room deleted successfully\n');
  })
  .catch((error) => {
    console.warn('Unexpected error:', error?.message || error);
  });
