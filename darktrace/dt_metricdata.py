import requests
from typing import Optional, List
from .dt_utils import debug_print, BaseEndpoint

class MetricData(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        metric: Optional[str] = None,
        metrics: Optional[List[str]] = None,
        did: Optional[int] = None,
        ddid: Optional[int] = None,
        odid: Optional[int] = None,
        port: Optional[int] = None,
        sourceport: Optional[int] = None,
        destinationport: Optional[int] = None,
        protocol: Optional[str] = None,
        applicationprotocol: Optional[str] = None,
        starttime: Optional[int] = None,
        endtime: Optional[int] = None,
        from_: Optional[int] = None,
        to: Optional[int] = None,
        interval: Optional[str] = None,
        breachtimes: Optional[bool] = None,
        fulldevicedetails: Optional[bool] = None,
        devices: Optional[List[str]] = None,
        **params
    ):
        """
        Get metric time series data from Darktrace /metricdata endpoint.

        Args:
            metric (str, optional): Metric name to retrieve (use 'metrics' for multiple).
            metrics (list of str, optional): List of metric names to retrieve.
            did (int, optional): Device ID.
            ddid (int, optional): Destination Device ID.
            odid (int, optional): Other Device ID.
            port (int, optional): Port number.
            sourceport (int, optional): Source port number.
            destinationport (int, optional): Destination port number.
            protocol (str, optional): Protocol name (e.g., 'tcp', 'udp').
            applicationprotocol (str, optional): Application protocol name.
            starttime (int, optional): Start time (epoch ms).
            endtime (int, optional): End time (epoch ms).
            from_ (int, optional): Alias for starttime (epoch ms).
            to (int, optional): Alias for endtime (epoch ms).
            interval (str, optional): Time interval (e.g., '1min', '5min').
            breachtimes (bool, optional): Whether to include breach times.
            fulldevicedetails (bool, optional): Whether to include full device details.
            devices (list of str, optional): List of device IDs or names.
            **params: Additional parameters for future compatibility.

        Returns:
            dict: Metric time series data from Darktrace.
        """
        endpoint = '/metricdata'
        url = f"{self.client.host}{endpoint}"
        query_params = dict()

        # Handle metric/metrics
        if metrics is not None:
            query_params['metric'] = ','.join(metrics)
        elif metric is not None:
            query_params['metric'] = metric

        if did is not None:
            query_params['did'] = did
        if ddid is not None:
            query_params['ddid'] = ddid
        if odid is not None:
            query_params['odid'] = odid
        if port is not None:
            query_params['port'] = port
        if sourceport is not None:
            query_params['sourceport'] = sourceport
        if destinationport is not None:
            query_params['destinationport'] = destinationport
        if protocol is not None:
            query_params['protocol'] = protocol
        if applicationprotocol is not None:
            query_params['applicationprotocol'] = applicationprotocol
        if starttime is not None:
            query_params['starttime'] = starttime
        if endtime is not None:
            query_params['endtime'] = endtime
        if from_ is not None:
            query_params['from'] = from_
        if to is not None:
            query_params['to'] = to
        if interval is not None:
            query_params['interval'] = interval
        if breachtimes is not None:
            query_params['breachtimes'] = breachtimes
        if fulldevicedetails is not None:
            query_params['fulldevicedetails'] = fulldevicedetails
        if devices is not None:
            query_params['devices'] = ','.join(devices)

        # Add any extra params
        query_params.update(params)

        headers, sorted_params = self._get_headers(endpoint, query_params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()