from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["MetricData"]


class MetricData(BaseEndpoint):
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
        protocol: int | str | None = None,
        applicationprotocol: str | None = None,
        starttime: int | None = None,
        endtime: int | None = None,
        from_: str | None = None,
        to: str | None = None,
        interval: int | None = None,
        breachtimes: bool | None = None,
        fulldevicedetails: bool | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
        """
        Get metric time series data from Darktrace /metricdata endpoint.

        Args:
            metric (str, optional): System name of a metric (the ``name`` field of /metrics, not the label).
            metrics (list of str, optional): Several metric names; sent as ``metric1=``, ``metric2=``, ... and
                one metric object is returned per name.
            did (int, optional): Device ID.
            ddid (int, optional): Destination Device ID.
            odid (int, optional): Other Device ID.
            port (int, optional): Port number.
            sourceport (int, optional): Source port number.
            destinationport (int, optional): Destination port number.
            protocol (int or str, optional): IP protocol, see /enums for the list (e.g. 6 for TCP).
            applicationprotocol (str, optional): Application protocol, see /enums for the list.
            starttime (int, optional): Start time (epoch ms).
            endtime (int, optional): End time (epoch ms).
            from_ (str, optional): Start time in ``YYYY-MM-DD HH:MM:SS`` format (sent as ``from``).
            to (str, optional): End time in ``YYYY-MM-DD HH:MM:SS`` format.
            interval (int, optional): Interval size in seconds to group data into (guide default 60).
            breachtimes (bool, optional): Whether to include breach times (alters the response structure).
            fulldevicedetails (bool, optional): Whether to include full device details.
            timeout (float or tuple, optional): Request timeout in seconds. Can be a single value or (connect_timeout, read_timeout).
            **params: Additional API parameters.

        Returns:
            list: One ``{"metric": ..., "data": [...]}`` object per requested metric; with
            ``breachtimes`` the first element is a ``{"breachtimes": [...]}`` object.

        Note:
            The API requires time parameters in pairs (starttime+endtime or from+to).
        """
        endpoint = "/metricdata"
        query_params = dict()

        if (starttime is None) != (endtime is None):
            raise ValueError("starttime and endtime must be given together.")
        if (from_ is None) != (to is None):
            raise ValueError("from_ and to must be given together.")

        # Several metrics: metric1=, metric2=, ... (guide); a single metric uses metric=
        if metrics is not None:
            for i, name in enumerate(metrics, start=1):
                query_params[f"metric{i}"] = name
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

        query_params.update(params)

        return self._get(endpoint, params=query_params, timeout=timeout)
