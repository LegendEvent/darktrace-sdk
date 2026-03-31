from typing import Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint


class SimilarDevices(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        device_id: Optional[str] = None,
        count: Optional[int] = None,
        fulldevicedetails: Optional[bool] = None,
        token: Optional[str] = None,
        responsedata: Optional[str] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
        **kwargs,
    ):
        """
        Get similar devices information from Darktrace.

        Args:
            device_id (str, optional): Device ID to find similar devices for. If not provided, returns all similar devices.
            count (int, optional): Number of similar devices to return.
            fulldevicedetails (bool, optional): Whether to include full device details in the response.
            token (str, optional): Pagination token for large result sets.
            responsedata (str, optional): Restrict the returned JSON to only the specified field(s).
            timeout (float or tuple, optional): Request timeout in seconds. Can be a single value or (connect_timeout, read_timeout).
            **kwargs: Additional parameters for future compatibility.

        Returns:
            list or dict: Similar devices information from Darktrace.
        """
        endpoint = f"/similardevices{f'/{device_id}' if device_id else ''}"
        url = f"{self.client.host}{endpoint}"

        params = dict()
        if count is not None:
            params["count"] = count
        if fulldevicedetails is not None:
            params["fulldevicedetails"] = fulldevicedetails
        if token is not None:
            params["token"] = token
        if responsedata is not None:
            params["responsedata"] = responsedata
        # Allow passing extra params for forward compatibility
        params.update(kwargs)

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
