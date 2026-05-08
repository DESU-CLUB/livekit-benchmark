#!/usr/bin/env python3
"""
Example usage scripts for broadcast.py

This file contains various examples of how to use the broadcast script
in different scenarios.
"""

import subprocess
import sys


def example_default_message():
    """Example 1: Broadcast default maintenance message."""
    print("Example 1: Broadcasting default maintenance message")
    print("Command: python3 broadcast.py")
    print("-" * 60)
    # In production, you would run:
    # subprocess.run(["python3", "broadcast.py"])


def example_custom_maintenance():
    """Example 2: Broadcast custom maintenance warning."""
    print("Example 2: Broadcasting custom maintenance warning")
    print('Command: python3 broadcast.py "SYSTEM: Server restart in 10 minutes"')
    print("-" * 60)
    # In production, you would run:
    # subprocess.run(["python3", "broadcast.py", "SYSTEM: Server restart in 10 minutes"])


def example_emergency():
    """Example 3: Broadcast emergency notification."""
    print("Example 3: Broadcasting emergency notification")
    print('Command: python3 broadcast.py "EMERGENCY: Immediate evacuation required"')
    print("-" * 60)
    # In production, you would run:
    # subprocess.run(["python3", "broadcast.py", "EMERGENCY: Immediate evacuation required"])


def example_feature_update():
    """Example 4: Broadcast feature update announcement."""
    print("Example 4: Broadcasting feature update announcement")
    print('Command: python3 broadcast.py "NEW: Screen sharing feature is now available!"')
    print("-" * 60)
    # In production, you would run:
    # subprocess.run(["python3", "broadcast.py", "NEW: Screen sharing feature is now available!"])


def example_long_message():
    """Example 5: Broadcast long multi-part message."""
    print("Example 5: Broadcasting long message")
    print('Command: python3 broadcast.py "IMPORTANT: Please be aware that scheduled system maintenance will begin at 2:00 AM UTC. All active sessions will be terminated. We recommend saving your work before this time. Thank you for your cooperation."')
    print("-" * 60)
    # In production, you would run:
    # message = "IMPORTANT: Please be aware that scheduled system maintenance will begin at 2:00 AM UTC. All active sessions will be terminated. We recommend saving your work before this time. Thank you for your cooperation."
    # subprocess.run(["python3", "broadcast.py", message])


def example_unicode_message():
    """Example 6: Broadcast message with Unicode characters."""
    print("Example 6: Broadcasting message with Unicode characters")
    print('Command: python3 broadcast.py "SYSTEM: 系统维护将在30分钟后开始 请保存您的工作 🚀"')
    print("-" * 60)
    # In production, you would run:
    # subprocess.run(["python3", "broadcast.py", "SYSTEM: 系统维护将在30分钟后开始 请保存您的工作 🚀"])


def example_programmatic_usage():
    """Example 7: Using broadcast from Python code."""
    print("Example 7: Programmatic usage from Python code")
    print("-" * 60)
    print("```python")
    print("import subprocess")
    print("")
    print("# Broadcast a message to all active rooms")
    print("message = 'SYSTEM: Custom notification message'")
    print("result = subprocess.run(")
    print("    ['python3', 'broadcast.py', message],")
    print("    capture_output=True,")
    print("    text=True")
    print(")")
    print("")
    print("# Check if broadcast was successful")
    print("if result.returncode == 0:")
    print("    print('Broadcast successful')")
    print("else:")
    print("    print(f'Broadcast failed: {result.stderr}')")
    print("```")
    print("-" * 60)


def example_cron_job():
    """Example 8: Setting up a cron job for scheduled broadcasts."""
    print("Example 8: Cron job for scheduled daily maintenance reminder")
    print("-" * 60)
    print("# Add to crontab with: crontab -e")
    print("# Broadcast daily at 8:00 AM")
    print("0 8 * * * cd /home/user/livekit-broadcast && python3 broadcast.py 'SYSTEM: Daily maintenance check at 8:00 AM' >> broadcast.log 2>&1")
    print("")
    print("# Broadcast every 6 hours")
    print("0 */6 * * * cd /home/user/livekit-broadcast && python3 broadcast.py 'SYSTEM: Scheduled system check' >> broadcast.log 2>&1")
    print("-" * 60)


def main():
    """Run all examples."""
    print("=" * 60)
    print("LiveKit Broadcast Script - Usage Examples")
    print("=" * 60)
    print()
    
    examples = [
        example_default_message,
        example_custom_maintenance,
        example_emergency,
        example_feature_update,
        example_long_message,
        example_unicode_message,
        example_programmatic_usage,
        example_cron_job,
    ]
    
    for i, example in enumerate(examples, 1):
        print()
        example()
        print()
    
    print("=" * 60)
    print("Note: These are examples. Uncomment the subprocess.run()")
    print("calls to execute them in a real environment.")
    print("=" * 60)


if __name__ == "__main__":
    main()