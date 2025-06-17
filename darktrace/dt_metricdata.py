import requests
from typing import Optional, List
from .dt_utils import debug_print

class MetricData:
    def __init__(self, client):
        self.client = client

    def get(self, metric_id: str, start_time: Optional[int] = None, end_time: Optional[int] = None, interval: Optional[str] = None, devices: Optional[List[str]] = None, **params):
        """Get metric time series data."""
        endpoint = '/metricdata'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
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
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 