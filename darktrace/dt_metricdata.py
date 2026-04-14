from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["MetricData"]


class MetricData(BaseEndpoint):
    def __init__(self, client) -> None:
        super().__init__(client)

    def get(
        self,
        metric: str | None = None,
        metrics: list[str] | None = None,
        did: int | None = None,
        ddid: int | None = None,
        odid: int | None = None,
        port: int | None = None,
        sourceport: int | None = None,
        destinationport: int | None = None,
        protocol: str | None = None,
        applicationprotocol: str | None = None,
        starttime: int | None = None,
        endtime: int | None = None,
        from_: int | None = None,
        to: int | None = None,
        interval: str | None = None,
        breachtimes: bool | None = None,
        fulldevicedetails: bool | None = None,
        devices: list[str] | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
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
            timeout (float or tuple, optional): Request timeout in seconds. Can be a single value or (connect_timeout, read_timeout).
            **params: Additional parameters for future compatibility.

        Returns:
            dict: Metric time series data from Darktrace.
        """
        endpoint = "/metricdata"
        query_params = dict()

        # Handle metric/metrics - mutually exclusive: use either metrics (list) or metric (single string)
        if metrics is not None:
            query_params["metric"] = ",".join(metrics)
        elif metric is not None:
            query_params["metric"] = metric

        if did is not None:
            query_params["did"] = did
        if ddid is not None:
            query_params["ddid"] = ddid
        if odid is not None:
            query_params["odid"] = odid
        if port is not None:
            query_params["port"] = port
        if sourceport is not None:
            query_params["sourceport"] = sourceport
        if destinationport is not None:
            query_params["destinationport"] = destinationport
        if protocol is not None:
            query_params["protocol"] = protocol
        if applicationprotocol is not None:
            query_params["applicationprotocol"] = applicationprotocol
        if starttime is not None:
            query_params["starttime"] = starttime
        if endtime is not None:
            query_params["endtime"] = endtime
        if from_ is not None:
            query_params["from"] = from_
        if to is not None:
            query_params["to"] = to
        if interval is not None:
            query_params["interval"] = interval
        if breachtimes is not None:
            query_params["breachtimes"] = breachtimes
        if fulldevicedetails is not None:
            query_params["fulldevicedetails"] = fulldevicedetails
        if devices is not None:
            query_params["devices"] = ",".join(devices)

        # Add any extra params
        query_params.update(params)

        return self._get(endpoint, params=query_params, timeout=timeout)
