import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Subnets(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, subnet_id: Optional[str] = None, response_data: Optional[str] = None, **params):
        """Get subnet information."""
        endpoint = f'/subnets{f"/{subnet_id}" if subnet_id else ""}'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json() 