from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["SummaryStatistics"]


class SummaryStatistics(BaseEndpoint):
    def get(
        self,
        responsedata: str | None = None,
        eventtype: str | None = None,
        endtime: int | None = None,
        to: str | None = None,
        hours: int | None = None,
        csensor: bool | None = None,
        mitreTactics: bool | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get summary statistics information from Darktrace.

        Args:
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field(s) or object(s).
            eventtype (str, optional): Changes the format of data to return numeric event counts for any of the four categories of events and/or three types (see docs).
            endtime (int, optional): End time of data to return in ms since epoch (UTC). Requires eventtype.
            to (str, optional): End time of data to return in 'YYYY-MM-DD HH:MM:SS' format. Requires eventtype.
            hours (int, optional): Number of hour intervals from the end time (or current time) to return. Requires eventtype.
            csensor (bool, optional): When true, only bandwidth statistics for cSensor agents are returned. When false, statistics for Darktrace/Network bandwidth.
            mitreTactics (bool, optional): When true, alters the returned data to display MITRE ATT&CK Framework breakdown.
            timeout (float or tuple, optional): Request timeout in seconds. Can be a single value or (connect_timeout, read_timeout).

        Returns:
            dict: Summary statistics information from Darktrace.

        Raises:
            ValueError: If more than one of ``eventtype``, ``csensor`` and ``mitreTactics`` is
                given, or if ``endtime``, ``to`` or ``hours`` is used without ``eventtype``
                (both rules are from the API guide).
        """
        selectors = [
            n
            for n, v in (("eventtype", eventtype), ("csensor", csensor), ("mitreTactics", mitreTactics))
            if v is not None
        ]
        if len(selectors) > 1:
            raise ValueError(f"Only one of eventtype, csensor or mitreTactics may be used, got: {', '.join(selectors)}")
        if eventtype is None:
            time_args = [n for n, v in (("endtime", endtime), ("to", to), ("hours", hours)) if v is not None]
            if time_args:
                raise ValueError(f"{', '.join(time_args)} require eventtype")
        params = {}
        if responsedata is not None:
            params["responsedata"] = responsedata
        if eventtype is not None:
            params["eventtype"] = eventtype
        if endtime is not None:
            params["endtime"] = endtime
        if to is not None:
            params["to"] = to
        if hours is not None:
            params["hours"] = hours
        if csensor is not None:
            params["csensor"] = csensor
        if mitreTactics is not None:
            params["mitreTactics"] = mitreTactics
        return self._get("/summarystatistics", params=params, timeout=timeout)
