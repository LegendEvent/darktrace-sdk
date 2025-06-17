#!/usr/bin/env python3
"""
Example script demonstrating how to use the Darktrace Intel Feed module.
This script shows how to retrieve and manage watched domains in Darktrace.
"""

import os
import sys
import logging
from pprint import pprint

# Add the parent directory to the path so we can import the darktrace module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from darktrace import DarktraceClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace these with your actual Darktrace instance and API credentials
DARKTRACE_HOST = "https://your-darktrace-instance"
PUBLIC_TOKEN = "your-public-token"
PRIVATE_TOKEN = "your-private-token"

def main():
    """Main function demonstrating Intel Feed module usage."""
    # Initialize the Darktrace client
    client = DarktraceClient(
        host=DARKTRACE_HOST,
        public_token=PUBLIC_TOKEN,
        private_token=PRIVATE_TOKEN,
        debug=True  # Set to False in production
    )
    
    try:
        # Example 1: Get list of sources
        logger.info("Getting list of sources...")
        logger.info("This demonstrates the fixed authentication with sources=true parameter")
        sources = client.intelfeed.get_sources()
        logger.info("Available sources:")
        pprint(sources)
        
        # Example 2: Get all watched domains
        logger.info("\nGetting all watched domains...")
        domains = client.intelfeed.get()
        logger.info(f"Found {len(domains)} domains:")
        pprint(domains[:10] if len(domains) > 10 else domains)  # Show only first 10 if there are many
        
        # Example 3: Get detailed information about watched domains
        logger.info("\nGetting detailed information about watched domains...")
        logger.info("This demonstrates the fixed authentication with fulldetails=true parameter")
        detailed_domains = client.intelfeed.get_with_details()
        logger.info("Detailed domains:")
        pprint(detailed_domains[:5] if len(detailed_domains) > 5 else detailed_domains)  # Show only first 5
        
        # Example 4: Add a domain (uncomment to test)
        """
        logger.info("\nAdding a new domain...")
        result = client.intelfeed.update(
            add_entry="example-threat.com",
            description="Test domain added via API",
            source="API_Test"
        )
        logger.info("Add domain result:")
        pprint(result)
        """
        
        # Example 5: If a specific source exists, get domains from that source
        if sources and len(sources) > 0:
            source = sources[0]  # Use the first source as an example
            logger.info(f"\nGetting domains from source '{source}'...")
            logger.info("This demonstrates the fixed authentication with source parameter")
            source_domains = client.intelfeed.get_by_source(source)
            logger.info(f"Domains from source '{source}':")
            pprint(source_domains[:10] if len(source_domains) > 10 else source_domains)
        
        # Example 6: Demonstrate how the authentication includes query parameters in the signature
        logger.info("\nDemonstrating authentication with multiple query parameters...")
        logger.info("This demonstrates the fixed authentication with multiple parameters")
        logger.info("Using source and fulldetails parameters together")
        
        if sources and len(sources) > 0:
            source = sources[0]  # Use the first source as an example
            detailed_source_domains = client.intelfeed.get(source=source, full_details=True)
            logger.info(f"Detailed domains from source '{source}':")
            pprint(detailed_source_domains[:5] if len(detailed_source_domains) > 5 else detailed_source_domains)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 