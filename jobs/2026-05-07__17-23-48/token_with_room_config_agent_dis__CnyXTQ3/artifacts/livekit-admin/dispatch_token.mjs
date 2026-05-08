import { AccessToken } from 'livekit-server-sdk';
import { RoomConfiguration, RoomAgentDispatch } from '@livekit/protocol';
import { writeFileSync } from 'fs';

// Read environment variables with fallbacks
const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret';

// Create access token with identity
const at = new AccessToken(apiKey, apiSecret, { identity: 'host-user' });

// Add grants for room access
at.addGrant({ roomJoin: true, room: 'ai-room', canPublish: true, canSubscribe: true });

// Set room configuration with agent dispatch
at.roomConfig = new RoomConfiguration({
  agents: [
    new RoomAgentDispatch({
      agentName: "my-agent",
      metadata: JSON.stringify({ source: "web" })
    })
  ]
});

// Generate JWT
const token = await at.toJwt();

// Write token to file
writeFileSync('token.txt', token);

// Log success message
console.log('Token written to token.txt');