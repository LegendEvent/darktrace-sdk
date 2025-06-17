#!/usr/bin/env python3
"""
Comprehensive example demonstrating how to use multiple Darktrace SDK modules together,
with a focus on threat intelligence integration.

This script:
1. Fetches threat intelligence from the Intel Feed
2. Checks for devices communicating with known threats
3. Retrieves model breaches related to those devices
4. Generates a threat intelligence report
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta, timezone
import urllib3
import requests
from typing import List, Dict, Any

# Add the parent directory to the path so we can import the darktrace module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from darktrace import DarktraceClient

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace these with your actual Darktrace instance and API credentials
DARKTRACE_HOST = "https://your-darktrace-instance"
PUBLIC_TOKEN = "your-public-token"
PRIVATE_TOKEN = "your-private-token"

# Configuration
THREAT_INTEL_SOURCE = "Threat Intel::Tor::Exit Node"  # Example source
DAYS_TO_CHECK = 7  # Number of days to look back for model breaches


def get_threat_intelligence(client: DarktraceClient) -> List[Dict[str, Any]]:
    """
    Fetch threat intelligence from the Intel Feed.
    
    Args:
        client: Initialized DarktraceClient
        
    Returns:
        List of threat intelligence entries
    """
    logger.info(f"Fetching threat intelligence from source: {THREAT_INTEL_SOURCE}")
    
    # This uses our fixed authentication with multiple query parameters
    entries = client.intelfeed.get(
        source=THREAT_INTEL_SOURCE,
        full_details=True
    )
    
    # Format entries into consistent structure
    threats = [
        {
            "name": entry.get("name", entry) if isinstance(entry, dict) else entry,
            "description": entry.get("description", "") if isinstance(entry, dict) else "",
            "expiry": entry.get("expiry", "") if isinstance(entry, dict) else "",
            "source": THREAT_INTEL_SOURCE
        }
        for entry in (entries or [])
    ]
    
    logger.info(f"Found {len(threats)} threat intelligence entries")
    return threats


def find_devices_communicating_with_threats(client: DarktraceClient, threats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Find devices communicating with known threats.
    
    Args:
        client: Initialized DarktraceClient
        threats: List of threat intelligence entries
        
    Returns:
        List of devices communicating with threats
    """
    logger.info("Searching for devices communicating with known threats")
    
    # Get all devices
    all_devices = client.devices.get()
    
    # This is a simplified example - in a real implementation, you would use
    # the advanced search module to find devices communicating with the threat IPs/domains
    # For demonstration purposes, we'll just return a subset of devices
    return all_devices[:5] if len(all_devices) > 5 else all_devices


def get_model_breaches_for_devices(client: DarktraceClient, devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get model breaches related to specific devices.
    
    Args:
        client: Initialized DarktraceClient
        devices: List of devices to check
        
    Returns:
        List of model breaches
    """
    logger.info("Fetching model breaches for devices of interest")
    
    # Calculate the start time (7 days ago)
    start_time = int((datetime.now(timezone.utc) - timedelta(days=DAYS_TO_CHECK)).timestamp() * 1000)
    
    # Get device IDs
    device_ids = [device.get("did") for device in devices if device.get("did")]
    
    if not device_ids:
        logger.info("No device IDs found")
        return []
    
    # Get model breaches for the devices
    # This demonstrates using multiple query parameters with the fixed authentication
    breaches = client.breaches.get(
        from_time=start_time,
        devices=",".join(str(did) for did in device_ids)
    )
    
    logger.info(f"Found {len(breaches)} model breaches for the devices of interest")
    return breaches


def generate_threat_report(threats: List[Dict[str, Any]], devices: List[Dict[str, Any]], breaches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a comprehensive threat intelligence report.
    
    Args:
        threats: List of threat intelligence entries
        devices: List of devices communicating with threats
        breaches: List of model breaches
        
    Returns:
        Report as a dictionary
    """
    logger.info("Generating threat intelligence report")
    
    # Create the report
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "threats_count": len(threats),
            "affected_devices_count": len(devices),
            "model_breaches_count": len(breaches)
        },
        "threats": threats[:10] if len(threats) > 10 else threats,  # Include only first 10 threats
        "affected_devices": [
            {
                "did": device.get("did"),
                "hostname": device.get("hostname"),
                "ip": device.get("ip")
            }
            for device in devices
        ],
        "model_breaches": [
            {
                "pid": breach.get("pid"),
                "time": breach.get("time"),
                "model": breach.get("model"),
                "score": breach.get("score"),
                "device": breach.get("device")
            }
            for breach in breaches[:10]  # Include only first 10 breaches
        ]
    }
    
    return report


def main():
    """Main function demonstrating multiple Darktrace SDK modules together."""
    # Initialize the Darktrace client
    client = DarktraceClient(
        host=DARKTRACE_HOST,
        public_token=PUBLIC_TOKEN,
        private_token=PRIVATE_TOKEN,
        debug=True  # Set to False in production
    )
    
    try:
        # Step 1: Get threat intelligence
        threats = get_threat_intelligence(client)
        
        # Step 2: Find devices communicating with threats
        devices = find_devices_communicating_with_threats(client, threats)
        
        # Step 3: Get model breaches for those devices
        breaches = get_model_breaches_for_devices(client, devices)
        
        # Step 4: Generate a threat report
        report = generate_threat_report(threats, devices, breaches)
        
        # Output the report
        logger.info("\nThreat Intelligence Report Summary:")
        logger.info(f"- Threats found: {report['summary']['threats_count']}")
        logger.info(f"- Affected devices: {report['summary']['affected_devices_count']}")
        logger.info(f"- Related model breaches: {report['summary']['model_breaches_count']}")
        
        # Save the report to a file
        output_file = "threat_intelligence_report.json"
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        logger.info(f"\nFull report saved to {output_file}")
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"\nHTTP Error: {e}")
        if hasattr(e.response, 'status_code'):
            logger.error(f"Response status: {e.response.status_code}")
        if hasattr(e.response, 'text'):
            logger.error(f"Response text: {e.response.text}")
        return 1
    except Exception as e:
        logger.error(f"\nError: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 