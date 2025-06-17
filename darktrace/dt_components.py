import requests
from typing import Optional
from .dt_utils import debug_print

class Components:
    def __init__(self, client):
        self.client = client

    def get(self, cid: Optional[int] = None, **params):
        """Get information about model components."""
        endpoint = f'/components{f"/{cid}" if cid is not None else ""}'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 