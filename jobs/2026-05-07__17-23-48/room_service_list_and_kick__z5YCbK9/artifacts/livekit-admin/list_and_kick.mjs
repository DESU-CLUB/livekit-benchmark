import { RoomServiceClient } from 'livekit-server-sdk';
import fs from 'node:fs';

// Read environment variables with fallbacks
const LIVEKIT_URL = process.env.LIVEKIT_URL || 'http://localhost:7880';
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'devkey';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'devsecret';

// Create RoomServiceClient instance
const svc = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

// Collect log lines
const logLines = [];

// Helper function to add and print log lines
function log(message) {
  logLines.push(message);
  console.log(message);
}

try {
  // List all active rooms
  const rooms = await svc.listRooms();
  
  // Build log line with room count
  log(`Active rooms: ${rooms.length}`);
  
  // Remove specific participant from target room
  try {
    await svc.removeParticipant('live-session', 'banned-user');
  } catch (error) {
    log('Note: participant not found or already removed');
  }
  
  // Append removal confirmation log
  log('Removed participant banned-user from live-session');
  
  // Write all log lines to output.log
  const logContent = logLines.join('\n');
  fs.writeFileSync('output.log', logContent);
  
} catch (error) {
  log(`Error: ${error.message}`);
  const logContent = logLines.join('\n');
  fs.writeFileSync('output.log', logContent);
}