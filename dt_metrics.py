import requests
from typing import Optional
from .utils import debug_print

class Metrics:
    def __init__(self, client):
        self.client = client

    def get(self, metric_id: Optional[int] = None, response_data: Optional[str] = None, **params):
        """Get metrics information."""
        endpoint = f'/metrics{f"/{metric_id}" if metric_id is not None else ""}'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 