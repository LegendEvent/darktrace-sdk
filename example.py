#!/usr/bin/env python3
"""
Simple example script for the Darktrace SDK
Shows how to connect and use basic functionality
"""

# Import the main client class
from darktrace import DarktraceClient

def main():
    """Example usage of the Darktrace SDK"""
    print("Darktrace SDK Example")
    print("--------------------")
    
    # Replace these with your actual credentials
    host = "https://your-darktrace-instance"
    public_token = "your_public_token"
    private_token = "your_private_token"
    
    # Initialize the client
    client = DarktraceClient(
        host=host, 
        public_token=public_token,
        private_token=private_token,
        debug=True  # Set to False in production
    )
    
    # Example 1: Get system status
    print("\nExample 1: Get system status")
    try:
        status = client.status.get()
        print(f"Connected to: {status.get('status', {}).get('instancename', 'Unknown')}")
        print(f"Version: {status.get('status', {}).get('version', 'Unknown')}")
    except Exception as e:
        print(f"Error getting status: {e}")
    
    # Example 2: Get recent devices
    print("\nExample 2: Get recent devices")
    try:
        # Get up to 10 devices
        devices = client.devices.get(count=10)
        print(f"Found {len(devices.get('devices', []))} devices")
        
        # Print info about the first few devices
        for device in devices.get('devices', [])[:3]:
            did = device.get('did', 'Unknown')
            hostname = device.get('hostname', 'Unknown')
            ip = device.get('ip', 'Unknown')
            print(f"Device ID: {did}, Hostname: {hostname}, IP: {ip}")
    except Exception as e:
        print(f"Error getting devices: {e}")
    
    # Example 3: Get recent model breaches
    print("\nExample 3: Get recent model breaches")
    try:
        # Get up to 10 model breaches
        breaches = client.breaches.get(count=10)
        print(f"Found {len(breaches.get('modelbreaches', []))} model breaches")
        
        # Print info about the first few breaches
        for breach in breaches.get('modelbreaches', [])[:3]:
            pbid = breach.get('pbid', 'Unknown')
            score = breach.get('score', 'Unknown')
            model_name = breach.get('model', {}).get('name', 'Unknown')
            print(f"Breach ID: {pbid}, Model: {model_name}, Score: {score}")
    except Exception as e:
        print(f"Error getting model breaches: {e}")
    
    # Example 4: Get Antigena actions
    print("\nExample 4: Get Antigena actions")
    try:
        # Get up to 10 actions
        actions = client.antigena.get_actions(count=10)
        print(f"Found {len(actions.get('actions', []))} Antigena actions")
        
        # Print info about the first few actions
        for action in actions.get('actions', [])[:3]:
            code_id = action.get('codeid', 'Unknown')
            action_type = action.get('action', 'Unknown')
            status = action.get('status', 'Unknown')
            print(f"Action ID: {code_id}, Type: {action_type}, Status: {status}")
    except Exception as e:
        print(f"Error getting Antigena actions: {e}")
    
    print("\nExample script completed!")

if __name__ == "__main__":
    main() 