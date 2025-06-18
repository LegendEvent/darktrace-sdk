import requests
from typing import List, Dict, Any
from .dt_utils import debug_print, BaseEndpoint


class Devices(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, **params):
        """Get device information from Darktrace.
        
        Args:
            **params: Query parameters for the request
                did (int): Device ID
                ip (str): Device IP
                sid (int): Subnet ID
                count (int): Number of devices to return
                seensince (str): Time window for device activity
                includetags (bool): Include device tags
                responsedata (str): Limit response to specific fields
        """
        endpoint = '/devices'
        url = f"{self.client.host}{endpoint}"
        
        # Get headers and sorted parameters
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        
        response = requests.get(
            url, 
            headers=headers,
            params=sorted_params,
            verify=False
        )
        response.raise_for_status()
        return response.json()

    def update(self, did: int, **kwargs):
        """Update device properties in Darktrace.
        
        Args:
            did (int): Device ID to update
            **kwargs: Device properties to update
                label (str): Device label
                priority (int): Device priority (-5 to 5)
                type (int): Device type enum
        """
        endpoint = '/devices'
        url = f"{self.client.host}{endpoint}"
        
        # Prepare request body
        body: Dict[str, Any] = {"did": did}
        body.update(kwargs)
        
        # Get headers (no params for POST request)
        headers, _ = self._get_headers(endpoint)
        self.client._debug(f"POST {url} body={body}")
        
        response = requests.post(
            url, 
            headers=headers,
            json=body,
            verify=False
        )
        return response.status_code == 200