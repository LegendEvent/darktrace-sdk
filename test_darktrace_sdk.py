#!/usr/bin/env python3
"""
Test script for the Darktrace SDK
This script demonstrates the basic functionality of the Darktrace SDK
"""

from darktrace import DarktraceClient
import argparse
import sys
import urllib3
import requests

def test_connection(host, public_token, private_token, debug=False, verify_ssl=True):
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
        
        # Set SSL verification for requests if needed
        if not verify_ssl:
            # This is a workaround since DarktraceClient doesn't have a verify_ssl parameter
            # We need to modify the session used by requests library
            urllib3.disable_warnings()
            
        # Try to get status (simple endpoint that requires authentication)
        status = client.status.get()
        print(f"✅ Connection successful!")
        print(f"Instance info: {status.get('status', {}).get('instancename', 'Unknown')}")
        print(f"Version: {status.get('status', {}).get('version', 'Unknown')}")
        return client
    
    except requests.RequestException as e:
        print(f"❌ Connection failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return None    
    
def test_devices(client, limit=5):
    """Test getting devices from Darktrace"""
    print("\nFetching devices...")
    try:
        # Using count parameter to demonstrate parameter handling
        devices = client.devices.get(count=limit)
        if isinstance(devices, dict):
            devices = devices.get('devices', [])
        print(f"✅ Found {len(devices)} devices")
        
        # Print some details about each device
        for i, device in enumerate(devices[:limit]):
            print(f"  [{i+1}] {device.get('hostname', 'Unknown')} (ID: {device.get('did', 'Unknown')})")
        return True
    
    except requests.RequestException as e:
        print(f"❌ Error fetching devices: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error fetching devices: {str(e)}")
        return False

def test_model_breaches(client, limit=5):
    """Test getting model breaches from Darktrace"""
    print("\nFetching model breaches...")
    try:
        # Using multiple parameters to test parameter ordering in authentication
        breaches = client.breaches.get(count=limit, full_details=True)
        breach_count = len(breaches.get('modelbreaches', []))
        print(f"✅ Found {breach_count} model breaches")
        
        # Print some details about each breach
        for i, breach in enumerate(breaches.get('modelbreaches', [])[:limit]):
            model = breach.get('model', {})
            print(f"  [{i+1}] {model.get('name', 'Unknown')} - Score: {breach.get('score', 'Unknown')}")
        return True
    
    except requests.RequestException as e:
        print(f"❌ Error fetching model breaches: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error fetching model breaches: {str(e)}")
        return False

def test_intel_feed(client):
    """Test the Intel Feed module with the fixed authentication mechanism"""
    print("\nTesting Intel Feed module...")
    try:
        # Get sources - tests the sources=true parameter
        sources = client.intelfeed.get_sources()
        print(f"✅ Found {len(sources)} Intel Feed sources")
        
        # Test basic get functionality
        print("Testing basic get functionality...")
        entries = client.intelfeed.get()
        print(f"✅ Found {len(entries)} Intel Feed entries")
        
        # Test get with full_details parameter
        print("Testing get with full_details parameter...")
        detailed_entries = client.intelfeed.get(full_details=True)
        print(f"✅ Found {len(detailed_entries)} detailed Intel Feed entries")
        
        # If there are sources, try to get entries from the first source
        if sources and len(sources) > 0:
            source = sources[0]
            print(f"Fetching entries from source '{source}'...")
            
            # Test source parameter
            source_entries = client.intelfeed.get(source=source)
            print(f"✅ Found {len(source_entries)} entries in source '{source}'")
            
            # Test multiple parameters together (source and full_details)
            print(f"Testing multiple parameters (source and full_details)...")
            detailed_source_entries = client.intelfeed.get(source=source, full_details=True)
            print(f"✅ Found {len(detailed_source_entries)} detailed entries in source '{source}'")
            
            # Print some details about a few entries
            for i, entry in enumerate(detailed_source_entries[:3]):
                if isinstance(entry, dict):
                    print(f"  [{i+1}] {entry.get('name', 'Unknown')} - {entry.get('description', 'No description')}")
                else:
                    print(f"  [{i+1}] {entry}")
        
        return True
    
    except requests.RequestException as e:
        print(f"❌ Error testing Intel Feed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error testing Intel Feed: {str(e)}")
        return False

def test_antigena_actions(client, limit=5):
    """Test getting Antigena actions from Darktrace"""
    print("\nFetching Antigena actions...")
    try:
        # Using multiple parameters to test parameter ordering in authentication
        actions = client.antigena.get_actions(count=limit, details=True)
        action_count = len(actions.get('actions', []))
        print(f"✅ Found {action_count} Antigena actions")
        
        # Print some details about each action
        for i, action in enumerate(actions.get('actions', [])[:limit]):
            print(f"  [{i+1}] {action.get('action', 'Unknown')} - Status: {action.get('status', 'Unknown')}")
        return True
    
    except requests.RequestException as e:
        print(f"❌ Error fetching Antigena actions: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
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
    parser.add_argument('--no-verify', action='store_true', help='Disable SSL verification')
    
    args = parser.parse_args()
    
    # Disable SSL warnings if requested
    if args.no_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Test the connection and get client
    client = test_connection(args.host, args.public_token, args.private_token, args.debug, not args.no_verify)
    if not client:
        sys.exit(1)
    
    # Run the tests
    test_devices(client)
    test_model_breaches(client)
    test_intel_feed(client)  # Added test for Intel Feed
    test_antigena_actions(client)
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    main() 