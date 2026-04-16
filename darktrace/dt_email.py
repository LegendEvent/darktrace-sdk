from __future__ import annotations

from typing import Any

from .dt_utils import _UNSET, BaseEndpoint
from .exceptions import _raise_for_status

__all__ = ["DarktraceEmail"]


class DarktraceEmail(BaseEndpoint):
    def decode_link(self, link: str, timeout: float | tuple[float, float] | None = _UNSET) -> dict | list:
        """
        Decode a link using the Darktrace/Email API.

        Args:
            link (str): The encoded link to decode.
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Decoded link information.
        Example:
            email.decode_link(link="https://...encoded...")
        """
        endpoint = "/agemail/api/ep/api/v1.0/admin/decode_link"
        params = {"link": link}
        return self._get(endpoint, params=params, timeout=timeout)

    def _dashboard_get(
        self,
        path_suffix: str,
        days: int | None = None,
        limit: int | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        endpoint = f"/agemail/api/ep/api/v1.0/dash/{path_suffix}"
        params = {}
        if days is not None:
            params["days"] = days
        if limit is not None:
            params["limit"] = limit
        return self._get(endpoint, params=params, timeout=timeout)

    def get_action_summary(
        self,
        days: int | None = None,
        limit: int | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get action summary from Darktrace/Email API.

        Args:
            days (int, optional): Number of days to include in the summary.
            limit (int, optional): Limit the number of results.
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Action summary data.
        Example:
            email.get_action_summary(days=7, limit=10)
        """
        return self._dashboard_get("action_summary", days=days, limit=limit, timeout=timeout)

    def get_dash_stats(
        self,
        days: int | None = None,
        limit: int | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get dashboard stats from Darktrace/Email API.

        Args:
            days (int, optional): Number of days to include in the stats.
            limit (int, optional): Limit the number of results.
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Dashboard statistics.
        Example:
            email.get_dash_stats(days=28, limit=2)
        """
        return self._dashboard_get("dash_stats", days=days, limit=limit, timeout=timeout)

    def get_data_loss(
        self,
        days: int | None = None,
        limit: int | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get data loss information from Darktrace/Email API.

        Args:
            days (int, optional): Number of days to include in the data loss stats.
            limit (int, optional): Limit the number of results.
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Data loss information.
        Example:
            email.get_data_loss(days=7, limit=5)
        """
        return self._dashboard_get("data_loss", days=days, limit=limit, timeout=timeout)

    def get_user_anomaly(
        self,
        days: int | None = None,
        limit: int | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get user anomaly data from Darktrace/Email API.

        Args:
            days (int, optional): Number of days to include in the anomaly stats.
            limit (int, optional): Limit the number of results.
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: User anomaly data.
        Example:
            email.get_user_anomaly(days=28, limit=2)
        """
        return self._dashboard_get("user_anomaly", days=days, limit=limit, timeout=timeout)

    def email_action(
        self,
        uuid: str,
        data: dict[str, Any],
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict:
        """Perform an action on an email by UUID in Darktrace/Email API."""
        endpoint = f"/agemail/api/ep/api/v1.0/emails/{uuid}/action"
        return self._post_json(endpoint, body=data, timeout=timeout)

    def get_email(
        self,
        uuid: str,
        include_headers: bool | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get email details by UUID from Darktrace/Email API.

        Args:
            uuid (str): Email UUID.
            include_headers (bool, optional): Whether to include email headers in the response.
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Email details.
        Example:
            email.get_email(uuid="...", include_headers=True)
        """
        endpoint = f"/agemail/api/ep/api/v1.0/emails/{uuid}"
        params = {}
        if include_headers is not None:
            params["include_headers"] = include_headers
        return self._get(endpoint, params=params, timeout=timeout)

    def download_email(self, uuid: str, timeout: float | tuple[float, float] | None = _UNSET) -> bytes:
        """
        Download an email by UUID from Darktrace/Email API.

        Args:
            uuid (str): Email UUID.
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            bytes: Raw email content (MIME).
        Example:
            email.download_email(uuid="...")
        """
        endpoint = f"/agemail/api/ep/api/v1.0/emails/{uuid}/download"
        headers, sorted_params = self._get_headers(endpoint)
        url = f"{self.client.host}{endpoint}"
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET",
            url,
            headers=headers,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        _raise_for_status(response, method="GET", url=url)
        return response.content

    def search_emails(
        self,
        data: dict[str, Any],
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """Search emails in Darktrace/Email API."""
        endpoint = "/agemail/api/ep/api/v1.0/emails/search"
        return self._post_json(endpoint, body=data, timeout=timeout)

    def get_tags(self, timeout: float | tuple[float, float] | None = _UNSET) -> dict | list:
        """
        Get tags from Darktrace/Email API.

        Args:
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Tags data.
        Example:
            email.get_tags()
        """
        endpoint = "/agemail/api/ep/api/v1.0/resources/tags"
        return self._get(endpoint, timeout=timeout)

    def get_actions(self, timeout: float | tuple[float, float] | None = _UNSET) -> dict | list:
        """
        Get actions from Darktrace/Email API.

        Args:
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Actions data.
        Example:
            email.get_actions()
        """
        endpoint = "/agemail/api/ep/api/v1.0/resources/actions"
        return self._get(endpoint, timeout=timeout)

    def get_filters(self, timeout: float | tuple[float, float] | None = _UNSET) -> dict | list:
        """
        Get filters from Darktrace/Email API.

        Args:
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Filters data.
        Example:
            email.get_filters()
        """
        endpoint = "/agemail/api/ep/api/v1.0/resources/filters"
        return self._get(endpoint, timeout=timeout)

    def get_event_types(self, timeout: float | tuple[float, float] | None = _UNSET) -> dict | list:
        """
        Get audit event types from Darktrace/Email API.

        Args:
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Audit event types.
        Example:
            email.get_event_types()
        """
        endpoint = "/agemail/api/ep/api/v1.0/system/audit/eventTypes"
        return self._get(endpoint, timeout=timeout)

    def get_audit_events(
        self,
        event_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get audit events from Darktrace/Email API.

        Args:
            event_type (str, optional): Filter by event type.
            limit (int, optional): Limit the number of results.
            offset (int, optional): Offset for pagination.
            timeout (float, tuple[float, float], optional): Request timeout in seconds.

        Returns:
            dict: Audit events data.
        Example:
            email.get_audit_events(event_type="login", limit=10, offset=0)
        """
        endpoint = "/agemail/api/ep/api/v1.0/system/audit/events"
        params = {}
        if event_type is not None:
            params["eventType"] = event_type
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._get(endpoint, params=params, timeout=timeout)
