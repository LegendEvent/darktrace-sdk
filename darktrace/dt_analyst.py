from __future__ import annotations

from typing import Any

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Analyst"]


class Analyst(BaseEndpoint):
    """AI Analyst endpoint (/aianalyst).

    Retrieve, acknowledge, pin, and comment on AI Analyst incident groups and events.
    """

    def get_groups(self, timeout: float | tuple[float, float] | None = _UNSET, **params) -> dict | list:
        """Get AI Analyst incident groups.

        Available parameters:
        - includeacknowledged (bool): Include acknowledged events
        - includeonlypinned (bool): Only return pinned incident events
        - locale (str): Language for returned strings
        - endtime (int): End time in ms format
        - starttime (int): Start time in ms format
        - groupcompliance (bool): Filter by compliance category
        - groupsuspicious (bool): Filter by suspicious category
        - groupcritical (bool): Filter by critical category
        - maxscore (int): Maximum score (0-100)
        - minscore (int): Minimum score (0-100)
        - did (int): Device ID to include
        - excludedid (int): Device ID to exclude
        - sid (int): Subnet ID to include
        - excludesid (int): Subnet ID to exclude
        - master (int): Master instance ID under Unified View
        - saasonly (bool): Restrict to SaaS activity
        - groupid (str): Incident group ID
        """
        return self._get("/aianalyst/groups", params=params, timeout=timeout)

    def get_incident_events(self, timeout: float | tuple[float, float] | None = _UNSET, **params) -> dict | list:
        """Get AI Analyst incident events.

        Available parameters:
        - includeacknowledged (bool): Include acknowledged events
        - includeallpinned (bool): Controls whether pinned events are returned
        - includeonlypinned (bool): Only return pinned incident events
        - includeincidenteventurl (bool): Include links to events
        - locale (str): Language for returned strings
        - endtime (int): End time in ms format
        - starttime (int): Start time in ms format
        - groupcompliance (bool): Filter by compliance category
        - groupsuspicious (bool): Filter by suspicious category
        - groupcritical (bool): Filter by critical category
        - maxscore (int): Maximum score (0-100)
        - minscore (int): Minimum score (0-100)
        - maxgroupscore (int): Maximum incident score (0-100)
        - mingroupscore (int): Minimum incident score (0-100)
        - did (int): Device ID to include
        - excludedid (int): Device ID to exclude
        - sid (int): Subnet ID to include
        - excludesid (int): Subnet ID to exclude
        - master (int): Master instance ID under Unified View
        - saasonly (bool): Restrict to SaaS activity
        - groupid (str): Incident group ID
        - uuid (str): Incident event UUID
        """
        return self._get("/aianalyst/incidentevents", params=params, timeout=timeout)

    def acknowledge(
        self,
        uuids: str | list[str],
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict:
        """Acknowledge AI Analyst incident events.

        Args:
            uuids: Single UUID string or list of UUID strings.

        Returns:
            dict: Full Darktrace API response.
        """
        if isinstance(uuids, list):
            uuids = ",".join(uuids)
        return self._post_form(
            "/aianalyst/acknowledge",
            form_data={"uuid": uuids},
            timeout=timeout,
        )

    def unacknowledge(
        self,
        uuids: str | list[str],
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict:
        """Unacknowledge AI Analyst incident events.

        Args:
            uuids: Single UUID string or list of UUID strings.

        Returns:
            dict: Full Darktrace API response.
        """
        if isinstance(uuids, list):
            uuids = ",".join(uuids)
        return self._post_form(
            "/aianalyst/unacknowledge",
            form_data={"uuid": uuids},
            timeout=timeout,
        )

    def pin(
        self,
        uuids: str | list[str],
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict:
        """Pin AI Analyst incident events.

        Args:
            uuids: Single UUID string or list of UUID strings.

        Returns:
            dict: Full Darktrace API response.
        """
        if isinstance(uuids, list):
            uuids = ",".join(uuids)
        return self._post_form(
            "/aianalyst/pin",
            form_data={"uuid": uuids},
            timeout=timeout,
        )

    def unpin(
        self,
        uuids: str | list[str],
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict:
        """Unpin AI Analyst incident events.

        Args:
            uuids: Single UUID string or list of UUID strings.

        Returns:
            dict: Full Darktrace API response.
        """
        if isinstance(uuids, list):
            uuids = ",".join(uuids)
        return self._post_form(
            "/aianalyst/unpin",
            form_data={"uuid": uuids},
            timeout=timeout,
        )

    def get_comments(
        self,
        incident_id: str,
        timeout: float | tuple[float, float] | None = _UNSET,
        response_data: str | None = "",
    ) -> dict | list:
        """Get comments for an AI Analyst incident event.

        Args:
            incident_id: Unique identifier for the AI Analyst event.
            response_data: Restrict returned JSON to specific fields.
        """
        endpoint = "/aianalyst/incident/comments"
        params: dict[str, Any] = {"incident_id": incident_id}
        if response_data:
            params["responsedata"] = response_data
        return self._get(endpoint, params=params, timeout=timeout)

    def add_comment(
        self,
        incident_id: str,
        message: str,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict:
        """Add a comment to an AI Analyst incident event.

        Args:
            incident_id: Unique identifier for the AI Analyst event.
            message: Text to add as a comment.

        Returns:
            dict: Full Darktrace API response.
        """
        body: dict[str, Any] = {"incident_id": incident_id, "message": message}
        return self._post_json("/aianalyst/incident/comments", body=body, timeout=timeout)

    def get_stats(self, timeout: float | tuple[float, float] | None = _UNSET, **params) -> dict | list:
        """Get AI Analyst statistics.

        Available parameters:
        - includeacknowledged (bool): Include acknowledged events
        - endtime (int): End time in ms format
        - starttime (int): Start time in ms format
        - groupcompliance (bool): Filter by compliance category
        - groupsuspicious (bool): Filter by suspicious category
        - groupcritical (bool): Filter by critical category
        - did (int): Device ID to include
        - excludedid (int): Device ID to exclude
        - sid (int): Subnet ID to include
        - excludesid (int): Subnet ID to exclude
        - master (int): Master instance ID under Unified View
        - saasonly (bool): Restrict to SaaS activity
        """
        return self._get("/aianalyst/stats", params=params, timeout=timeout)

    def get_investigations(self, timeout: float | tuple[float, float] | None = _UNSET, **params) -> dict | list:
        """Get AI Analyst investigations.

        Available parameters:
        - includeacknowledged (bool): Include acknowledged events
        - endtime (int): End time in ms format
        - starttime (int): Start time in ms format
        - did (int): Device ID
        - excludedid (int): Device ID to exclude
        - sid (int): Subnet ID to include
        - excludesid (int): Subnet ID to exclude
        - pbid (int): Playbook ID filter
        - minfirstreporttime (int): Earliest first report time in ms
        - maxfirstreporttime (int): Latest first report time in ms
        - maxlastreporttime (int): Latest last report time in ms
        - minlastreporttime (int): Earliest last report time in ms
        - includefirstreports (bool): Include first reports
        - investigationid (str): Investigation ID
        """
        return self._get("/aianalyst/investigations", params=params, timeout=timeout)

    def create_investigation(
        self,
        investigate_time: str,
        did: int,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict:
        """Create a new AI Analyst investigation.

        Args:
            investigate_time: Epoch timestamp to focus the investigation around.
            did: Device ID to investigate.

        Returns:
            dict: Full Darktrace API response.
        """
        body = {"investigateTime": investigate_time, "did": did}
        return self._post_json("/aianalyst/investigations", body=body, timeout=timeout)
