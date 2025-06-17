import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Components(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, cid: Optional[int] = None, **params):
        """Get information about model components."""
        endpoint = f'/components{f"/{cid}" if cid is not None else ""}'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json() 