import requests
from typing import Dict, Any
from .dt_utils import debug_print, BaseEndpoint, encode_query

class AdvancedSearch(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def search(self, query: Dict[str, Any], post_request: bool = False):
        """Perform Advanced Search query."""
        encoded_query = encode_query(query)
        endpoint = '/advancedsearch/api/search'
        if post_request:
            url = f"{self.client.host}{endpoint}"
            headers, sorted_params = self._get_headers(endpoint)
            self.client._debug(f"POST {url} body={{'hash': {encoded_query}}}")
            response = requests.post(url, headers=headers, json={'hash': encoded_query}, verify=False)
        else:
            url = f"{self.client.host}{endpoint}/{encoded_query}"
            headers, sorted_params = self._get_headers(f"{endpoint}/{encoded_query}")
            self.client._debug(f"GET {url}")
            response = requests.get(url, headers=headers, params=sorted_params or , verify=False)
        response.raise_for_status()
        return response.json()

    def analyze(self, field: str, analysis_type: str, query: Dict[str, Any]):
        """Analyze field data."""
        encoded_query = encode_query(query)
        endpoint = f'/advancedsearch/api/analyze/{field}/{analysis_type}/{encoded_query}'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url}")
        response = requests.get(url, headers=headers, params=sorted_params or , verify=False)
        response.raise_for_status()
        return response.json()

    def graph(self, graph_type: str, interval: int, query: Dict[str, Any]):
        """Get graph data."""
        encoded_query = encode_query(query)
        endpoint = f'/advancedsearch/api/graph/{graph_type}/{interval}/{encoded_query}'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url}")
        response = requests.get(url, headers=headers, params=sorted_params or , verify=False)
        response.raise_for_status()
        return response.json() 