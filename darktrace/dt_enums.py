import requests
from typing import Optional
from .dt_utils import debug_print

class Enums:
    def __init__(self, client):
        self.client = client

    def get(self, enum_type: Optional[str] = None, response_data: Optional[str] = None, **params):
        """Get enum values for a given type or all types."""
        endpoint = f'/enums{f"/{enum_type}" if enum_type else ""}'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 