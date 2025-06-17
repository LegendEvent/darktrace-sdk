import requests
from typing import List
from .utils import debug_print

class Devices:
    def __init__(self, client):
        self.client = client

    def get(self, **params):
        """Get device information from Darktrace."""
        endpoint = '/devices'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def update(self, did: int, **kwargs):
        """Update device properties in Darktrace."""
        endpoint = '/devices'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body = {"did": did}
        body.update(kwargs)
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200 