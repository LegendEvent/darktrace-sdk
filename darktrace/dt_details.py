import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Details(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, did: Optional[int] = None, pbid: Optional[int] = None, msg: Optional[str] = None, blocked_connections: Optional[str] = None, event_type: str = "connection", count: Optional[int] = None, start_time: Optional[int] = None, end_time: Optional[int] = None, from_time: Optional[str] = None, to_time: Optional[str] = None, application_protocol: Optional[str] = None, destination_port: Optional[int] = None, source_port: Optional[int] = None, port: Optional[int] = None, protocol: Optional[str] = None, ddid: Optional[int] = None, odid: Optional[int] = None, external_hostname: Optional[str] = None, intext: Optional[str] = None, uid: Optional[str] = None, deduplicate: bool = False, full_device_details: bool = False, response_data: Optional[str] = None, **params):
        """Get detailed connection and event information."""
        endpoint = '/details'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        if did is not None:
            params['did'] = did
        if pbid is not None:
            params['pbid'] = pbid
        if msg is not None:
            params['msg'] = msg
        if blocked_connections is not None:
            params['blockedconnections'] = blocked_connections
        params['eventtype'] = event_type
        if from_time:
            params['from'] = from_time
        if to_time:
            params['to'] = to_time
        if start_time:
            params['starttime'] = start_time
        if end_time:
            params['endtime'] = end_time
        if count is not None:
            params['count'] = count
        if application_protocol:
            params['applicationprotocol'] = application_protocol
        if destination_port:
            params['destinationport'] = destination_port
        if source_port:
            params['sourceport'] = source_port
        if port:
            params['port'] = port
        if protocol:
            params['protocol'] = protocol
        if ddid:
            params['ddid'] = ddid
        if odid:
            params['odid'] = odid
        if external_hostname:
            params['externalhostname'] = external_hostname
        if intext:
            params['intext'] = intext
        if uid:
            params['uid'] = uid
        if deduplicate:
            params['deduplicate'] = str(deduplicate).lower()
        if full_device_details:
            params['fulldevicedetails'] = str(full_device_details).lower()
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json() 