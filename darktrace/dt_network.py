from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Network"]


class Network(BaseEndpoint):
    def __init__(self, client) -> None:
        super().__init__(client)

    def get(
        self,
        applicationprotocol: str | None = None,
        destinationport: int | None = None,
        did: int | None = None,
        endtime: int | None = None,
        from_: str | None = None,
        fulldevicedetails: bool | None = None,
        intext: str | None = None,
        ip: str | None = None,
        metric: str | None = None,
        port: int | None = None,
        protocol: str | None = None,
        sourceport: int | None = None,
        starttime: int | None = None,
        to: str | None = None,
        viewsubnet: int | None = None,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
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
        params = {}
        if applicationprotocol is not None:
            params["applicationprotocol"] = applicationprotocol
        if destinationport is not None:
            params["destinationport"] = destinationport
        if did is not None:
            params["did"] = did
        if endtime is not None:
            params["endtime"] = endtime
        if from_ is not None:
            params["from"] = from_
        if fulldevicedetails is not None:
            params["fulldevicedetails"] = fulldevicedetails
        if intext is not None:
            params["intext"] = intext
        if ip is not None:
            params["ip"] = ip
        if metric is not None:
            params["metric"] = metric
        if port is not None:
            params["port"] = port
        if protocol is not None:
            params["protocol"] = protocol
        if sourceport is not None:
            params["sourceport"] = sourceport
        if starttime is not None:
            params["starttime"] = starttime
        if to is not None:
            params["to"] = to
        if viewsubnet is not None:
            params["viewsubnet"] = viewsubnet
        if responsedata is not None:
            params["responsedata"] = responsedata
        return self._get("/network", params=params, timeout=timeout)
