import requests
from typing import Union, List, Dict, Any, Optional
from .dt_utils import debug_print, BaseEndpoint

class Analyst(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get_groups(self, **params):
        """Get AI Analyst incident groups."""
        endpoint = '/aianalyst/groups'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_incident_events(self, **params):
        """Get AI Analyst incident events."""
        endpoint = '/aianalyst/incidentevents'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def acknowledge(self, uuids: Union[str, List[str]]):
        """Acknowledge AI Analyst incident events."""
        if isinstance(uuids, list):
            uuids = ','.join(uuids)
        endpoint = '/aianalyst/acknowledge'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.client._debug(f"POST {url} data=uuid={uuids}")
        response = requests.post(url, headers=headers, params=sorted_params or , data={'uuid': uuids}, verify=False)
        return response.status_code == 200

    def unacknowledge(self, uuids: Union[str, List[str]]):
        """Unacknowledge AI Analyst incident events."""
        if isinstance(uuids, list):
            uuids = ','.join(uuids)
        endpoint = '/aianalyst/unacknowledge'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.client._debug(f"POST {url} data=uuid={uuids}")
        response = requests.post(url, headers=headers, params=sorted_params or , data={'uuid': uuids}, verify=False)
        return response.status_code == 200

    def pin(self, uuids: Union[str, List[str]]):
        """Pin AI Analyst incident events."""
        if isinstance(uuids, list):
            uuids = ','.join(uuids)
        endpoint = '/aianalyst/pin'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.client._debug(f"POST {url} data=uuid={uuids}")
        response = requests.post(url, headers=headers, params=sorted_params or , data={'uuid': uuids}, verify=False)
        return response.status_code == 200

    def unpin(self, uuids: Union[str, List[str]]):
        """Unpin AI Analyst incident events."""
        if isinstance(uuids, list):
            uuids = ','.join(uuids)
        endpoint = '/aianalyst/unpin'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.client._debug(f"POST {url} data=uuid={uuids}")
        response = requests.post(url, headers=headers, params=sorted_params or , data={'uuid': uuids}, verify=False)
        return response.status_code == 200

    def get_comments(self, incident_id: str, response_data: Optional[str] = ""):
        """Get comments for an AI Analyst incident event."""
        endpoint = '/aianalyst/incident/comments'
        params = {'incident_id': incident_id}
        if response_data:
            params['responsedata'] = response_data
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def add_comment(self, incident_id: str, message: str):
        """Add a comment to an AI Analyst incident event."""
        endpoint = '/aianalyst/incident/comments'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, Any] = {"incident_id": incident_id, "message": message}
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def get_stats(self, **params):
        """Get statistics about AI Analyst investigations, incidents and events."""
        endpoint = '/aianalyst/stats'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json() 