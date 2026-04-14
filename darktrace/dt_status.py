from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Status"]


class Status(BaseEndpoint):
    def __init__(self, client) -> None:
        super().__init__(client)

    def get(
        self,
        includechildren: bool | None = None,
        fast: bool | None = None,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get detailed system health and status information from Darktrace.

        Args:
            includechildren (bool, optional): Whether to include information about probes (children). True by default.
            fast (bool, optional): When true, returns data faster but may omit subnet connectivity information if not cached.
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field(s) or object(s).
            timeout (float or tuple, optional): Request timeout in seconds. Can be a single value or (connect_timeout, read_timeout).

        Returns:
            dict: System health and status information from Darktrace.
        """
        params = {}
        if includechildren is not None:
            params["includechildren"] = includechildren
        if fast is not None:
            params["fast"] = fast
        if responsedata is not None:
            params["responsedata"] = responsedata
        return self._get("/status", params=params, timeout=timeout)
