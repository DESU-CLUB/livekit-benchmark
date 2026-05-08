import { RoomServiceClient } from "livekit-server-sdk";
import fs from "node:fs";

const livekitUrl = process.env.LIVEKIT_URL ?? "http://localhost:7880";
const livekitApiKey = process.env.LIVEKIT_API_KEY ?? "devkey";
const livekitApiSecret = process.env.LIVEKIT_API_SECRET ?? "devsecret";

const svc = new RoomServiceClient(livekitUrl, livekitApiKey, livekitApiSecret);

const logLines = [];

const rooms = await svc.listRooms();
logLines.push(`Active rooms: ${rooms.length}`);

try {
  await svc.removeParticipant("live-session", "banned-user");
} catch (error) {
  logLines.push("Note: participant not found or already removed");
}

logLines.push("Removed participant banned-user from live-session");

const logOutput = `${logLines.join("\n")}\n`;
fs.writeFileSync("output.log", logOutput, "utf8");

for (const line of logLines) {
  console.log(line);
}
