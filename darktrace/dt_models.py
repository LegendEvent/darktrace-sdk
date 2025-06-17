import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Models(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, uuid: Optional[str] = None, response_data: Optional[str] = None, **params):
        """Get model information."""
        endpoint = '/models'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        if uuid:
            params['uuid'] = uuid
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json() 