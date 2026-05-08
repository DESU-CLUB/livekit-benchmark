# LiveKit Room Broadcast Script

This script broadcasts system messages to all active LiveKit rooms using the Room Service `send_data` API.

## Features

- Lists all active LiveKit rooms
- Broadcasts messages to each room with reliable delivery (DATA_PACKET_KIND_RELIABLE)
- Comprehensive logging to both file and console
- Error handling and status reporting
- Support for custom messages via command line arguments

## Prerequisites

- Python 3.7+
- `livekit-server-sdk` (Python) - already installed
- LiveKit server credentials configured in `.env.local`

## Configuration

The script reads the following environment variables from `.env.local`:

- `LIVEKIT_URL`: LiveKit server URL (e.g., `http://localhost:7880`)
- `LIVEKIT_API_KEY`: LiveKit API key
- `LIVEKIT_API_SECRET`: LiveKit API secret

## Usage

### Basic Usage (Default Message)

Run the script with the default system message:

```bash
python3 broadcast.py
```

Default message: `SYSTEM: Scheduled maintenance will begin in 30 minutes. Please save your work.`

### Custom Message

Provide a custom message as command line arguments:

```bash
python3 broadcast.py "Your custom message here"
```

### Examples

```bash
# Broadcast maintenance warning
python3 broadcast.py "SYSTEM: Server maintenance in 15 minutes"

# Broadcast emergency notification
python3 broadcast.py "EMERGENCY: All users must disconnect immediately"

# Broadcast with multiple words
python3 broadcast.py "IMPORTANT: Please save your work before logging out"
```

## Output

The script logs all activities to:

- **Console**: Real-time output
- **File**: `broadcast.log` (persistent log file)

Log format: `%(asctime)s - %(levelname)s - %(message)s`

### Sample Log Output

```
2026-05-08 00:33:03,123 - INFO - Successfully initialized LiveKit API client for URL: http://localhost:7880
2026-05-08 00:33:03,124 - INFO - Fetching list of active rooms...
2026-05-08 00:33:03,156 - INFO - Found 2 active room(s): ['room-1', 'room-2']
2026-05-08 00:33:03,157 - INFO - Broadcasting message to room 'room-1': SYSTEM: Scheduled maintenance will begin in 30 minutes. Please save your work.
2026-05-08 00:33:03,189 - INFO - Successfully broadcast message to room 'room-1'
2026-05-08 00:33:03,190 - INFO - Broadcasting message to room 'room-2': SYSTEM: Scheduled maintenance will begin in 30 minutes. Please save your work.
2026-05-08 00:33:03,221 - INFO - Successfully broadcast message to room 'room-2'
2026-05-08 00:33:03,222 - INFO - Broadcast completed. Success: 2/2, Failed: 0/2
2026-05-08 00:33:03,223 - INFO - LiveKit API client closed.
2026-05-08 00:33:03,223 - INFO - Broadcast completed successfully
```

## Exit Codes

- `0`: All broadcasts successful
- `1`: One or more broadcasts failed

## Error Handling

The script handles various error scenarios:

- Missing environment variables
- Failed API client initialization
- Network connectivity issues
- Invalid room names
- API authentication failures

All errors are logged with descriptive messages.

## Implementation Details

### API Methods Used

1. **List Rooms**: `client.room.list_rooms(ListRoomsRequest())`
   - Retrieves all active rooms

2. **Send Data**: `client.room.send_data(SendDataRequest(...))`
   - Sends binary payload to specified room
   - Uses `kind=0` (RELIABLE) for guaranteed delivery

### Data Flow

```
1. Load environment variables
2. Initialize LiveKit API client
3. List all active rooms
4. For each room:
   - Encode message to UTF-8 bytes
   - Send data with reliable delivery
   - Log success/failure
5. Close client connection
6. Return summary statistics
```

## Testing

To test the script without a LiveKit server:

```bash
# Verify imports work
python3 -c "from livekit import api; print('SDK OK')"

# Check syntax
python3 -m py_compile broadcast.py
```

## Troubleshooting

### Connection Issues

- Verify `LIVEKIT_URL` is correct and accessible
- Check firewall rules
- Ensure LiveKit server is running

### Authentication Issues

- Verify `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` are correct
- Check that the API key has room service permissions

### No Rooms Found

- Ensure there are active rooms in the LiveKit server
- Check room visibility settings

## License

This script is provided as-is for LiveKit server-side applications.