import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class DeviceInfo(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        did: int,
        datatype: str = "co",
        odid: Optional[int] = None,
        port: Optional[int] = None,
        externaldomain: Optional[str] = None,
        fulldevicedetails: bool = False,
        showallgraphdata: bool = True,
        similardevices: Optional[int] = None,
        intervalhours: int = 1,
        **params
    ):
        """
        Get device connection information from the /deviceinfo endpoint.

        Parameters
        ----------
        did : int
            Identification number of a device.
        datatype : str, optional
            Return data for either connections ('co'), data size out ('sizeout'), or data size in ('sizein'). Default is 'co'.
        odid : int, optional
            Identification number of a destination device to restrict data to.
        port : int, optional
            Restricts returned connection data to the port specified.
        externaldomain : str, optional
            Restrict external data to a particular domain name.
        fulldevicedetails : bool, optional
            Returns the full device detail objects for all devices referenced by data in an API response. Default is False.
        showallgraphdata : bool, optional
            Return an entry for all time intervals in the graph data, including zero counts. Default is True.
        similardevices : int, optional
            Return data for the primary device and this number of similar devices.
        intervalhours : int, optional
            The size in hours that the returned time series data is grouped by. Default is 1.
        **params : dict
            Additional parameters to pass to the API.

        Returns
        -------
        dict
            JSON response from the API.
        """
        endpoint = '/deviceinfo'
        params.update({
            'did': did,
            'datatype': datatype,
            'showallgraphdata': str(showallgraphdata).lower(),
            'fulldevicedetails': str(fulldevicedetails).lower(),
            'intervalhours': intervalhours
        })
        if odid is not None:
            params['odid'] = odid
        if port is not None:
            params['port'] = port
        if externaldomain is not None:
            params['externaldomain'] = externaldomain
        if similardevices is not None:
            params['similardevices'] = similardevices

        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()