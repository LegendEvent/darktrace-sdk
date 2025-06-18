import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class CVEs(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        did: Optional[int] = None,
        fulldevicedetails: Optional[bool] = None,
        **params
    ):
        """
        Retrieve CVE information for devices from the Darktrace/OT ICS Vulnerability Tracker.

        Parameters:
            did (int, optional): Device ID to filter CVEs for a specific device.
            fulldevicedetails (bool, optional): If True, returns full device detail objects for all referenced devices.
            **params: Additional query parameters for future compatibility.

        Returns:
            dict: JSON response from the /cves endpoint.

        Example usage:
            client.cves.get()
            client.cves.get(did=12, fulldevicedetails=True)
        """
        endpoint = '/cves'
        url = f"{self.client.host}{endpoint}"
        # Build params dict
        if did is not None:
            params['did'] = did
        if fulldevicedetails is not None:
            params['fulldevicedetails'] = 'true' if fulldevicedetails else 'false'
        # Use consistent parameter/header handling
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()