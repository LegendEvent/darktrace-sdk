#!/usr/bin/env python3
"""
Test script for the Darktrace SDK
This script demonstrates the basic functionality of the Darktrace SDK
"""

from darktrace import DarktraceClient
import argparse
import sys

def test_connection(host, public_token, private_token, debug=False):
    """Test the connection to the Darktrace instance"""
    print(f"Testing connection to {host}...")
    try:
        # Initialize the client
        client = DarktraceClient(
            host=host,
            public_token=public_token,
            private_token=private_token,
            debug=debug
        )
        
        # Try to get status (simple endpoint that requires authentication)
        status = client.status.get()
        print(f"✅ Connection successful!")
        print(f"Instance info: {status.get('status', {}).get('instancename', 'Unknown')}")
        print(f"Version: {status.get('status', {}).get('version', 'Unknown')}")
        return True
    
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_devices(client, limit=5):
    """Test getting devices from Darktrace"""
    print("\nFetching devices...")
    try:
        devices = client.devices.get(count=limit)
        print(f"✅ Found {len(devices.get('devices', []))} devices")
        
        # Print some details about each device
        for i, device in enumerate(devices.get('devices', [])[:limit]):
            print(f"  [{i+1}] {device.get('hostname', 'Unknown')} (ID: {device.get('did', 'Unknown')})")
        return True
    
    except Exception as e:
        print(f"❌ Error fetching devices: {str(e)}")
        return False

def test_model_breaches(client, limit=5):
    """Test getting model breaches from Darktrace"""
    print("\nFetching model breaches...")
    try:
        breaches = client.breaches.get(count=limit)
        breach_count = len(breaches.get('modelbreaches', []))
        print(f"✅ Found {breach_count} model breaches")
        
        # Print some details about each breach
        for i, breach in enumerate(breaches.get('modelbreaches', [])[:limit]):
            model = breach.get('model', {})
            print(f"  [{i+1}] {model.get('name', 'Unknown')} - Score: {breach.get('score', 'Unknown')}")
        return True
    
    except Exception as e:
        print(f"❌ Error fetching model breaches: {str(e)}")
        return False

def test_antigena_actions(client, limit=5):
    """Test getting Antigena actions from Darktrace"""
    print("\nFetching Antigena actions...")
    try:
        actions = client.antigena.get_actions(count=limit)
        action_count = len(actions.get('actions', []))
        print(f"✅ Found {action_count} Antigena actions")
        
        # Print some details about each action
        for i, action in enumerate(actions.get('actions', [])[:limit]):
            print(f"  [{i+1}] {action.get('action', 'Unknown')} - Status: {action.get('status', 'Unknown')}")
        return True
    
    except Exception as e:
        print(f"❌ Error fetching Antigena actions: {str(e)}")
        return False

def main():
    """Main function to run the test script"""
    parser = argparse.ArgumentParser(description='Test the Darktrace SDK')
    parser.add_argument('--host', required=True, help='Darktrace instance URL (e.g., https://darktrace.example.com)')
    parser.add_argument('--public-token', required=True, help='Public API token')
    parser.add_argument('--private-token', required=True, help='Private API token')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Test the connection
    if not test_connection(args.host, args.public_token, args.private_token, args.debug):
        sys.exit(1)
    
    # Initialize the client for further tests
    client = DarktraceClient(
        host=args.host,
        public_token=args.public_token,
        private_token=args.private_token,
        debug=args.debug
    )
    
    # Run the tests
    test_devices(client)
    test_model_breaches(client)
    test_antigena_actions(client)
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    main() 