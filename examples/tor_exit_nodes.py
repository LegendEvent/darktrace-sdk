#!/usr/bin/env python3
"""
Example script demonstrating how to fetch Tor exit nodes from the Darktrace Intel Feed.
This script shows how to use the fixed authentication mechanism with the source and full_details parameters.
"""

import os
import sys
import json
from datetime import datetime, timezone
import urllib3

# Add the parent directory to the path so we can import the darktrace module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from darktrace import DarktraceClient

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    # Configuration
    # Replace these with your actual Darktrace instance and API credentials
    host = "https://your-darktrace-instance"
    public_token = "your-public-token"
    private_token = "your-private-token"

    # Initialize the Darktrace client
    client = DarktraceClient(
        host=host,
        public_token=public_token,
        private_token=private_token,
        debug=True  # Set to False in production
    )

    try:
        print("Fetching Tor exit nodes from intel feed...")
        # This demonstrates the fixed authentication with both source and full_details parameters
        entries = client.intelfeed.get(
            source="Threat Intel::Tor::Exit Node",
            full_details=True
        )

        # Format entries into consistent structure
        nodes = [
            {
                "name": entry.get("name", entry) if isinstance(entry, dict) else entry,
                "description": entry.get("description", "") if isinstance(entry, dict) else "",
                "expiry": entry.get("expiry", "") if isinstance(entry, dict) else "",
                "source": "Threat Intel::Tor::Exit Node"
            }
            for entry in (entries or [])
        ]

        # Create result JSON
        result = {
            "total_nodes": len(nodes),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "nodes": nodes
        }
        
        print(f"\nFound {len(nodes)} Tor exit nodes")
        print("\nSample of nodes (first 5):")
        print(json.dumps(nodes[:5], indent=2))
        print(f"\nTotal nodes: {len(nodes)}")

        # Save the result to a file
        output_file = "tor_exit_nodes.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nFull results saved to {output_file}")

    except Exception as e:
        print(f"\nError accessing Darktrace API: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 