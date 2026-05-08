const express = require('express');
const { AccessToken, TokenVerifier } = require('livekit-server-sdk');

const app = express();
app.use(express.json());

const PORT = 3000;

// Use environment variables for API key and secret, or default values for development
const apiKey = process.env.LIVEKIT_API_KEY || 'devkey';
const apiSecret = process.env.LIVEKIT_API_SECRET || 'secret';

// GET /health - health check endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok' });
});

// GET /token - issue a new token
app.get('/token', async (req, res) => {
    try {
        const roomName = req.query.room || 'test-room';
        const participantName = req.query.identity || `user-${Math.floor(Math.random() * 10000)}`;

        const at = new AccessToken(apiKey, apiSecret, {
            identity: participantName,
            ttl: '30m',
        });

        at.addGrant({ roomJoin: true, room: roomName });

        const token = await at.toJwt();
        res.json({ token });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// POST /refresh - refresh an existing token
app.post('/refresh', async (req, res) => {
    try {
        let token = req.body.token;
        
        // Also support Authorization header: Bearer <token>
        if (!token && req.headers.authorization) {
            const parts = req.headers.authorization.split(' ');
            if (parts.length === 2 && parts[0] === 'Bearer') {
                token = parts[1];
            }
        }

        if (!token) {
            return res.status(400).json({ error: 'Token is required' });
        }

        const verifier = new TokenVerifier(apiKey, apiSecret);
        const claims = await verifier.verify(token);

        // Issue a new token with the same identity and claims, but renewed TTL
        const at = new AccessToken(apiKey, apiSecret, {
            identity: claims.sub,
            ttl: '30m',
            name: claims.name,
            metadata: claims.metadata,
            attributes: claims.attributes
        });

        // Copy over all grants
        if (claims.video) {
            at.addGrant(claims.video);
        }
        if (claims.sip) {
            at.addSIPGrant(claims.sip);
        }
        if (claims.inference) {
            at.addInferenceGrant(claims.inference);
        }
        if (claims.observability) {
            at.addObservabilityGrant(claims.observability);
        }
        if (claims.kind) {
            at.kind = claims.kind;
        }
        if (claims.sha256) {
            at.sha256 = claims.sha256;
        }
        if (claims.roomPreset) {
            at.roomPreset = claims.roomPreset;
        }
        if (claims.roomConfig) {
            at.roomConfig = claims.roomConfig;
        }

        const newToken = await at.toJwt();
        res.json({ token: newToken });
    } catch (e) {
        res.status(401).json({ error: 'Invalid token: ' + e.message });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
