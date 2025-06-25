import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Network(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self,
            applicationprotocol: Optional[str] = None,
            destinationport: Optional[int] = None,
            did: Optional[int] = None,
            endtime: Optional[int] = None,
            from_: Optional[str] = None,
            fulldevicedetails: Optional[bool] = None,
            intext: Optional[str] = None,
            ip: Optional[str] = None,
            metric: Optional[str] = None,
            port: Optional[int] = None,
            protocol: Optional[str] = None,
            sourceport: Optional[int] = None,
            starttime: Optional[int] = None,
            to: Optional[str] = None,
            viewsubnet: Optional[int] = None,
            responsedata: Optional[str] = None
        ):
        """
        Get network connectivity and statistics information from Darktrace.

        Args:
            applicationprotocol (str, optional): Filter by application protocol (see /enums for values).
            destinationport (int, optional): Filter by destination port.
            did (int, optional): Device ID to focus on.
            endtime (int, optional): End time in ms since epoch (UTC).
            from_ (str, optional): Start time in 'YYYY-MM-DD HH:MM:SS' format.
            fulldevicedetails (bool, optional): Return full device detail objects for all referenced devices.
            intext (str, optional): Filter by internal/external traffic ('internal' or 'external').
            ip (str, optional): Return data for this IP address.
            metric (str, optional): Name of metric (see /metrics for available metrics).
            port (int, optional): Filter by source or destination port.
            protocol (str, optional): Filter by IP protocol (see /enums for values).
            sourceport (int, optional): Filter by source port.
            starttime (int, optional): Start time in ms since epoch (UTC).
            to (str, optional): End time in 'YYYY-MM-DD HH:MM:SS' format.
            viewsubnet (int, optional): Subnet ID to focus on.
            responsedata (str, optional): Restrict returned JSON to only the specified field(s) or object(s).

        Returns:
            dict: Network connectivity/statistics information from Darktrace.
        """
        endpoint = '/network'
        url = f"{self.client.host}{endpoint}"
        params = dict()
        if applicationprotocol is not None:
            params['applicationprotocol'] = applicationprotocol
        if destinationport is not None:
            params['destinationport'] = destinationport
        if did is not None:
            params['did'] = did
        if endtime is not None:
            params['endtime'] = endtime
        if from_ is not None:
            params['from'] = from_
        if fulldevicedetails is not None:
            params['fulldevicedetails'] = fulldevicedetails
        if intext is not None:
            params['intext'] = intext
        if ip is not None:
            params['ip'] = ip
        if metric is not None:
            params['metric'] = metric
        if port is not None:
            params['port'] = port
        if protocol is not None:
            params['protocol'] = protocol
        if sourceport is not None:
            params['sourceport'] = sourceport
        if starttime is not None:
            params['starttime'] = starttime
        if to is not None:
            params['to'] = to
        if viewsubnet is not None:
            params['viewsubnet'] = viewsubnet
        if responsedata is not None:
            params['responsedata'] = responsedata

        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()