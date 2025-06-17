import requests
from typing import Optional, List
from .dt_utils import debug_print, BaseEndpoint

class MetricData(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, metric_id: str, start_time: Optional[int] = None, end_time: Optional[int] = None, interval: Optional[str] = None, devices: Optional[List[str]] = None, **params):
        """Get metric time series data."""
        endpoint = '/metricdata'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        params['metricid'] = metric_id
        if start_time is not None:
            params['starttime'] = start_time
        if end_time is not None:
            params['endtime'] = end_time
        if interval:
            params['interval'] = interval
        if devices:
            params['devices'] = ','.join(devices)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json() 