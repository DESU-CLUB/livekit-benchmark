import { useState } from 'react';
import {
  LiveKitRoom,
  VideoConference,
  PreJoin,
} from '@livekit/components-react';
import '@livekit/components-styles';

const serverUrl = import.meta.env.VITE_SERVER_URL;
const tokenEndpoint = import.meta.env.VITE_TOKEN_SERVER_URL + '/token';

export default function App() {
  const [token, setToken] = useState(null);
  const [room, setRoom] = useState('quickstart-room');
  const [name, setName] = useState('User ' + Math.floor(Math.random() * 100));

  async function handleJoin(choices) {
    const resp = await fetch(`${tokenEndpoint}?room=${choices.roomName}&identity=${choices.username}`);
    const data = await resp.json();
    setToken(data.token);
    setRoom(choices.roomName);
    setName(choices.username);
  }

  if (!token) {
    return (
      <div className="prejoin-container" style={{ display: 'grid', placeItems: 'center', height: '100vh' }}>
        <PreJoin
          defaults={{
            roomName: room,
            username: name,
          }}
          onSubmit={handleJoin}
        />
      </div>
    );
  }

  return (
    <LiveKitRoom
      video={true}
      audio={true}
      token={token}
      serverUrl={serverUrl}
      onDisconnected={() => setToken(null)}
      style={{ height: '100vh' }}
    >
      <VideoConference />
    </LiveKitRoom>
  );
}
