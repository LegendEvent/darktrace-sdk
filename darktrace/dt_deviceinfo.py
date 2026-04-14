from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["DeviceInfo"]


class DeviceInfo(BaseEndpoint):
    def __init__(self, client) -> None:
        super().__init__(client)

    def get(
        self,
        did: int,
        datatype: str = "co",
        odid: int | None = None,
        port: int | None = None,
        externaldomain: str | None = None,
        fulldevicedetails: bool = False,
        showallgraphdata: bool = True,
        similardevices: int | None = None,
        intervalhours: int = 1,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
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
        endpoint = "/deviceinfo"
        params.update(
            {
                "did": did,
                "datatype": datatype,
                "showallgraphdata": str(showallgraphdata).lower(),
                "fulldevicedetails": str(fulldevicedetails).lower(),
                "intervalhours": intervalhours,
            }
        )
        if odid is not None:
            params["odid"] = odid
        if port is not None:
            params["port"] = port
        if externaldomain is not None:
            params["externaldomain"] = externaldomain
        if similardevices is not None:
            params["similardevices"] = similardevices

        return self._get(endpoint, params=params, timeout=timeout)
