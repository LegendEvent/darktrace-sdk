import requests
import json
from typing import Dict, Any, Optional, Union, List
from .dt_utils import debug_print, BaseEndpoint

class DarktraceEmail(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def decode_link(self, link: str) -> Dict[str, Any]:
        """
        Decode a link using the Darktrace/Email API.

        Args:
            link (str): The encoded link to decode.

        Returns:
            dict: Decoded link information.
        Example:
            email.decode_link(link="https://...encoded...")
        """
        endpoint = '/agemail/api/ep/api/v1.0/admin/decode_link'
        url = f"{self.client.host}{endpoint}"
        params = {"link": link}
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_action_summary(self, days: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get action summary from Darktrace/Email API.

        Args:
            days (int, optional): Number of days to include in the summary.
            limit (int, optional): Limit the number of results.

        Returns:
            dict: Action summary data.
        Example:
            email.get_action_summary(days=7, limit=10)
        """
        endpoint = '/agemail/api/ep/api/v1.0/dash/action_summary'
        url = f"{self.client.host}{endpoint}"
        params = {}
        if days is not None:
            params["days"] = days
        if limit is not None:
            params["limit"] = limit
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_dash_stats(self, days: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get dashboard stats from Darktrace/Email API.

        Args:
            days (int, optional): Number of days to include in the stats.
            limit (int, optional): Limit the number of results.

        Returns:
            dict: Dashboard statistics.
        Example:
            email.get_dash_stats(days=28, limit=2)
        """
        endpoint = '/agemail/api/ep/api/v1.0/dash/dash_stats'
        url = f"{self.client.host}{endpoint}"
        params = {}
        if days is not None:
            params["days"] = days
        if limit is not None:
            params["limit"] = limit
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_data_loss(self, days: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get data loss information from Darktrace/Email API.

        Args:
            days (int, optional): Number of days to include in the data loss stats.
            limit (int, optional): Limit the number of results.

        Returns:
            dict: Data loss information.
        Example:
            email.get_data_loss(days=7, limit=5)
        """
        endpoint = '/agemail/api/ep/api/v1.0/dash/data_loss'
        url = f"{self.client.host}{endpoint}"
        params = {}
        if days is not None:
            params["days"] = days
        if limit is not None:
            params["limit"] = limit
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_user_anomaly(self, days: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get user anomaly data from Darktrace/Email API.

        Args:
            days (int, optional): Number of days to include in the anomaly stats.
            limit (int, optional): Limit the number of results.

        Returns:
            dict: User anomaly data.
        Example:
            email.get_user_anomaly(days=28, limit=2)
        """
        endpoint = '/agemail/api/ep/api/v1.0/dash/user_anomaly'
        url = f"{self.client.host}{endpoint}"
        params = {}
        if days is not None:
            params["days"] = days
        if limit is not None:
            params["limit"] = limit
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def email_action(self, uuid: str, data: Dict[str, Any]):
        """Perform an action on an email by UUID in Darktrace/Email API."""
        endpoint = f'/agemail/api/ep/api/v1.0/emails/{uuid}/action'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, json_body=data)
        headers['Content-Type'] = 'application/json'
        self.client._debug(f"POST {url} data={data}")
        response = requests.post(url, headers=headers, data=json.dumps(data, separators=(',', ':')), verify=False)
        self.client._debug(f"Response status: {response.status_code}")
        self.client._debug(f"Response text: {response.text}")
        response.raise_for_status()
        return response.json()

    def get_email(self, uuid: str, include_headers: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get email details by UUID from Darktrace/Email API.

        Args:
            uuid (str): Email UUID.
            include_headers (bool, optional): Whether to include email headers in the response.

        Returns:
            dict: Email details.
        Example:
            email.get_email(uuid="...", include_headers=True)
        """
        endpoint = f'/agemail/api/ep/api/v1.0/emails/{uuid}'
        url = f"{self.client.host}{endpoint}"
        params = {}
        if include_headers is not None:
            params["include_headers"] = include_headers
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def download_email(self, uuid: str) -> bytes:
        """
        Download an email by UUID from Darktrace/Email API.

        Args:
            uuid (str): Email UUID.

        Returns:
            bytes: Raw email content (MIME).
        Example:
            email.download_email(uuid="...")
        """
        endpoint = f'/agemail/api/ep/api/v1.0/emails/{uuid}/download'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={{}}")
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.content

    def search_emails(self, data: Dict[str, Any]):
        """Search emails in Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/emails/search'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, json_body=data)
        headers['Content-Type'] = 'application/json'
        self.client._debug(f"POST {url} data={data}")
        response = requests.post(url, headers=headers, data=json.dumps(data, separators=(',', ':')), verify=False)
        self.client._debug(f"Response status: {response.status_code}")
        self.client._debug(f"Response text: {response.text}")
        response.raise_for_status()
        return response.json()

    def get_tags(self) -> Dict[str, Any]:
        """
        Get tags from Darktrace/Email API.

        Returns:
            dict: Tags data.
        Example:
            email.get_tags()
        """
        endpoint = '/agemail/api/ep/api/v1.0/resources/tags'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={{}}")
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def get_actions(self) -> Dict[str, Any]:
        """
        Get actions from Darktrace/Email API.

        Returns:
            dict: Actions data.
        Example:
            email.get_actions()
        """
        endpoint = '/agemail/api/ep/api/v1.0/resources/actions'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={{}}")
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def get_filters(self) -> Dict[str, Any]:
        """
        Get filters from Darktrace/Email API.

        Returns:
            dict: Filters data.
        Example:
            email.get_filters()
        """
        endpoint = '/agemail/api/ep/api/v1.0/resources/filters'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={{}}")
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def get_event_types(self) -> Dict[str, Any]:
        """
        Get audit event types from Darktrace/Email API.

        Returns:
            dict: Audit event types.
        Example:
            email.get_event_types()
        """
        endpoint = '/agemail/api/ep/api/v1.0/system/audit/eventTypes'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={{}}")
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def get_audit_events(self, event_type: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """
        Get audit events from Darktrace/Email API.

        Args:
            event_type (str, optional): Filter by event type.
            limit (int, optional): Limit the number of results.
            offset (int, optional): Offset for pagination.

        Returns:
            dict: Audit events data.
        Example:
            email.get_audit_events(event_type="login", limit=10, offset=0)
        """
        endpoint = '/agemail/api/ep/api/v1.0/system/audit/events'
        url = f"{self.client.host}{endpoint}"
        params = {}
        if event_type is not None:
            params["eventType"] = event_type
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()