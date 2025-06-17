import requests
from typing import Dict, Any, Union, Optional, List
from .dt_utils import debug_print

class Antigena:
    def __init__(self, client):
        self.client = client

    def get_actions(self, **params):
        """Get information about current and past Antigena actions."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def approve_action(self, code_id: int, reason: str = "", duration: int = 0) -> bool:
        """Approve/activate a pending Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
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
        headers = self.client.auth.get_headers(endpoint)
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
        headers = self.client.auth.get_headers(endpoint)
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
        headers = self.client.auth.get_headers(endpoint)
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
        headers = self.client.auth.get_headers(endpoint)
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
        """Get a summary of active and pending Antigena actions."""
        endpoint = '/antigena/summary'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 