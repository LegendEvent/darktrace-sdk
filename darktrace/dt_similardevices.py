from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["SimilarDevices"]


class SimilarDevices(BaseEndpoint):
    def get(
        self,
        device_id: str | None = None,
        count: int | None = None,
        fulldevicedetails: bool | None = None,
        token: str | None = None,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **kwargs,
    ) -> dict | list:
        """
        Get similar devices information from Darktrace.

        Args:
            device_id (str, optional): Device ID to find similar devices for. If not provided, returns all similar devices.
            count (int, optional): Number of similar devices to return.
            fulldevicedetails (bool, optional): Whether to include full device details in the response.
            token (str, optional): Pagination token for large result sets.
            responsedata (str, optional): Restrict the returned JSON to only the specified field(s).
            timeout (float or tuple, optional): Request timeout in seconds. Can be a single value or (connect_timeout, read_timeout).
            **kwargs: Additional API parameters.

        Returns:
            list or dict: Similar devices information from Darktrace.
        """
        endpoint = f"/similardevices{f'/{device_id}' if device_id else ''}"
        params = {}
        if count is not None:
            params["count"] = count
        if fulldevicedetails is not None:
            params["fulldevicedetails"] = fulldevicedetails
        if token is not None:
            params["token"] = token
        if responsedata is not None:
            params["responsedata"] = responsedata
        params.update(kwargs)
        return self._get(endpoint, params=params, timeout=timeout)
