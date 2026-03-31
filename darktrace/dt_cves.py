from typing import Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint


class CVEs(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        did: Optional[int] = None,
        fulldevicedetails: Optional[bool] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
        **params,
    ):
        """
        Retrieve CVE information for devices from the Darktrace/OT ICS Vulnerability Tracker.

        Parameters:
            did (int, optional): Device ID to filter CVEs for a specific device.
            fulldevicedetails (bool, optional): If True, returns full device detail objects for all referenced devices.
            **params: Additional query parameters for future compatibility.

        Returns:
            dict: JSON response from the /cves endpoint.

        Example usage:
            client.cves.get()
            client.cves.get(did=12, fulldevicedetails=True)
        """
        endpoint = "/cves"
        url = f"{self.client.host}{endpoint}"
        # Build params dict
        if did is not None:
            params["did"] = did
        if fulldevicedetails is not None:
            params["fulldevicedetails"] = "true" if fulldevicedetails else "false"
        # Use consistent parameter/header handling
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
