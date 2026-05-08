import { useState } from 'react';
import {
  LiveKitRoom,
  VideoConference,
  RoomAudioRenderer,
} from '@livekit/components-react';
import '@livekit/components-styles';
import './App.css';

function App() {
  const [room, setRoom] = useState('');
  const [identity, setIdentity] = useState('');
  const [token, setToken] = useState('');

  const serverUrl = import.meta.env.VITE_SERVER_URL || 'ws://localhost:7880';

  const joinRoom = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:3001/token?room=${room}&identity=${identity}`);
      const data = await response.json();
      setToken(data.token);
    } catch (error) {
      console.error('Error fetching token:', error);
    }
  };

  if (token === '') {
    return (
      <div className="join-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <h2>Join Video Conference</h2>
        <form onSubmit={joinRoom} style={{ display: 'flex', flexDirection: 'column', gap: '10px', width: '300px' }}>
          <input
            type="text"
            placeholder="Room Name"
            value={room}
            onChange={(e) => setRoom(e.target.value)}
            required
            style={{ padding: '10px', fontSize: '16px' }}
          />
          <input
            type="text"
            placeholder="Your Name"
            value={identity}
            onChange={(e) => setIdentity(e.target.value)}
            required
            style={{ padding: '10px', fontSize: '16px' }}
          />
          <button type="submit" style={{ padding: '10px', fontSize: '16px', cursor: 'pointer' }}>Join Room</button>
        </form>
      </div>
    );
  }

  return (
    <LiveKitRoom
      video={true}
      audio={true}
      token={token}
      serverUrl={serverUrl}
      data-lk-theme="default"
      style={{ height: '100vh' }}
      onDisconnected={() => setToken('')}
    >
      <VideoConference />
      <RoomAudioRenderer />
    </LiveKitRoom>
  );
}

export default App;
