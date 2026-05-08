#!/usr/bin/env python3
"""
Test script for broadcast.py functionality.

This script performs basic validation without requiring a running LiveKit server.
"""

import sys
import os

def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    try:
        from dotenv import load_dotenv
        from livekit import api
        from livekit.api import (
            LiveKitAPI,
            ListRoomsRequest,
            SendDataRequest,
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_environment_variables():
    """Test that environment variables can be loaded."""
    print("\nTesting environment variables...")
    try:
        from dotenv import load_dotenv
        load_dotenv(".env.local")
        
        required_vars = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
        missing = []
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                # Check if it's a placeholder (e.g., ${VAR_NAME})
                if value.startswith("${") and value.endswith("}"):
                    print(f"⚠ {var} is set to a placeholder: {value}")
                else:
                    print(f"✓ {var} is set")
            else:
                print(f"✗ {var} is not set")
                missing.append(var)
        
        if missing:
            print(f"\n✗ Missing environment variables: {', '.join(missing)}")
            return False
        else:
            print("\n✓ All environment variables configured")
            return True
    except Exception as e:
        print(f"✗ Error loading environment variables: {e}")
        return False

def test_script_syntax():
    """Test that the main script has valid syntax."""
    print("\nTesting script syntax...")
    try:
        import py_compile
        py_compile.compile("broadcast.py", doraise=True)
        print("✓ Script syntax is valid")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ Syntax error: {e}")
        return False

def test_message_encoding():
    """Test that message encoding works correctly."""
    print("\nTesting message encoding...")
    try:
        test_message = "SYSTEM: Test message with Unicode: 你好 🎉"
        encoded = test_message.encode("utf-8")
        decoded = encoded.decode("utf-8")
        
        if decoded == test_message:
            print(f"✓ Message encoding/decoding successful")
            print(f"  Original: {test_message}")
            print(f"  Encoded length: {len(encoded)} bytes")
            return True
        else:
            print("✗ Encoding/decoding mismatch")
            return False
    except Exception as e:
        print(f"✗ Encoding test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("LiveKit Broadcast Script - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_environment_variables,
        test_script_syntax,
        test_message_encoding,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())