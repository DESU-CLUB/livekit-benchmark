const { RoomServiceClient } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

async function main() {
  const url = process.env.LIVEKIT_URL || 'http://localhost:7880';
  const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
  const apiSecret = process.env.LIVEKIT_API_SECRET || 'secret';

  const svc = new RoomServiceClient(url, apiKey, apiSecret);
  const roomName = 'old-meeting-room';
  const logFile = path.join(__dirname, 'output.log');

  try {
    try {
      await svc.createRoom({ name: roomName });
      console.log(`Room ${roomName} created or already exists.`);
    } catch (createErr) {
      console.log('Error creating room (might already exist):', createErr.message);
    }

    await svc.deleteRoom(roomName);
    console.log('Room deleted successfully');
    fs.appendFileSync(logFile, 'Room deleted successfully\n');
  } catch (error) {
    console.error('Error deleting room:', error.message);
  }
}

main();
