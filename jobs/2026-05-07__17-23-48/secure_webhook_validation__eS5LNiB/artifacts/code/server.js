const express = require('express');
const { WebhookReceiver } = require('livekit-server-sdk');
const fs = require('fs');
const path = require('path');

// Configuration
const PORT = process.env.PORT || 4000;
const WEBHOOK_SECRET = process.env.LIVEKIT_WEBHOOK_SECRET || 'your-webhook-secret';
const LOG_FILE = path.join(__dirname, 'events.log');

// Initialize Express app
const app = express();

// Initialize WebhookReceiver
const webhookReceiver = new WebhookReceiver(WEBHOOK_SECRET);

// Logging utility
function logEvent(eventData) {
  const timestamp = new Date().toISOString();
  const logEntry = JSON.stringify({
    timestamp,
    event: eventData
  }) + '\n';
  
  fs.appendFile(LOG_FILE, logEntry, (err) => {
    if (err) {
      console.error('Error writing to log file:', err);
    }
  });
}

// ============================================
// Event Handler Functions
// ============================================

function handleRoomStarted(event) {
  console.log(`[Room Started] Room: ${event.room.name}, ID: ${event.room.sid}`);
  logEvent({
    type: 'room_started',
    room: {
      sid: event.room.sid,
      name: event.room.name,
      creationTime: event.room.creationTime,
      numParticipants: event.room.numParticipants
    }
  });
}

function handleRoomFinished(event) {
  console.log(`[Room Finished] Room: ${event.room.name}, ID: ${event.room.sid}`);
  logEvent({
    type: 'room_finished',
    room: {
      sid: event.room.sid,
      name: event.room.name,
      creationTime: event.room.creationTime,
      numParticipants: event.room.numParticipants
    }
  });
}

function handleParticipantJoined(event) {
  console.log(`[Participant Joined] Room: ${event.room.name}, Participant: ${event.participant.identity}, ID: ${event.participant.sid}`);
  logEvent({
    type: 'participant_joined',
    room: {
      sid: event.room.sid,
      name: event.room.name
    },
    participant: {
      sid: event.participant.sid,
      identity: event.participant.identity,
      name: event.participant.name,
      state: event.participant.state,
      tracks: event.participant.tracks?.length || 0,
      metadata: event.participant.metadata
    }
  });
}

function handleParticipantLeft(event) {
  console.log(`[Participant Left] Room: ${event.room.name}, Participant: ${event.participant.identity}, ID: ${event.participant.sid}`);
  logEvent({
    type: 'participant_left',
    room: {
      sid: event.room.sid,
      name: event.room.name
    },
    participant: {
      sid: event.participant.sid,
      identity: event.participant.identity,
      name: event.participant.name,
      duration: event.participant.duration
    }
  });
}

function handleTrackPublished(event) {
  console.log(`[Track Published] Room: ${event.room.name}, Participant: ${event.participant.identity}, Track: ${event.track.sid}`);
  logEvent({
    type: 'track_published',
    room: {
      sid: event.room.sid,
      name: event.room.name
    },
    participant: {
      sid: event.participant.sid,
      identity: event.participant.identity
    },
    track: {
      sid: event.track.sid,
      type: event.track.type,
      name: event.track.name,
      source: event.track.source,
      mimeType: event.track.mimeType
    }
  });
}

function handleTrackUnpublished(event) {
  console.log(`[Track Unpublished] Room: ${event.room.name}, Participant: ${event.participant.identity}, Track: ${event.track.sid}`);
  logEvent({
    type: 'track_unpublished',
    room: {
      sid: event.room.sid,
      name: event.room.name
    },
    participant: {
      sid: event.participant.sid,
      identity: event.participant.identity
    },
    track: {
      sid: event.track.sid
    }
  });
}

function handleTrackSubscribed(event) {
  console.log(`[Track Subscribed] Room: ${event.room.name}, Subscriber: ${event.subscriber.identity}, Publisher: ${event.publisher.identity}`);
  logEvent({
    type: 'track_subscribed',
    room: {
      sid: event.room.sid,
      name: event.room.name
    },
    subscriber: {
      sid: event.subscriber.sid,
      identity: event.subscriber.identity
    },
    publisher: {
      sid: event.publisher.sid,
      identity: event.publisher.identity
    },
    track: {
      sid: event.track.sid,
      type: event.track.type
    }
  });
}

function handleTrackUnsubscribed(event) {
  console.log(`[Track Unsubscribed] Room: ${event.room.name}, Subscriber: ${event.subscriber.identity}, Publisher: ${event.publisher.identity}`);
  logEvent({
    type: 'track_unsubscribed',
    room: {
      sid: event.room.sid,
      name: event.room.name
    },
    subscriber: {
      sid: event.subscriber.sid,
      identity: event.subscriber.identity
    },
    publisher: {
      sid: event.publisher.sid,
      identity: event.publisher.identity
    },
    track: {
      sid: event.track.sid
    }
  });
}

function handleEgressStarted(event) {
  console.log(`[Egress Started] Room: ${event.egressInfo.roomName}, Egress ID: ${event.egressInfo.egressId}, Type: ${event.egressInfo.status}`);
  logEvent({
    type: 'egress_started',
    egressInfo: {
      egressId: event.egressInfo.egressId,
      roomName: event.egressInfo.roomName,
      status: event.egressInfo.status,
      startedAt: event.egressInfo.startedAt
    }
  });
}

