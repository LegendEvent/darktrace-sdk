import requests
from typing import Optional
from .utils import debug_print

class DeviceInfo:
    def __init__(self, client):
        self.client = client

    def get(self, did: int, datatype: str = "co", odid: Optional[int] = None, port: Optional[int] = None, external_domain: Optional[str] = None, full_device_details: bool = False, show_all_graph_data: bool = True, similar_devices: Optional[int] = None, interval_hours: int = 1, **params):
        """Get device connection information."""
        endpoint = '/deviceinfo'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        params.update({
            'did': did,
            'datatype': datatype,
            'showallgraphdata': str(show_all_graph_data).lower(),
            'fulldevicedetails': str(full_device_details).lower(),
            'intervalhours': interval_hours
        })
        if odid is not None:
            params['odid'] = odid
        if port is not None:
            params['port'] = port
        if external_domain is not None:
            params['externaldomain'] = external_domain
        if similar_devices is not None:
            params['similardevices'] = similar_devices
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 