import requests
from .utils import debug_print

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

    def approve_action(self, code_id: int, reason: str = None, duration: int = None) -> bool:
        """Approve/activate a pending Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body = {"codeid": code_id, "activate": True}
        if reason:
            body["reason"] = reason
        if duration:
            body["duration"] = duration
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def extend_action(self, code_id: int, duration: int, reason: str = None) -> bool:
        """Extend an active Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body = {"codeid": code_id, "duration": duration}
        if reason:
            body["reason"] = reason
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def clear_action(self, code_id: int, reason: str = None) -> bool:
        """Clear an active, pending or expired Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body = {"codeid": code_id, "clear": True}
        if reason:
            body["reason"] = reason
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def reactivate_action(self, code_id: int, duration: int, reason: str = None) -> bool:
        """Reactivate a cleared or expired Antigena action."""
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body = {"codeid": code_id, "activate": True, "duration": duration}
        if reason:
            body["reason"] = reason
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        return response.status_code == 200

    def create_manual_action(self, did: int, action: str, duration: int, reason: str = "", connections=None) -> int:
        """Create a manual Antigena action."""
        endpoint = '/antigena/manual'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        body = {"did": did, "action": action, "duration": duration, "reason": reason}
        if action == 'connection' and connections:
            body["connections"] = connections
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        if response.status_code == 200:
            return response.json().get('code')
        return None

    def get_summary(self, **params):
        """Get a summary of active and pending Antigena actions."""
        endpoint = '/antigena/summary'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json() 