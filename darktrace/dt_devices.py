import json
from typing import Any, Dict, Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Devices"]


class Devices(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        did: Optional[int] = None,
        ip: Optional[str] = None,
        iptime: Optional[str] = None,
        mac: Optional[str] = None,
        seensince: Optional[str] = None,
        sid: Optional[int] = None,
        count: Optional[int] = None,
        includetags: Optional[bool] = None,
        responsedata: Optional[str] = None,
        cloudsecurity: Optional[bool] = None,
        saasfilter: Optional[Any] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ):
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
        url = f"{self.client.host}{endpoint}"

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

    def update(
        self,
        did: int,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
        **kwargs,
    ) -> dict:  # type: ignore[assignment]
        """Update device properties in Darktrace.

        Args:
            did (int): Device ID to update
            **kwargs: Device properties to update
                label (str): Device label
                priority (int): Device priority (-5 to 5)
                type (int): Device type enum
        """
        endpoint = "/devices"
        url = f"{self.client.host}{endpoint}"

        # Prepare request body
        body: Dict[str, Any] = {"did": did}
        body.update(kwargs)

        # Get headers with JSON body for signature generation
        headers, sorted_params = self._get_headers(endpoint, json_body=body)

        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(",", ":"))
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "POST",
            url,
            headers=headers,
            params=sorted_params,
            data=json_data,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()
