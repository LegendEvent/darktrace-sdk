import requests
from .dt_utils import debug_print, BaseEndpoint

class DeviceSearch(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, **params):
        """Search for devices."""
        endpoint = '/devicesearch'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json() 