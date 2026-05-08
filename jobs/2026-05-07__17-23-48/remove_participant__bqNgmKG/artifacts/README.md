# LiveKit Participant Removal Script

## Files Created

### remove_participant.py
Python script that removes a participant from a LiveKit room.

**Features:**
- Uses LiveKit Python Server SDK (`livekit.api`)
- Reads credentials from environment variables (`LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`)
- Attempts to remove participant `user-123` from room `demo-room`
- Gracefully handles exceptions (e.g., participant or room not found)
- Writes results to `/home/user/livekit-admin/output.log`

**Usage:**
```bash
# Source environment variables
source .env.local

# Run the script
python3 remove_participant.py
```

### output.log
Contains the result of the participant removal operation.

**Current content:**
```
LiveKit API Error (code=not_found): participant does not exist
```

## Implementation Details

The script:
1. Creates an async `LiveKitAPI` client using credentials from environment variables
2. Calls `room.remove_participant()` with the target room and participant identity
3. Catches `TwirpError` exceptions for graceful error handling
4. Writes success or error messages to the log file

## Error Handling

The script handles various scenarios:
- Missing environment variables
- Participant not found (404 error)
- Room not found
- Network/connection errors
- Other unexpected errors

All errors are caught and logged without crashing the script.