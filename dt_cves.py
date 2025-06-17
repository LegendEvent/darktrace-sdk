import requests
from typing import Optional
from .utils import debug_print

class CVEs:
    def __init__(self, client):
        self.client = client

    def get(self, did: Optional[int] = None, full_device_details: bool = False, **params):
        """Get CVE information for devices."""
        endpoint = '/cves'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        if did is not None:
            params['did'] = did
        if full_device_details:
            params['fulldevicedetails'] = 'true'
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 