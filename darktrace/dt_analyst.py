from typing import Any, Dict, List, Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Analyst"]


class Analyst(BaseEndpoint):
    """AI Analyst endpoint (/aianalyst).

    Retrieve, acknowledge, pin, and comment on AI Analyst incident groups and events.
    """

    def get_groups(self, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET, **params) -> Any:
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
        endpoint = "/aianalyst/groups"
        headers, sorted_params = self._get_headers(endpoint, params)
        resolved_timeout = self._resolve_timeout(timeout)

        response = self._make_request(
            "GET",
            f"{self.client.host}{endpoint}",
            headers=headers,
            params=sorted_params or params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_incident_events(self, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET, **params) -> Any:
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
        endpoint = "/aianalyst/incidentevents"
        headers, sorted_params = self._get_headers(endpoint, params)
        resolved_timeout = self._resolve_timeout(timeout)

        response = self._make_request(
            "GET",
            f"{self.client.host}{endpoint}",
            headers=headers,
            params=sorted_params or params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def acknowledge(
        self,
        uuids: Union[str, List[str]],
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
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
        uuids: Union[str, List[str]],
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
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
        uuids: Union[str, List[str]],
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
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
        uuids: Union[str, List[str]],
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
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
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
        response_data: Optional[str] = "",
    ) -> Any:
        """Get comments for an AI Analyst incident event.

        Args:
            incident_id: Unique identifier for the AI Analyst event.
            response_data: Restrict returned JSON to specific fields.
        """
        endpoint = "/aianalyst/incident/comments"
        params: Dict[str, Any] = {"incident_id": incident_id}
        if response_data:
            params["responsedata"] = response_data
        return self._get(endpoint, params=params, timeout=timeout)

    def add_comment(
        self,
        incident_id: str,
        message: str,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
        """Add a comment to an AI Analyst incident event.

        Args:
            incident_id: Unique identifier for the AI Analyst event.
            message: Text to add as a comment.

        Returns:
            dict: Full Darktrace API response.
        """
        body: Dict[str, Any] = {"incident_id": incident_id, "message": message}
        return self._post_json("/aianalyst/incident/comments", body=body, timeout=timeout)

    def get_stats(self, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET, **params) -> Any:
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
        endpoint = "/aianalyst/stats"
        headers, sorted_params = self._get_headers(endpoint, params)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET",
            f"{self.client.host}{endpoint}",
            headers=headers,
            params=sorted_params or params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_investigations(self, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET, **params) -> Any:
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
        endpoint = "/aianalyst/investigations"
        headers, sorted_params = self._get_headers(endpoint, params)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET",
            f"{self.client.host}{endpoint}",
            headers=headers,
            params=sorted_params or params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def create_investigation(
        self,
        investigate_time: str,
        did: int,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
        """Create a new AI Analyst investigation.

        Args:
            investigate_time: Epoch timestamp to focus the investigation around.
            did: Device ID to investigate.

        Returns:
            dict: Full Darktrace API response.
        """
        body = {"investigateTime": investigate_time, "did": did}
        return self._post_json("/aianalyst/investigations", body=body, timeout=timeout)
