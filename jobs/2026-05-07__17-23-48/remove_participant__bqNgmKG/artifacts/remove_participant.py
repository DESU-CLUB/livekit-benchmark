#!/usr/bin/env python3
"""
Script to remove a participant from a LiveKit room.
"""

import asyncio
import os
import sys
import livekit.api as api


async def remove_participant():
    """Remove a participant from a LiveKit room."""
    
    # Get credentials from environment
    livekit_url = os.getenv('LIVEKIT_URL')
    api_key = os.getenv('LIVEKIT_API_KEY')
    api_secret = os.getenv('LIVEKIT_API_SECRET')
    
    # Check if credentials are available
    if not all([livekit_url, api_key, api_secret]):
        error_msg = "Error: LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET must be set in environment variables"
        print(error_msg)
        with open('/home/user/livekit-admin/output.log', 'w') as f:
            f.write(error_msg + '\n')
        return
    
    # Target room and participant
    room_name = 'demo-room'
    participant_identity = 'user-123'
    
    try:
        # Create LiveKit API client
        async with api.LiveKitAPI(
            url=livekit_url,
            api_key=api_key,
            api_secret=api_secret
        ) as lkapi:
            
            # Remove the participant
            await lkapi.room.remove_participant(
                api.RoomParticipantIdentity(
                    room=room_name,
                    identity=participant_identity
                )
            )
            
            success_msg = f"Successfully removed participant '{participant_identity}' from room '{room_name}'"
            print(success_msg)
            
            # Write success message to log file
            with open('/home/user/livekit-admin/output.log', 'w') as f:
                f.write(success_msg + '\n')
                
    except api.twirp_client.TwirpError as e:
        # Handle LiveKit-specific errors (e.g., room or participant not found)
        error_msg = f"LiveKit API Error (code={e.code}): {e.message}"
        print(error_msg)
        
        with open('/home/user/livekit-admin/output.log', 'w') as f:
            f.write(error_msg + '\n')
            
    except Exception as e:
        # Handle any other exceptions
        error_msg = f"Unexpected error: {type(e).__name__}: {e}"
        print(error_msg)
        
        with open('/home/user/livekit-admin/output.log', 'w') as f:
            f.write(error_msg + '\n')


if __name__ == '__main__':
    asyncio.run(remove_participant())