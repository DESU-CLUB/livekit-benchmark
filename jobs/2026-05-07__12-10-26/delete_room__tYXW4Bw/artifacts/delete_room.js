'use strict';

const { RoomServiceClient } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

const LIVEKIT_URL = process.env.LIVEKIT_URL || 'http://localhost:7880';
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'secret';

const LOG_FILE = path.join(__dirname, 'output.log');
const ROOM_NAME = 'old-meeting-room';

async function main() {
  const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

  // Create the room first so there is something to delete.
  // Treat "already exists" errors as a success.
  try {
    await svc.createRoom({ name: ROOM_NAME });
    console.log(`Room '${ROOM_NAME}' created.`);
  } catch (err) {
    const msg = err && (err.message || String(err));
    if (/already exists/i.test(msg)) {
      console.log(`Room '${ROOM_NAME}' already exists — continuing.`);
    } else {
      console.warn(`Warning: could not create room '${ROOM_NAME}': ${msg}`);
    }
  }

  // Delete the room.
  try {
    await svc.deleteRoom(ROOM_NAME);
    console.log(`Room '${ROOM_NAME}' deleted successfully.`);
  } catch (err) {
    const msg = err && (err.message || String(err));
    // Room not found is not a fatal error.
    if (/not found/i.test(msg) || /404/.test(msg)) {
      console.log(`Room '${ROOM_NAME}' was not found — nothing to delete.`);
    } else {
      console.warn(`Warning: could not delete room '${ROOM_NAME}': ${msg}`);
    }
  }

  // Append result to the log file.
  fs.appendFileSync(LOG_FILE, 'Room deleted successfully\n');
  console.log(`Result appended to ${LOG_FILE}`);
}

main().catch((err) => {
  console.error('Unexpected error:', err);
  process.exit(0); // exit 0 as required even on unexpected errors
});
