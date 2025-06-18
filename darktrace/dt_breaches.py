import requests
from typing import Dict, Any, Optional, Union
from datetime import datetime
from .dt_utils import debug_print, BaseEndpoint

class ModelBreaches(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, **params):
        """Get model breach alerts.
        
        Parameters:
            deviceattop (bool): Return device JSON at top-level (default: True)
            did (int): Device ID to filter by
            endtime (int): End time in milliseconds since epoch
            expandenums (bool): Expand numeric enums to strings
            from_time (str): Start time in YYYY-MM-DD HH:MM:SS format
            historicmodelonly (bool): Return only historic model details
            includeacknowledged (bool): Include acknowledged breaches
            includebreachurl (bool): Include breach URLs in response
            minimal (bool): Reduce data returned (default: False for API)
            minscore (float): Minimum breach score filter
            pbid (int): Specific breach ID to return
            pid (int): Filter by model ID
            starttime (int): Start time in milliseconds since epoch
            to_time (str): End time in YYYY-MM-DD HH:MM:SS format
            uuid (str): Filter by model UUID
            responsedata (str): Restrict response to specific fields
            saasonly (bool): Return only SaaS breaches
            group (str): Group results (e.g. 'device')
            includesuppressed (bool): Include suppressed breaches
            saasfilter (str): Filter by SaaS platform
            creationtime (bool): Use creation time for filtering
        """
        endpoint = '/modelbreaches'
        
        # Handle special parameter names
        if 'from_time' in params:
            params['from'] = params.pop('from_time')
        if 'to_time' in params:
            params['to'] = params.pop('to_time')
            
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(
            url,
            headers=headers,
            params=sorted_params,
            verify=False
        )
        response.raise_for_status()
        return response.json()

    def get_comments(self, pbid: int, **params):
        """Get comments for a specific model breach alert."""
        endpoint = f'/modelbreaches/{pbid}/comments'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def add_comment(self, pbid: int, message: str):
        """Add a comment to a model breach alert."""
        endpoint = f'/modelbreaches/{pbid}/comments'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, Any] = {'message': message}
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def acknowledge(self, pbid: int):
        """Acknowledge a model breach alert."""
        endpoint = f'/modelbreaches/{pbid}/acknowledge'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, bool] = {'acknowledge': True}
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def unacknowledge(self, pbid: int):
        """Unacknowledge a model breach alert."""
        endpoint = f'/modelbreaches/{pbid}/unacknowledge'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, bool] = {'unacknowledge': True}
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200