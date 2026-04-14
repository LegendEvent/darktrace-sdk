from __future__ import annotations

from typing import Any

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Devices"]


class Devices(BaseEndpoint):
    def __init__(self, client) -> None:
        super().__init__(client)

    def get(
        self,
        did: int | None = None,
        ip: str | None = None,
        iptime: str | None = None,
        mac: str | None = None,
        seensince: str | None = None,
        sid: int | None = None,
        count: int | None = None,
        includetags: bool | None = None,
        responsedata: str | None = None,
        cloudsecurity: bool | None = None,
        saasfilter: Any | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get device(s) from Darktrace.

        Args:
            did (int, optional): Device ID
            ip (str, optional): Filter by IP address
            iptime (str, optional): IP time
            mac (str, optional): Filter by MAC address
            sid (int, optional): Subnet ID
            seensince (str, optional): Relative offset for activity
            count (int, optional): Number of devices to return
            includetags (bool, optional): Include tags in response
            cloudsecurity (bool, optional): Cloud security status
            responsedata (str, optional): Restrict returned JSON to only this field/object
            saasfilter (Any, optional): SaaS filter

        Returns:
            list or dict: API response containing device information
        """
        endpoint = "/devices"

        # Build parameters dictionary
        params = dict()
        if did is not None:
            params["did"] = did
        if ip is not None:
            params["ip"] = ip
        if iptime is not None:
            params["iptime"] = iptime
        if mac is not None:
            params["mac"] = mac
        if seensince is not None:
            params["seensince"] = seensince
        if sid is not None:
            params["sid"] = sid
        if count is not None:
            params["count"] = count
        if includetags is not None:
            params["includetags"] = includetags
        if responsedata is not None:
            params["responsedata"] = responsedata
        if cloudsecurity is not None:
            params["cloudsecurity"] = cloudsecurity
        # saasfilter can be a string or list of strings
        if saasfilter is not None:
            params["saasfilter"] = saasfilter

        return self._get(endpoint, params=params, timeout=timeout)

    def update(
        self,
        did: int,
        timeout: float | tuple[float, float] | None = _UNSET,
        **kwargs,
    ) -> dict:
        """Update device properties in Darktrace.

        Args:
            did (int): Device ID to update
            **kwargs: Device properties to update
                label (str): Device label
                priority (int): Device priority (-5 to 5)
                type (int): Device type enum
        """
        endpoint = "/devices"

        # Prepare request body
        body: dict[str, Any] = {"did": did}
        body.update(kwargs)

        return self._post_json(endpoint, body=body, timeout=timeout)
