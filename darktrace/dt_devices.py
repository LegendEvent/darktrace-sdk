import requests
from typing import List, Dict, Any
from .dt_utils import debug_print, BaseEndpoint

class Devices(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, **params):
        """Get device information from Darktrace."""
        endpoint = '/devices'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def update(self, did: int, **kwargs):
        """Update device properties in Darktrace."""
        endpoint = '/devices'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, Any] = {"did": did}
        body.update(kwargs)
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200 