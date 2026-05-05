import { RoomServiceClient } from 'livekit-server-sdk';
import { appendFileSync } from 'fs';

const url = process.env.LIVEKIT_URL;
const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

const room = process.argv[2];
const identity = process.argv[3];
const trackSid = process.argv[4];

if (!room || !identity || !trackSid) {
  console.error('Usage: node mute_track.mjs <room> <identity> <trackSid>');
  process.exit(1);
}

if (!url || !apiKey || !apiSecret) {
  console.error('Environment variables LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET must be set');
  process.exit(1);
}

async function muteTrack() {
  const svc = new RoomServiceClient(url, apiKey, apiSecret);
  try {
    await svc.mutePublishedTrack(room, identity, trackSid, true);
    const message = `Track muted: ${trackSid}`;
    appendFileSync('output.log', message + '\n');
    console.log(message);
  } catch (error) {
    console.error('Error muting track:', error.message);
    process.exit(1);
  }
}

muteTrack();
