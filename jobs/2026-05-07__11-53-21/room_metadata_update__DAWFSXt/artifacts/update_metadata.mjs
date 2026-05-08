import { RoomServiceClient } from 'livekit-server-sdk';
import { appendFileSync } from 'fs';

const url = process.env.LIVEKIT_URL;
const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

if (!url || !apiKey || !apiSecret) {
    console.error('Missing LIVEKIT_URL, LIVEKIT_API_KEY, or LIVEKIT_API_SECRET');
    process.exit(1);
}

const svc = new RoomServiceClient(url, apiKey, apiSecret);

async function main() {
    try {
        const metadata = JSON.stringify({ status: 'active', updated_at: new Date().toISOString() });
        await svc.updateRoomMetadata('conference-room', metadata);
        appendFileSync('output.log', 'Metadata updated successfully\n');
    } catch (error) {
        console.error('Error updating metadata:', error);
        process.exit(1);
    }
}

main();
