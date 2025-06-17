import requests
from typing import Dict, Any
from .dt_utils import debug_print

class ModelBreaches:
    def __init__(self, client):
        self.client = client

    def get(self, **params):
        """Get model breach alerts."""
        endpoint = '/modelbreaches'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_comments(self, pbid: int, **params):
        """Get comments for a specific model breach alert."""
        endpoint = f'/modelbreaches/{pbid}/comments'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def add_comment(self, pbid: int, message: str):
        """Add a comment to a model breach alert."""
        endpoint = f'/modelbreaches/{pbid}/comments'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body: Dict[str, Any] = {'message': message}
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def acknowledge(self, pbid: int):
        """Acknowledge a model breach alert."""
        endpoint = f'/modelbreaches/{pbid}/acknowledge'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body: Dict[str, bool] = {'acknowledge': True}
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def unacknowledge(self, pbid: int):
        """Unacknowledge a model breach alert."""
        endpoint = f'/modelbreaches/{pbid}/unacknowledge'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body: Dict[str, bool] = {'unacknowledge': True}
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200 