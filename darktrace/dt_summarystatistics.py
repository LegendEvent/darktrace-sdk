import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class SummaryStatistics(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self,
            responsedata: Optional[str] = None,
            eventtype: Optional[str] = None,
            endtime: Optional[int] = None,
            to: Optional[str] = None,
            hours: Optional[int] = None,
            csensor: Optional[bool] = None,
            mitreTactics: Optional[bool] = None
        ):
        """
        Get summary statistics information from Darktrace.

        Args:
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field(s) or object(s).
            eventtype (str, optional): Changes the format of data to return numeric event counts for any of the four categories of events and/or three types (see docs).
            endtime (int, optional): End time of data to return in ms since epoch (UTC). Requires eventtype.
            to (str, optional): End time of data to return in 'YYYY-MM-DD HH:MM:SS' format. Requires eventtype.
            hours (int, optional): Number of hour intervals from the end time (or current time) to return. Requires eventtype.
            csensor (bool, optional): When true, only bandwidth statistics for cSensor agents are returned. When false, statistics for Darktrace/Network bandwidth.
            mitreTactics (bool, optional): When true, alters the returned data to display MITRE ATT&CK Framework breakdown.

        Returns:
            dict: Summary statistics information from Darktrace.
        """
        endpoint = '/summarystatistics'
        url = f"{self.client.host}{endpoint}"

        params = dict()
        if responsedata is not None:
            params['responsedata'] = responsedata
        if eventtype is not None:
            params['eventtype'] = eventtype
        if endtime is not None:
            params['endtime'] = endtime
        if to is not None:
            params['to'] = to
        if hours is not None:
            params['hours'] = hours
        if csensor is not None:
            params['csensor'] = csensor
        if mitreTactics is not None:
            params['mitreTactics'] = mitreTactics

        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()