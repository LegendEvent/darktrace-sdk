import requests
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
            
        Note:
            POST requests are currently not working due to authentication signature issues.
            The Darktrace API documentation indicates POST parameters should be included
            in the signature calculation, but the exact format is unclear and multiple
            attempts following the official documentation have failed with "API SIGNATURE ERROR".
            Use post_request=False (default) to use GET requests which work correctly.
        """
        if post_request:
            raise NotImplementedError(
                "POST requests to Advanced Search API are currently not supported due to "
                "unresolved authentication signature calculation issues. Use GET requests instead "
                "by setting post_request=False (default)."
            )
            
        encoded_query = encode_query(query)
        endpoint = '/advancedsearch/api/search'
        
        # Use GET request (working method)
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