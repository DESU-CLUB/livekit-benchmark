import { AccessToken } from 'livekit-server-sdk';
import { RoomAgentDispatch, RoomConfiguration } from '@livekit/protocol';
import { writeFile } from 'node:fs/promises';

const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret';

const at = new AccessToken(apiKey, apiSecret, { identity: 'host-user' });

at.addGrant({
  roomJoin: true,
  room: 'ai-room',
  canPublish: true,
  canSubscribe: true,
});

at.roomConfig = new RoomConfiguration({
  agents: [
    new RoomAgentDispatch({
      agentName: 'my-agent',
      metadata: JSON.stringify({ source: 'web' }),
    }),
  ],
});

const token = await at.toJwt();
await writeFile('token.txt', token, 'utf8');
console.log('Token written to token.txt');
