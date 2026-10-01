from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["SimilarDevices"]


class SimilarDevices(BaseEndpoint):
    def get(
        self,
        device_id: int | str | None = None,
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
            device_id (int or str, optional): Device ID (sent as the ``did`` query parameter) to find similar devices for.
            count (int, optional): Number of similar devices to return.
            fulldevicedetails (bool, optional): Whether to include full device details in the response.
            token (str, optional): System-notice change token; the response then contains the old and new similar-device lists.
            responsedata (str, optional): Restrict the returned JSON to only the specified field(s).
            timeout (float or tuple, optional): Request timeout in seconds. Can be a single value or (connect_timeout, read_timeout).
            **kwargs: Additional API parameters.

        Returns:
            list or dict: Similar devices information from Darktrace.
        """
        endpoint = "/similardevices"
        params = {}
        if device_id is not None:
            params["did"] = device_id
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
