const express = require("express");
const { AccessToken, VideoGrants } = require("livekit-server-sdk");

const apiKey = process.env.LIVEKIT_API_KEY;
const apiSecret = process.env.LIVEKIT_API_SECRET;

const app = express();
const port = 3000;

app.get("/token", (req, res) => {
  const { room, identity } = req.query;

  if (!room || !identity) {
    return res.status(400).json({ error: "room and identity are required" });
  }

  const grant = new VideoGrants({
    roomJoin: true,
    room,
    canPublish: true,
    canSubscribe: true,
  });

  const token = new AccessToken(apiKey, apiSecret, { identity });
  token.addGrant(grant);

  return res.json({ token: token.toJwt() });
});

app.listen(port, () => {
  console.log(`LiveKit token server listening on port ${port}`);
});
