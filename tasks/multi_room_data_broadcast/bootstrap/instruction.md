# Build a Multi-Room Data Broadcast Script

Create a Python script `/home/user/livekit-broadcast/broadcast.py` that broadcasts a system message to all active LiveKit rooms.

## Requirements

The script should:

1. **Use `api.LiveKitAPI()` as an async context manager** (loads credentials from environment variables `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`).

2. **Call `lkapi.room.list_rooms(api.ListRoomsRequest())`** to retrieve all active rooms.

3. **For each room**, call:
   ```python
   await lkapi.room.send_data(api.SendDataRequest(
       room=room.name,
       data=json.dumps({
           "type": "system",
           "message": "Server maintenance in 5 minutes",
           "timestamp": datetime.utcnow().isoformat()
       }).encode(),
       kind=api.DataPacketKind.DATA_PACKET_KIND_RELIABLE,
   ))
   ```

4. **Log** `Broadcast sent to {room.name}` for each room successfully sent to, or `No active rooms found` if the room list is empty.

5. **Write all log lines** to `/home/user/livekit-broadcast/broadcast.log` (append mode).

## Project Structure

```
/home/user/livekit-broadcast/
├── broadcast.py
├── broadcast.log       # created on first run
└── .env.local          # already exists
```

## Notes

- Load environment variables from `.env.local` using `python-dotenv` or `os.environ`.
- The script should be runnable with `python3 broadcast.py`.
- Use `asyncio.run(main())` as the entry point.
- Import: `from livekit import api`
