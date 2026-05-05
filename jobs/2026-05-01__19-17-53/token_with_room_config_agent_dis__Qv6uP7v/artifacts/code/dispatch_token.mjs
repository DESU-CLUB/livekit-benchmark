import { AccessToken } from 'livekit-server-sdk';
import { RoomConfiguration, RoomAgentDispatch } from '@livekit/protocol';
import fs from 'fs';

const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret';

const at = new AccessToken(apiKey, apiSecret, {
  identity: 'host-user',
});

at.addGrant({ roomJoin: true, room: 'ai-room', canPublish: true, canSubscribe: true });

at.roomConfig = new RoomConfiguration({
  agents: [
    new RoomAgentDispatch({
      agentName: 'my-agent',
      metadata: JSON.stringify({ source: 'web' }),
    }),
  ],
});

const token = await at.toJwt();

fs.writeFileSync('token.txt', token);
console.log('Token written to token.txt');
