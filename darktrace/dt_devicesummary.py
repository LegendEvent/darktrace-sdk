import requests
from typing import Optional, Dict, Any
from .dt_utils import debug_print, BaseEndpoint

class DeviceSummary(BaseEndpoint):
    """
    Interface for the /devicesummary endpoint.
    Returns contextual information for a device, aggregated from /devices, /similardevices, /modelbreaches, /deviceinfo und /details.

    Parameters:
        did (int): Identification number of a device modelled in the Darktrace system. Required.
        device_name (str, optional): Device name.
        ip_address (str, optional): IP address.
        end_timestamp (int, optional): Epoch time for end of time range.
        start_timestamp (int, optional): Epoch time for start of time range.
        devicesummary_by (str, optional): Field to group summary by.
        devicesummary_by_value (str, optional): Value for grouping.
        device_type (str, optional): Device type filter.
        network_location (str, optional): Network location filter.
        network_location_id (str, optional): Network location ID filter.
        peer_id (str, optional): Peer device filter.
        source (str, optional): Source filter.
        status (str, optional): Device status filter.
        responsedata (str, optional): Restrict returned JSON to only this field/object.
        **kwargs: Any additional parameters (future-proofing, not in official docs)
    """

    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        did: int,
        device_name: Optional[str] = None,
        ip_address: Optional[str] = None,
        end_timestamp: Optional[int] = None,
        start_timestamp: Optional[int] = None,
        devicesummary_by: Optional[str] = None,
        devicesummary_by_value: Optional[str] = None,
        device_type: Optional[str] = None,
        network_location: Optional[str] = None,
        network_location_id: Optional[str] = None,
        peer_id: Optional[str] = None,
        source: Optional[str] = None,
        status: Optional[str] = None,
        responsedata: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get device summary information for a specific device.

        Args:
            did (int): Device ID (required)
            device_name (str, optional): Device name
            ip_address (str, optional): IP address
            end_timestamp (int, optional): Epoch time for end of time range
            start_timestamp (int, optional): Epoch time for start of time range
            devicesummary_by (str, optional): Field to group summary by
            devicesummary_by_value (str, optional): Value for grouping
            device_type (str, optional): Device type filter
            network_location (str, optional): Network location filter
            network_location_id (str, optional): Network location ID filter
            peer_id (str, optional): Peer device filter
            source (str, optional): Source filter
            status (str, optional): Device status filter
            responsedata (str, optional): Restrict returned JSON to only this field/object
            **kwargs: Any additional parameters (not in official docs)

        Returns:
            dict: API response
        """
        endpoint = '/devicesummary'
        url = f"{self.client.host}{endpoint}"
        params = {'did': did}
        if device_name is not None:
            params['device_name'] = device_name
        if ip_address is not None:
            params['ip_address'] = ip_address
        if end_timestamp is not None:
            params['end_timestamp'] = end_timestamp
        if start_timestamp is not None:
            params['start_timestamp'] = start_timestamp
        if devicesummary_by is not None:
            params['devicesummary_by'] = devicesummary_by
        if devicesummary_by_value is not None:
            params['devicesummary_by_value'] = devicesummary_by_value
        if device_type is not None:
            params['device_type'] = device_type
        if network_location is not None:
            params['network_location'] = network_location
        if network_location_id is not None:
            params['network_location_id'] = network_location_id
        if peer_id is not None:
            params['peer_id'] = peer_id
        if source is not None:
            params['source'] = source
        if status is not None:
            params['status'] = status
        if responsedata is not None:
            params['responsedata'] = responsedata
        params.update(kwargs)
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()