import { useState } from 'react';
import {
  LiveKitRoom,
  VideoConference,
  useToken,
  formatChatMessageLinks,
  useTracks,
  Track,
} from '@livekit/components-react';
import { RoomEvent } from 'livekit-client';
import './App.css';

function App() {
  const [roomName, setRoomName] = useState('');
  const [userName, setUserName] = useState('');
  const [hasJoined, setHasJoined] = useState(false);

  // Token provider function
  const tokenProvider = async () => {
    if (!roomName || !userName) {
      throw new Error('Room name and user name are required');
    }

    const response = await fetch(
      `${import.meta.env.VITE_SERVER_URL || 'http://localhost:3001'}/token?room=${encodeURIComponent(roomName)}&identity=${encodeURIComponent(userName)}`
    );

    if (!response.ok) {
      throw new Error('Failed to get token');
    }

    const data = await response.json();
    return data.token;
  };

  const handleJoin = (e) => {
    e.preventDefault();
    if (roomName.trim() && userName.trim()) {
      setHasJoined(true);
    }
  };

  const handleLeave = () => {
    setHasJoined(false);
    setRoomName('');
    setUserName('');
  };

  if (hasJoined) {
    return (
      <div className="container">
        <div className="room-header">
          <h1>LiveKit Meet</h1>
          <p>Room: {roomName} | User: {userName}</p>
          <button onClick={handleLeave} className="leave-button">
            Leave Room
          </button>
        </div>
        
        <LiveKitRoom
          token={tokenProvider}
          serverUrl={import.meta.env.VITE_SERVER_URL || 'http://localhost:3001'}
          onDisconnected={handleLeave}
          connectOptions={{
            autoSubscribe: true,
          }}
        >
          <VideoConference />
        </LiveKitRoom>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="join-form">
        <h1>LiveKit Meet</h1>
        <p>Enter your name and room to join a video conference</p>
        
        <form onSubmit={handleJoin}>
          <div className="form-group">
            <label htmlFor="userName">Your Name</label>
            <input
              type="text"
              id="userName"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              placeholder="Enter your name"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="roomName">Room Name</label>
            <input
              type="text"
              id="roomName"
              value={roomName}
              onChange={(e) => setRoomName(e.target.value)}
              placeholder="Enter room name"
              required
            />
          </div>
          
          <button type="submit" className="join-button">
            Join Room
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;