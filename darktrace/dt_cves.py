import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class CVEs(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, did: Optional[int] = None, full_device_details: bool = False, **params):
        """Get CVE information for devices."""
        endpoint = '/cves'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        if did is not None:
            params['did'] = did
        if full_device_details:
            params['fulldevicedetails'] = 'true'
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json() 