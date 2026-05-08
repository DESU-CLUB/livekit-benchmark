# LiveKit Permission Update Script

## Overview
This script updates a participant's permissions in a LiveKit room using the Python Server SDK.

## Script Details
- **File**: `update_permissions.py`
- **Location**: `/home/user/livekit-admin/update_permissions.py`
- **Purpose**: Dynamically update participant permissions for a connected user

## Implementation

### Requirements Met
✅ Imports `asyncio`, `api` from `livekit`, and `ParticipantPermission` from `livekit.protocol.models`
✅ Defines an `async def main()` function
✅ Uses `async with api.LiveKitAPI() as lkapi:` to create an authenticated API client
✅ Calls `lkapi.room.update_participant()` with the required parameters:
   - Room: `stage-room`
   - Identity: `speaker-1`
   - Permission: `ParticipantPermission(can_publish=True, can_subscribe=True, can_publish_data=True)`
✅ Writes to `output.log` in append mode after the API call
✅ Prints "Permissions updated" to stdout

### Usage
```bash
source .env.local
python3 update_permissions.py
```

### Environment Variables Required
- `LIVEKIT_API_KEY`: Your LiveKit API key
- `LIVEKIT_API_SECRET`: Your LiveKit API secret
- `LIVEKIT_URL`: Your LiveKit server URL

### Code Structure
```python
import asyncio
from livekit import api
from livekit.protocol.models import ParticipantPermission


async def main():
    async with api.LiveKitAPI() as lkapi:
        await lkapi.room.update_participant(
            api.UpdateParticipantRequest(
                room="stage-room",
                identity="speaker-1",
                permission=ParticipantPermission(
                    can_publish=True,
                    can_subscribe=True,
                    can_publish_data=True
                )
            )
        )
    
    with open("output.log", "a") as f:
        f.write("Permissions updated\n")
    
    print("Permissions updated")


if __name__ == "__main__":
    asyncio.run(main())
```

## Note
The script was tested with test credentials. In a production environment, you would need:
- Valid LiveKit server credentials
- An actual room named "stage-room"
- A participant with identity "speaker-1" connected to that room