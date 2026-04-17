from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["EndpointDetails"]


class EndpointDetails(BaseEndpoint):
    def get(
        self,
        ip: str | None = None,
        hostname: str | None = None,
        additionalinfo: bool | None = None,
        devices: bool | None = None,
        score: bool | None = None,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get endpoint details from Darktrace.

        Args:
            ip (str, optional): Return data for this IP address.
            hostname (str, optional): Return data for this hostname.
            additionalinfo (bool, optional): Return additional information about the endpoint.
            devices (bool, optional): Return a list of devices which have recently connected to the endpoint.
            score (bool, optional): Return rarity data for this endpoint.
            responsedata (str, optional): Restrict the returned JSON to only the specified field/object.

        Returns:
            dict: Endpoint details from Darktrace.
        """
        endpoint = "/endpointdetails"
        params = dict()
        if ip is not None:
            params["ip"] = ip
        if hostname is not None:
            params["hostname"] = hostname
        if additionalinfo is not None:
            params["additionalinfo"] = additionalinfo
        if devices is not None:
            params["devices"] = devices
        if score is not None:
            params["score"] = score
        if responsedata is not None:
            params["responsedata"] = responsedata

        return self._get(endpoint, params=params, timeout=timeout)
