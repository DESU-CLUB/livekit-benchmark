const express = require("express");
const { AccessToken } = require("livekit-server-sdk");

const app = express();
app.use(express.json());

const PORT = 3000;
const TOKEN_TTL = "30m";

const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

const requiredEnv = ["LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"];
const missingEnv = requiredEnv.filter((key) => !process.env[key]);
if (missingEnv.length > 0) {
  console.warn(
    `Missing environment variables: ${missingEnv.join(", ")}. Token endpoints will return errors until configured.`,
  );
}

const ensureFields = (payload, fields) => {
  const missing = fields.filter((field) => !payload[field]);
  if (missing.length > 0) {
    return `Missing required fields: ${missing.join(", ")}`;
  }
  return null;
};

const buildToken = ({ identity, name, room }) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
    throw new Error("LiveKit API credentials are not configured.");
  }

  const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
    identity,
    name,
    ttl: TOKEN_TTL,
  });

  token.addGrant({
    room,
    roomJoin: true,
  });

  return token.toJwt();
};

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.get("/token", (req, res) => {
  const { identity, name, room } = req.query;
  const error = ensureFields(req.query, ["identity", "room"]);
  if (error) {
    return res.status(400).json({ error });
  }

  try {
    const token = buildToken({ identity, name, room });
    return res.json({ token, ttl: TOKEN_TTL });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

app.post("/refresh", (req, res) => {
  const { identity, name, room } = req.body || {};
  const error = ensureFields(req.body || {}, ["identity", "room"]);
  if (error) {
    return res.status(400).json({ error });
  }

  try {
    const token = buildToken({ identity, name, room });
    return res.json({ token, ttl: TOKEN_TTL });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`LiveKit token server listening on port ${PORT}`);
});
