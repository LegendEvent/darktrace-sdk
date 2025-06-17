import requests
from .dt_utils import debug_print

class DeviceSearch:
    def __init__(self, client):
        self.client = client

    def get(self, **params):
        """Search for devices."""
        endpoint = '/devicesearch'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 