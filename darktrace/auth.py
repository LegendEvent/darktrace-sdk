import hmac
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Optional, Any

class DarktraceAuth:
    def __init__(self, public_token: str, private_token: str):
        self.public_token = public_token
        self.private_token = private_token

    def get_headers(self, request_path: str, params: Optional[Dict[str, Any]] = None, json_body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:    
        """
        Generate authentication headers and sorted parameters for Darktrace API requests.
        
        Args:
            request_path: The API endpoint path
            params: Optional query parameters to include in the signature
            json_body: Optional JSON body for POST requests to include in signature
            
        Returns:
            Dict containing:
            - 'headers': The required authentication headers
            - 'params': The sorted parameters (or original params if none)
        """
        date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        # Include query parameters in the signature if provided
        signature_path = request_path
        sorted_params = None
        
        if params and len(params) > 0:
            # Sort parameters alphabetically by key as required by Darktrace API
            sorted_params = dict(sorted(params.items()))
            query_string = '&'.join(f"{k}={v}" for k, v in sorted_params.items())
            signature_path = f"{request_path}?{query_string}"
          # For POST requests with JSON body, include the body as a query string parameter
        # as per Darktrace docs: "add each post parameter into the query string as /postendpoint?{"param1":"value","param2":"value"}"
        # NOTE: This implementation is currently not working for Advanced Search POST requests.
        # Multiple attempts following the official documentation result in "API SIGNATURE ERROR".
        # GET requests work correctly with this authentication method.
        if json_body:
            json_string = json.dumps(json_body, separators=(',', ':'))  # Compact JSON without spaces
            separator = '&' if '?' in signature_path else '?'
            signature_path = f"{signature_path}{separator}{json_string}"
        
        signature = self.generate_signature(signature_path, date)
        
        return {
            'headers': {
            'DTAPI-Token': self.public_token,
            'DTAPI-Date': date,
            'DTAPI-Signature': signature,
            'Content-Type': 'application/json',
            },
            'params': sorted_params or params
        }

    def generate_signature(self, request_path: str, date: str) -> str:
        """
        Generate the HMAC signature for Darktrace API authentication.
        
        Args:
            request_path: The API endpoint path (including query parameters if any)
            date: The formatted date string
            
        Returns:
            The HMAC-SHA1 signature as a hexadecimal string
        """
        message = f"{request_path}\n{self.public_token}\n{date}"
        signature = hmac.new(
            self.private_token.encode('ASCII'),
            message.encode('ASCII'),
            hashlib.sha1
        ).hexdigest()
        return signature 