const express = require("express");
const { RoomServiceClient } = require("livekit-server-sdk");

const { LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET } = process.env;

const roomService = new RoomServiceClient(
  LIVEKIT_URL,
  LIVEKIT_API_KEY,
  LIVEKIT_API_SECRET
);

const handRaiseState = new Map();

const app = express();
app.use(express.json());

app.post("/hand-raise", async (req, res) => {
  const { room, identity } = req.body;

  if (!room || !identity) {
    return res.status(400).json({
      error: "room and identity are required",
    });
  }

  const currentState = handRaiseState.get(identity) ?? false;
  const canPublish = !currentState;

  try {
    await roomService.updateParticipant(room, identity, undefined, {
      canPublish,
      canSubscribe: true,
    });

    handRaiseState.set(identity, canPublish);

    return res.json({ identity, canPublish });
  } catch (error) {
    return res.status(500).json({
      error: "Failed to update participant permissions",
      details: error instanceof Error ? error.message : String(error),
    });
  }
});

app.get("/hands-up", (req, res) => {
  const handsUp = [];

  for (const [identity, canPublish] of handRaiseState.entries()) {
    if (canPublish) {
      handsUp.push(identity);
    }
  }

  return res.json(handsUp);
});

app.listen(3000, () => {
  console.log("LiveKit hand-raise server running on port 3000");
});
