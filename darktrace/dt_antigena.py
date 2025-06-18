import requests
from typing import Dict, Any, Union, Optional, List
from .dt_utils import debug_print, BaseEndpoint

class Antigena(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get_actions(self, **params):
        """Get information about current and past Antigena actions.
        
        Parameters for GET requests:
            fulldevicedetails (bool): Returns full device detail objects for all referenced devices
            includecleared (bool): Returns all actions including cleared ones (default: false)
            includehistory (bool): Include additional history information about action states
            needconfirming (bool): Filter actions by those needing human confirmation
            endtime (int): End time in milliseconds since epoch
            from_time (str): Start time in YYYY-MM-DD HH:MM:SS format
            starttime (int): Start time in milliseconds since epoch
            to_time (str): End time in YYYY-MM-DD HH:MM:SS format
            includeconnections (bool): Add connections object with blocked connections
            responsedata (str): Restrict response to specific fields/objects
            pbid (int): Only return actions for specific model breach ID
        """
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        
        # Handle special parameter names
        if 'from_time' in params:
            params['from'] = params.pop('from_time')
        if 'to_time' in params:
            params['to'] = params.pop('to_time')
            
        # Get headers and sorted parameters for authentication
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

    def approve_action(self, code_id: int, reason: str = "", duration: int = 0) -> bool:
        """Approve/activate a pending Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, Any] = {"codeid": code_id, "activate": True}
        if reason:
            body["reason"] = reason
        if duration:
            body["duration"] = duration
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def extend_action(self, code_id: int, duration: int, reason: str = "") -> bool:
        """Extend an active Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, Any] = {"codeid": code_id, "duration": duration}
        if reason:
            body["reason"] = reason
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def clear_action(self, code_id: int, reason: str = "") -> bool:
        """Clear an active, pending or expired Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, Any] = {"codeid": code_id, "clear": True}
        if reason:
            body["reason"] = reason
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def reactivate_action(self, code_id: int, duration: int, reason: str = "") -> bool:
        """Reactivate a cleared or expired Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, Any] = {"codeid": code_id, "activate": True, "duration": duration}
        if reason:
            body["reason"] = reason
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def create_manual_action(self, did: int, action: str, duration: int, reason: str = "", connections: Optional[List] = None) -> int:
        """Create a manual Antigena action."""
        endpoint = '/antigena/manual'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        body: Dict[str, Any] = {"did": did, "action": action, "duration": duration, "reason": reason}
        if action == 'connection' and connections:
            body["connections"] = connections
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        if response.status_code == 200:
            # Ensure we get an integer value from the response
            result = response.json()
            return int(result.get('code', 0))
        return 0

    def get_summary(self, **params):
        """Get a summary of active and pending Antigena actions.
        
        Parameters for GET requests:
            endtime (int): End time in milliseconds since epoch
            starttime (int): Start time in milliseconds since epoch
            responsedata (str): Restrict response to specific fields/objects
            
        Notes:
            - Time parameters must be specified in pairs
            - Historic pending action information is not available
            - Returns device IDs (did) which can be used to query /devices for more info
        """
        endpoint = '/antigena/summary'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()