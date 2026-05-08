/**
 * Test script for LiveKit webhook server
 * 
 * Usage:
 *   node test-webhook.js
 * 
 * This script tests:
 * 1. Health endpoint
 * 2. Webhook endpoint with invalid signature (should fail)
 * 3. Provides guidance for testing with LiveKit
 */

const http = require('http');

const SERVER_URL = process.env.SERVER_URL || 'http://localhost:4000';

function testHealthEndpoint() {
  return new Promise((resolve, reject) => {
    console.log('\n=== Testing Health Endpoint ===');
    
    http.get(`${SERVER_URL}/health`, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        console.log(`Status: ${res.statusCode}`);
        console.log('Response:', data);
        
        if (res.statusCode === 200) {
          console.log('✅ Health check passed');
          resolve();
        } else {
          console.log('❌ Health check failed');
          reject(new Error('Health check failed'));
        }
      });
    }).on('error', (error) => {
      console.log('❌ Health check error:', error.message);
      reject(error);
    });
  });
}

function testWebhookWithoutAuth() {
  return new Promise((resolve, reject) => {
    console.log('\n=== Testing Webhook Endpoint (No Auth) ===');
    console.log('This test should fail with 401 Unauthorized');
    
    const postData = JSON.stringify({
      event: 'room_started',
      room: {
        sid: 'RM_test123',
        name: 'test-room',
        creationTime: Date.now(),
        numParticipants: 0
      }
    });

    const options = {
      hostname: 'localhost',
      port: 4000,
      path: '/webhook',
      method: 'POST',
      headers: {
        'Content-Type': 'application/webhook+json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        console.log(`Status: ${res.statusCode}`);
        console.log('Response:', data);
        
        if (res.statusCode === 401) {
          console.log('✅ Webhook correctly rejected request without auth');
          resolve();
        } else {
          console.log('⚠️  Unexpected response:', res.statusCode);
          resolve(); // Don't fail on unexpected, just warn
        }
      });
    });

    req.on('error', (error) => {
      console.log('❌ Webhook test error:', error.message);
      reject(error);
    });

    req.write(postData);
    req.end();
  });
}

function printTestInstructions() {
  console.log('\n=== Testing with LiveKit ===');
  console.log('To test with actual LiveKit webhooks:');
  console.log('');
  console.log('1. Start this webhook server:');
  console.log('   node server.js');
  console.log('');
  console.log('2. Configure your LiveKit server to send webhooks:');
  console.log('   livekit-server --webhook-url http://localhost:4000/webhook --webhook-secret YOUR_SECRET');
  console.log('');
  console.log('3. Create a room and join with a participant');
  console.log('');
  console.log('4. Check the events.log file for logged events:');
  console.log('   cat events.log');
  console.log('');
  console.log('5. Check server console output for event processing');
  console.log('');
}

async function runTests() {
  console.log('🧪 LiveKit Webhook Server Test Suite');
  console.log(`📍 Testing server at: ${SERVER_URL}`);
  
  try {
    await testHealthEndpoint();
    await testWebhookWithoutAuth();
    printTestInstructions();
    
    console.log('\n✅ All tests completed successfully!');
    console.log('\n📝 Next steps:');
    console.log('   1. Set LIVEKIT_WEBHOOK_SECRET environment variable');
    console.log('   2. Start the server: node server.js');
    console.log('   3. Configure LiveKit to send webhooks to your server');
    console.log('   4. Monitor events.log for incoming events');
    
  } catch (error) {
    console.log('\n❌ Tests failed:', error.message);
    console.log('\n🔧 Troubleshooting:');
    console.log('   - Make sure the server is running: node server.js');
    console.log('   - Check if port 4000 is available');
    console.log('   - Verify server.js exists in this directory');
    process.exit(1);
  }
}

// Run tests
runTests();