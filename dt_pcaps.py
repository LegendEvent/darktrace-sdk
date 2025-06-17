import requests
from typing import Optional
from .utils import debug_print

class PCAPs:
    def __init__(self, client):
        self.client = client

    def get(self, pcap_id: Optional[str] = None, response_data: Optional[str] = None, **params):
        """Get PCAP information or download a PCAP file."""
        endpoint = f'/pcaps{f"/{pcap_id}" if pcap_id else ""}'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.content 