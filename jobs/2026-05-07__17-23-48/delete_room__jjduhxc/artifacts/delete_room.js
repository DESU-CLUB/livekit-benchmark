const { RoomServiceClient } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

// Read environment variables
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

// Validate environment variables
if (!LIVEKIT_URL || !LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
  console.error('Error: LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET environment variables are required');
  process.exit(1);
}

// Create RoomServiceClient instance
const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

// Room name to delete
const ROOM_NAME = 'old-meeting-room';

// Log file path
const LOG_FILE = '/home/user/livekit-admin/output.log';

async function deleteRoom() {
  try {
    // First, create the target room so there is something to delete
    // Treat "already exists" error as success
    try {
      await svc.createRoom({ name: ROOM_NAME });
      console.log(`Room '${ROOM_NAME}' created successfully`);
    } catch (createError) {
      // Check if error is "already exists" - treat as success
      if (createError.message && createError.message.includes('already exists')) {
        console.log(`Room '${ROOM_NAME}' already exists, proceeding to delete`);
      } else {
        // Rethrow other errors
        throw createError;
      }
    }

    // Delete the room
    try {
      await svc.deleteRoom(ROOM_NAME);
      console.log(`Room '${ROOM_NAME}' deleted successfully`);
      
      // Append success message to log file
      const logMessage = 'Room deleted successfully\n';
      fs.appendFileSync(LOG_FILE, logMessage, 'utf8');
      console.log(`Logged success to ${LOG_FILE}`);
    } catch (deleteError) {
      // Handle room not found gracefully - should not crash the script
      if (deleteError.message && deleteError.message.includes('not found')) {
        console.log(`Room '${ROOM_NAME}' not found, treating as success`);
        const logMessage = 'Room deleted successfully\n';
        fs.appendFileSync(LOG_FILE, logMessage, 'utf8');
        console.log(`Logged success to ${LOG_FILE}`);
      } else {
        throw deleteError;
      }
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Run the delete room function
deleteRoom()
  .then(() => {
    console.log('Script completed successfully');
    process.exit(0);
  })
  .catch((error) => {
    console.error('Script failed:', error);
    process.exit(1);
  });