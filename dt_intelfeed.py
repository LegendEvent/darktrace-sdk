import requests
from typing import Optional, List
from .utils import debug_print

class IntelFeed:
    def __init__(self, client):
        self.client = client

    def get(self, feed_type: Optional[str] = None, response_data: Optional[str] = None, **params):
        """Get intelligence feed data or details for a specific feed type."""
        endpoint = f'/intelfeed{f"/{feed_type}" if feed_type else ""}'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def update(self, add_entry: Optional[str] = None, add_list: Optional[List[str]] = None, description: Optional[str] = None, source: Optional[str] = None, expiry: Optional[str] = None, is_hostname: bool = False, remove_entry: Optional[str] = None, remove_all: bool = False, enable_antigena: bool = False):
        """Update the intel feed (watched domains) in Darktrace."""
        endpoint = '/intelfeed'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body = {}
        if add_entry:
            body['addentry'] = add_entry
        elif add_list:
            body['addlist'] = ','.join(add_list)
        elif remove_entry:
            body['removeentry'] = remove_entry
        elif remove_all:
            body['removeall'] = True
        if description:
            body['description'] = description
        if source:
            body['source'] = source
        if expiry:
            body['expiry'] = expiry
        if is_hostname:
            body['hostname'] = True
        if enable_antigena:
            body['iagn'] = True
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        response.raise_for_status()
        return response.json() 