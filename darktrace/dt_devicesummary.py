import requests
from typing import Optional, Dict, Any
from .dt_utils import debug_print, BaseEndpoint

class DeviceSummary(BaseEndpoint):
    """
    Interface for the /devicesummary endpoint.
    Returns contextual information for a device, aggregated from /devices, /similardevices, /modelbreaches, /deviceinfo und /details.

    Parameters:
        did (int): Identification number of a device modelled in the Darktrace system. Required.
        responsedata (str, optional): Restrict returned JSON to only this field/object.
        **kwargs: Any additional parameters (future-proofing, not in official docs)
    """

    def __init__(self, client):
        super().__init__(client)

    def get(self, did: int, responsedata: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Get device summary information for a specific device.

        Args:
            did (int): Device ID (required)
            responsedata (str, optional): Restrict returned JSON to only this field/object
            **kwargs: Any additional parameters (not in official docs)

        Returns:
            dict: API response
        """
        endpoint = '/devicesummary'
        url = f"{self.client.host}{endpoint}"
        params = {'did': did}
        if responsedata is not None:
            params['responsedata'] = responsedata
        params.update(kwargs)
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()