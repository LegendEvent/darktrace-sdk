import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Metrics(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        metric_id: Optional[int] = None,
        responsedata: Optional[str] = None,
        **params
    ):
        """
        Get metrics information from Darktrace.

        Args:
            metric_id (int, optional): The metric logic ID (mlid) for a specific metric. If not provided, returns all metrics.
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field or object.
            **params: Additional parameters for future compatibility (currently unused).

        Returns:
            dict or list: Metric information from Darktrace. If metric_id is provided, returns a dict for that metric; otherwise, returns a list of all metrics.

        Example:
            >>> client.metrics.get()
            >>> client.metrics.get(metric_id=4)
            >>> client.metrics.get(responsedata="mlid,name")
        """
        endpoint = f'/metrics{f"/{metric_id}" if metric_id is not None else ""}'
        url = f"{self.client.host}{endpoint}"
        query_params = dict()
        if responsedata is not None:
            query_params['responsedata'] = responsedata
        # Add any extra params (future-proofing)
        query_params.update(params)
        headers, sorted_params = self._get_headers(endpoint, query_params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()