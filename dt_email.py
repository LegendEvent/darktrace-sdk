import requests
from .utils import debug_print

class DarktraceEmail:
    def __init__(self, client):
        self.client = client

    def decode_link(self, **params):
        """Decode a link using the Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/admin/decode_link'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_action_summary(self, **params):
        """Get action summary from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/dash/action_summary'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_dash_stats(self, **params):
        """Get dashboard stats from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/dash/dash_stats'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_data_loss(self, **params):
        """Get data loss information from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/dash/data_loss'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_user_anomaly(self, **params):
        """Get user anomaly data from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/dash/user_anomaly'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def email_action(self, uuid: str, data: dict):
        """Perform an action on an email by UUID in Darktrace/Email API."""
        endpoint = f'/agemail/api/ep/api/v1.0/emails/{uuid}/action'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"POST {url} data={data}")
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        return response.json()

    def get_email(self, uuid: str, **params):
        """Get email details by UUID from Darktrace/Email API."""
        endpoint = f'/agemail/api/ep/api/v1.0/emails/{uuid}'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def download_email(self, uuid: str, **params):
        """Download an email by UUID from Darktrace/Email API."""
        endpoint = f'/agemail/api/ep/api/v1.0/emails/{uuid}/download'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.content

    def search_emails(self, data: dict):
        """Search emails in Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/emails/search'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"POST {url} data={data}")
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        return response.json()

    def get_tags(self, **params):
        """Get tags from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/resources/tags'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_actions(self, **params):
        """Get actions from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/resources/actions'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_filters(self, **params):
        """Get filters from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/resources/filters'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_event_types(self, **params):
        """Get audit event types from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/system/audit/eventTypes'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_audit_events(self, **params):
        """Get audit events from Darktrace/Email API."""
        endpoint = '/agemail/api/ep/api/v1.0/system/audit/events'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 