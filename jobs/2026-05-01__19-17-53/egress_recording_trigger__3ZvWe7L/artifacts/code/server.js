const express = require('express');
const { EgressClient, EncodedFileOutput, EncodedFileType } = require('livekit-server-sdk');

const app = express();
const port = 5000;

const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

if (!LIVEKIT_URL || !LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
  console.error('Missing LiveKit environment variables');
  process.exit(1);
}

const egressClient = new EgressClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

app.use(express.json());

// POST /start-recording
app.post('/start-recording', async (req, res) => {
  const { room, filepath } = req.body;

  if (!room || !filepath) {
    return res.status(400).json({ error: 'room and filepath are required' });
  }

  try {
    const info = await egressClient.startRoomCompositeEgress(room, {
      file: new EncodedFileOutput({
        fileType: EncodedFileType.MP4,
        filepath,
      }),
    });
    res.status(200).json({ egressId: info.egressId });
  } catch (error) {
    console.error('Error starting recording:', error);
    res.status(500).json({ error: error.message });
  }
});

// GET /egress/:egressId
app.get('/egress/:egressId', async (req, res) => {
  try {
    const list = await egressClient.listEgress({
      egressId: req.params.egressId,
    });

    if (list.length === 0) {
      return res.status(404).json({ error: 'Egress not found' });
    }

    res.status(200).json(list[0]);
  } catch (error) {
    console.error('Error fetching egress info:', error);
    res.status(500).json({ error: error.message });
  }
});

// POST /stop-recording/:egressId
app.post('/stop-recording/:egressId', async (req, res) => {
  try {
    await egressClient.stopEgress(req.params.egressId);
    res.status(200).json({ stopped: true });
  } catch (error) {
    console.error('Error stopping recording:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