function handleEgressEnded(event) {
  console.log(`[Egress Ended] Egress ID: ${event.egressInfo.egressId}, Status: ${event.egressInfo.status}, Error: ${event.egressInfo.error || 'None'}`);
  logEvent({
    type: 'egress_ended',
    egressInfo: {
      egressId: event.egressInfo.egressId,
      roomName: event.egressInfo.roomName,
      status: event.egressInfo.status,
      startedAt: event.egressInfo.startedAt,
      endedAt: event.egressInfo.endedAt,
      error: event.egressInfo.error
    }
  });
}

function handleEgressUpdated(event) {
  console.log(`[Egress Updated] Egress ID: ${event.egressInfo.egressId}, Status: ${event.egressInfo.status}`);
  logEvent({
    type: 'egress_updated',
    egressInfo: {
      egressId: event.egressInfo.egressId,
      roomName: event.egressInfo.roomName,
      status: event.egressInfo.status
    }
  });
}

function handleParticipantMetadataUpdated(event) {
  console.log(`[Participant Metadata Updated] Room: ${event.room.name}, Participant: ${event.participant.identity}`);
  logEvent({
    type: 'participant_metadata_updated',
    room: {
      sid: event.room.sid,
      name: event.room.name
    },
    participant: {
      sid: event.participant.sid,
      identity: event.participant.identity,
      metadata: event.participant.metadata
    }
  });
}

function handleRoomMetadataUpdated(event) {
  console.log(`[Room Metadata Updated] Room: ${event.room.name}`);
  logEvent({
    type: 'room_metadata_updated',
    room: {
      sid: event.room.sid,
      name: event.room.name,
      metadata: event.room.metadata
    }
  });
}

function handleUnknownEvent(event) {
  console.log(`[Unknown Event] Event: ${JSON.stringify(event)}`);
  logEvent({
    type: 'unknown_event',
    event: event
  });
}

// ============================================
// Event Router
// ============================================

function routeEvent(event) {
  if (!event || !event.event) {
    console.log('Invalid event structure');
    return;
  }

  switch (event.event) {
    case 'room_started':
      handleRoomStarted(event);
      break;
    case 'room_finished':
      handleRoomFinished(event);
      break;
    case 'participant_joined':
      handleParticipantJoined(event);
      break;
    case 'participant_left':
      handleParticipantLeft(event);
      break;
    case 'track_published':
      handleTrackPublished(event);
      break;
    case 'track_unpublished':
      handleTrackUnpublished(event);
      break;
    case 'track_subscribed':
      handleTrackSubscribed(event);
      break;
    case 'track_unsubscribed':
      handleTrackUnsubscribed(event);
      break;
    case 'egress_started':
      handleEgressStarted(event);
      break;
    case 'egress_ended':
      handleEgressEnded(event);
      break;
    case 'egress_updated':
      handleEgressUpdated(event);
      break;
    case 'participant_metadata_updated':
      handleParticipantMetadataUpdated(event);
      break;
    case 'room_metadata_updated':
      handleRoomMetadataUpdated(event);
      break;
    default:
      handleUnknownEvent(event);
      break;
  }
}

// ============================================
// Webhook Route
// ============================================

// IMPORTANT: Use express.raw() to preserve raw body for signature verification
// Do NOT use express.json() globally before this route
app.post('/webhook', express.raw({ type: 'application/webhook+json' }), async (req, res) => {
  try {
    // Get the raw body as string
    const body = req.body.toString('utf8');
    
    // Get the LiveKit signature from headers
    const authHeader = req.headers['livekit-webhook-authorization'] || req.headers['authorization'];
    
    if (!authHeader) {
      console.error('Missing authorization header');
      return res.status(401).json({ error: 'Missing authorization header' });
    }

    // Verify the webhook signature
    try {
      // WebhookReceiver.verify() expects the raw body and auth header
      // This validates the HMAC signature
      const isValid = await webhookReceiver.verify(body, authHeader);
      
      if (!isValid) {
        console.error('Invalid webhook signature');
        return res.status(401).json({ error: 'Invalid webhook signature' });
      }
    } catch (verifyError) {
      console.error('Webhook verification error:', verifyError.message);
      return res.status(401).json({ error: 'Webhook verification failed' });
    }

    // Parse the JSON body after verification
    const event = JSON.parse(body);
    console.log(`Received webhook event: ${event.event}`);

    // Route the event to the appropriate handler
    routeEvent(event);

    // Send success response
    res.status(200).json({ status: 'ok', event: event.event });
    
  } catch (error) {
    console.error('Error processing webhook:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================
// Health Check Route
// ============================================

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// ============================================
// Start Server
// ============================================

app.listen(PORT, () => {
  console.log(`LiveKit webhook server listening on port ${PORT}`);
  console.log(`Webhook endpoint: http://localhost:${PORT}/webhook`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`Events log: ${LOG_FILE}`);
  console.log(`Webhook secret: ${WEBHOOK_SECRET}`);
});