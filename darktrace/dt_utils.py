import base64
import json
from typing import Dict, Any, Optional, Tuple

def debug_print(message: str, debug: bool = False):
    if debug:
        print(f"DEBUG: {message}")

class BaseEndpoint:
    """Base class for all Darktrace API endpoint modules."""
    
    def __init__(self, client):
        self.client = client
    
    def _get_headers(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json_body: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, str], Optional[Dict[str, Any]]]:
        """
        Get authentication headers and sorted parameters for API requests.
        
        Args:
            endpoint: The API endpoint path
            params: Optional query parameters to include in the signature
            json_body: Optional JSON body for POST requests to include in signature
            
        Returns:
            Tuple containing:
            - Dict with the required authentication headers
            - Dict with sorted parameters (or None if no params)
        """
        result = self.client.auth.get_headers(endpoint, params, json_body)
        return result['headers'], result['params']

def encode_query(query: dict) -> str:
    query_json = json.dumps(query)
    return base64.b64encode(query_json.encode()).decode() 