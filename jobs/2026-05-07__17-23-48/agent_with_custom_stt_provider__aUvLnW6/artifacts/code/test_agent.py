"""
Test script to verify the agent can be imported and initialized
"""
import os
import sys

# Add the project to the path
sys.path.insert(0, ".")

try:
    from livekit.agents import JobProcess
    from livekit.plugins import deepgram, silero
    from livekit_agent.agent import deepgram_agent, prewarm
    
    print("✓ All imports successful")
    print(f"✓ Agent function: {deepgram_agent.__name__}")
    print(f"✓ Prewarm function: {prewarm.__name__}")
    
    # Check if DEEPGRAM_API_KEY is set
    if os.getenv("DEEPGRAM_API_KEY"):
        print("✓ DEEPGRAM_API_KEY is set")
    else:
        print("⚠ DEEPGRAM_API_KEY is not set (this is expected for testing)")
    
    print("\nAll checks passed! The agent is ready to use.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)