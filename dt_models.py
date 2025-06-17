import requests
from typing import Optional
from .utils import debug_print

class Models:
    def __init__(self, client):
        self.client = client

    def get(self, uuid: Optional[str] = None, response_data: Optional[str] = None, **params):
        """Get model information."""
        endpoint = '/models'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        if uuid:
            params['uuid'] = uuid
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 