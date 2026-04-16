from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Metrics"]


class Metrics(BaseEndpoint):
    def get(
        self,
        metric_id: int | None = None,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
        """
        Get metrics information from Darktrace.

        Args:
            metric_id (int, optional): The metric logic ID (mlid) for a specific metric. If not provided, returns all metrics.
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field or object.
            **params: Additional API parameters.

        Returns:
            dict or list: Metric information from Darktrace. If metric_id is provided, returns a dict for that metric; otherwise, returns a list of all metrics.

        Example:
            >>> client.metrics.get()
            >>> client.metrics.get(metric_id=4)
            >>> client.metrics.get(responsedata="mlid,name")
        """
        endpoint = f"/metrics{f'/{metric_id}' if metric_id is not None else ''}"
        query_params = {}
        if responsedata is not None:
            query_params["responsedata"] = responsedata
        query_params.update(params)
        return self._get(endpoint, params=query_params, timeout=timeout)
