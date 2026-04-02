from typing import Any, Dict, Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["EndpointDetails"]


class EndpointDetails(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        ip: Optional[str] = None,
        hostname: Optional[str] = None,
        additionalinfo: Optional[bool] = None,
        devices: Optional[bool] = None,
        score: Optional[bool] = None,
        responsedata: Optional[str] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Dict[str, Any]:
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
        url = f"{self.client.host}{endpoint}"
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

        headers, sorted_params = self._get_headers(endpoint, params)

        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET",
            url,
            headers=headers,
            params=sorted_params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()
