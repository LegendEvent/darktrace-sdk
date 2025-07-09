import requests
import json
from typing import Union, List, Dict, Any, Optional
from .dt_utils import debug_print, BaseEndpoint

class Analyst(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get_groups(self, **params):
        """Get AI Analyst incident groups.
        
        Available parameters:
        - includeacknowledged (bool): Include acknowledged events in the data
        - includeonlypinned (bool): False by default. Used to only return pinned incident events
        - locale (str): Language for returned strings (de_DE, en_GB, en_US, es_ES, es_419, fr_FR, it_IT, ja_JP, ko_KR, pt_BR, zh_Hans, zh_Hant)
        - endtime (int): End time in millisecond format, relative to midnight January 1st 1970 UTC
        - starttime (int): Start time in millisecond format, relative to midnight January 1st 1970 UTC
        - groupcompliance (bool): Return only events that are part of incidents with "compliance" behavior category
        - groupsuspicious (bool): Return only events that are part of incidents with "suspicious" behavior category
        - groupcritical (bool): Return only events that are part of incidents with "critical" behavior category
        - maxscore (int): Maximum score an incident can possess (0-100)
        - minscore (int): Minimum score an incident can possess (0-100)
        - did (int): Device ID to include incident events for
        - excludedid (int): Device ID to exclude incident events for
        - sid (int): Subnet ID to include incident events for
        - excludesid (int): Subnet ID to exclude incident events for
        - master (int): Master instance ID under Unified View
        - saasonly (bool): Restricts returned incidents to only those with SaaS activity
        - groupid (str): Unique identifier of an AI Analyst incident
        """
        endpoint = '/aianalyst/groups'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_incident_events(self, **params):
        """Get AI Analyst incident events.
        
        Available parameters:
        - includeacknowledged (bool): Include acknowledged events in the data
        - includeallpinned (bool): True by default. Controls whether pinned events are returned
        - includeonlypinned (bool): False by default. Used to only return pinned incident events
        - includeincidenteventurl (bool): Controls whether links to events are included in the response
        - locale (str): Language for returned strings (de_DE, en_GB, en_US, es_ES, es_419, fr_FR, it_IT, ja_JP, ko_KR, pt_BR, zh_Hans, zh_Hant)
        - endtime (int): End time in millisecond format, relative to midnight January 1st 1970 UTC
        - starttime (int): Start time in millisecond format, relative to midnight January 1st 1970 UTC
        - groupcompliance (bool): Return only events that are part of incidents with "compliance" behavior category
        - groupsuspicious (bool): Return only events that are part of incidents with "suspicious" behavior category
        - groupcritical (bool): Return only events that are part of incidents with "critical" behavior category
        - maxscore (int): Maximum score an event can possess (0-100)
        - minscore (int): Minimum score an event can possess (0-100)
        - maxgroupscore (int): Maximum incident score for the incident (0-100)
        - mingroupscore (int): Minimum incident score for the incident (0-100)
        - did (int): Device ID to include incident events for
        - excludedid (int): Device ID to exclude incident events for
        - sid (int): Subnet ID to include incident events for
        - excludesid (int): Subnet ID to exclude incident events for
        - master (int): Master instance ID under Unified View
        - saasonly (bool): Restricts returned events to only those with SaaS activity
        - groupid (str): Unique identifier of an AI Analyst incident
        - uuid (str): Unique identifier of an AI Analyst incident event
        """
        endpoint = '/aianalyst/incidentevents'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def acknowledge(self, uuids: Union[str, List[str]]) -> dict:
        """
            Acknowledge AI Analyst incident events.
        
            Returns: Full Darktrace return JSON
        """
        if isinstance(uuids, list):
            uuids = ','.join(uuids)
        endpoint = '/aianalyst/acknowledge'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.client._debug(f"POST {url} data=uuid={uuids}")
        response = requests.post(url, headers=headers, params=sorted_params, data={'uuid': uuids}, verify=False)
        response.raise_for_status()
        return response.json()

    def unacknowledge(self, uuids: Union[str, List[str]]) -> dict:
        """
        Unacknowledge AI Analyst incident events.
        
        returns: Full Darktrace return JSON
        """
        if isinstance(uuids, list):
            uuids = ','.join(uuids)
        endpoint = '/aianalyst/unacknowledge'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.client._debug(f"POST {url} data=uuid={uuids}")
        response = requests.post(url, headers=headers, params=sorted_params, data={'uuid': uuids}, verify=False)
        response.raise_for_status()
        return response.json()

    def pin(self, uuids: Union[str, List[str]]) -> dict:
        """
        Pin AI Analyst incident events.

        Returns: Full Darktrace return JSON
        """
        if isinstance(uuids, list):
            uuids = ','.join(uuids)
        endpoint = '/aianalyst/pin'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.client._debug(f"POST {url} data=uuid={uuids}")
        response = requests.post(url, headers=headers, params=sorted_params, data={'uuid': uuids}, verify=False)
        response.raise_for_status()
        return response.json()

    def unpin(self, uuids: Union[str, List[str]]) -> dict:
        """
        Unpin AI Analyst incident events.

        Returns: Full Darktrace return JSON
        """
        if isinstance(uuids, list):
            uuids = ','.join(uuids)
        endpoint = '/aianalyst/unpin'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.client._debug(f"POST {url} data=uuid={uuids}")
        response = requests.post(url, headers=headers, params=sorted_params, data={'uuid': uuids}, verify=False)
        response.raise_for_status()
        return response.json()

    def get_comments(self, incident_id: str, response_data: Optional[str] = ""):
        """Get comments for an AI Analyst incident event.
        
        Parameters:
        - incident_id (str): Unique identifier for the AI Analyst event to return comments for
        - response_data (str): When given the name of a top-level field or object, restricts the returned JSON to only that field or object
        """
        endpoint = '/aianalyst/incident/comments'
        params = {'incident_id': incident_id}
        if response_data:
            params['responsedata'] = response_data
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def add_comment(self, incident_id: str, message: str) -> dict:
        """Add a comment to an AI Analyst incident event.
        
        Parameters:
        - incident_id (str): Unique identifier for the AI Analyst event
        - message (str): Text that should be added as a comment to the AI Analyst incident event
        """
        endpoint = '/aianalyst/incident/comments'
        url = f"{self.client.host}{endpoint}"
        body: Dict[str, Any] = {"incident_id": incident_id, "message": message}
        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        self.client._debug(f"POST {url} body={body}")
        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()

    def get_stats(self, **params):
        """Get AI Analyst statistics.
        
        Available parameters:
        - includeacknowledged (bool): Include acknowledged events in the data
        - endtime (int): End time in millisecond format, relative to midnight January 1st 1970 UTC
        - starttime (int): Start time in millisecond format, relative to midnight January 1st 1970 UTC
        - groupcompliance (bool): Return only events that are part of incidents with "compliance" behavior category
        - groupsuspicious (bool): Return only events that are part of incidents with "suspicious" behavior category
        - groupcritical (bool): Return only events that are part of incidents with "critical" behavior category
        - did (int): Device ID to include incident events for
        - excludedid (int): Device ID to exclude incident events for
        - sid (int): Subnet ID to include incident events for
        - excludesid (int): Subnet ID to exclude incident events for
        - master (int): Master instance ID under Unified View
        - saasonly (bool): Restricts returned events to only those with SaaS activity
        """
        endpoint = '/aianalyst/stats'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_investigations(self, **params):
        """Get AI Analyst investigations (GET request).
        
        Available parameters:
        - includeacknowledged (bool): Include acknowledged events in the data
        - endtime (int): End time in millisecond format, relative to midnight January 1st 1970 UTC
        - starttime (int): Start time in millisecond format, relative to midnight January 1st 1970 UTC
        - did (int): Device ID to include investigation events for
        - excludedid (int): Device ID to exclude investigation events for
        - sid (int): Subnet ID to include investigation events for
        - excludesid (int): Subnet ID to exclude investigation events for
        - pbid (int): Playbook ID that the search is filtered to. 0 for all Playbooks, null for built-in only
        - minfirstreporttime (int): Earliest first report time for investigation in millisecond format
        - maxfirstreporttime (int): Latest first report time for investigation in millisecond format
        - maxlastreporttime (int): Latest last report time for investigation in millisecond format
        - minlastreporttime (int): Earliest last report time for investigation in millisecond format
        - includefirstreports (bool): Include first reports along with the investigation data
        - investigationid (str): Unique identifier of an AI Analyst investigation
        """
        endpoint = '/aianalyst/investigations'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
        response.raise_for_status()
        return response.json()

    def create_investigation(self, investigate_time: str, did: int):
        """Create a new AI Analyst investigation (POST request).
        
        Parameters:
        - investigate_time (str): The time that the investigation should focus around (epoch timestamp)
        - did (int): The device that an investigation should be created for
        """
        endpoint = '/aianalyst/investigations'
        url = f"{self.client.host}{endpoint}"
        
        # Prepare the JSON body
        body = {
            "investigateTime": investigate_time,
            "did": did
        }
        
        # For POST requests with JSON body, include it in signature
        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        
        self.client._debug(f"POST {url} json={body}")
        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()