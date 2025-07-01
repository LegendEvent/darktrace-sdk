import requests
import json
from typing import Dict, Any
from .dt_utils import debug_print, BaseEndpoint, encode_query

class AdvancedSearch(BaseEndpoint):    
    def __init__(self, client):
        super().__init__(client)

    def search(self, query: Dict[str, Any], post_request: bool = False):
        """Perform Advanced Search query.
        
        Parameters:
            query: Dictionary containing the search query parameters
            post_request: If True, use POST method (6.1+), otherwise GET method
            
        Returns:
            dict: Search results from Darktrace Advanced Search API
        """
        endpoint = '/advancedsearch/api/search'
        
        if post_request:
            # For POST requests (6.1+), we need to create the full Advanced Search structure
            # and encode it as base64, then send it as {"hash": "encoded_string"}
            
            # Build the complete Advanced Search query structure
            full_query = {
                "search": query.get("search", ""),
                "fields": query.get("fields", []),
                "offset": query.get("offset", 0),
                "timeframe": query.get("timeframe", "3600"),  # Default 1 hour
                "time": query.get("time", {"user_interval": 0})
            }
            
            # If custom timeframe is used, ensure proper time structure
            if "from" in query and "to" in query:
                full_query["timeframe"] = "custom"
                full_query["time"] = {
                    "from": query["from"],
                    "to": query["to"],
                    "user_interval": "0"
                }
            elif "starttime" in query and "endtime" in query:
                full_query["timeframe"] = "custom"
                full_query["time"] = {
                    "from": query["starttime"],
                    "to": query["endtime"], 
                    "user_interval": "0"
                }
            elif "interval" in query:
                full_query["timeframe"] = str(query["interval"])
            
            # Encode the complete query structure
            encoded_query = encode_query(full_query)
            
            # Use POST request with JSON body containing the hash
            url = f"{self.client.host}{endpoint}"
            body = {"hash": encoded_query}
            headers, sorted_params = self._get_headers(endpoint, json_body=body)
            headers['Content-Type'] = 'application/json'
            self.client._debug(f"POST {url} body={body}")
            response = requests.post(url, headers=headers, data=json.dumps(body, separators=(',', ':')), verify=False)
            self.client._debug(f"Response status: {response.status_code}")
            self.client._debug(f"Response text: {response.text}")
            response.raise_for_status()
            return response.json()
        else:
            # Use GET request (traditional method) - encode the full query structure
            full_query = {
                "search": query.get("search", ""),
                "fields": query.get("fields", []),
                "offset": query.get("offset", 0),
                "timeframe": query.get("timeframe", "3600"),
                "time": query.get("time", {"user_interval": 0})
            }
            
            # Handle custom timeframes for GET as well
            if "from" in query and "to" in query:
                full_query["timeframe"] = "custom"
                full_query["time"] = {
                    "from": query["from"],
                    "to": query["to"],
                    "user_interval": "0"
                }
            elif "interval" in query:
                full_query["timeframe"] = str(query["interval"])
                
            encoded_query = encode_query(full_query)
            url = f"{self.client.host}{endpoint}/{encoded_query}"
            headers, sorted_params = self._get_headers(f"{endpoint}/{encoded_query}")
            self.client._debug(f"GET {url}")
            response = requests.get(url, headers=headers, params=sorted_params, verify=False)
            response.raise_for_status()
            return response.json()

    def analyze(self, field: str, analysis_type: str, query: Dict[str, Any]):
        """Analyze field data."""
        encoded_query = encode_query(query)
        endpoint = f'/advancedsearch/api/analyze/{field}/{analysis_type}/{encoded_query}'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def graph(self, graph_type: str, interval: int, query: Dict[str, Any]):
        """Get graph data."""
        encoded_query = encode_query(query)
        endpoint = f'/advancedsearch/api/graph/{graph_type}/{interval}/{encoded_query}'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()