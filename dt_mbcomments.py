import requests
from typing import Optional
from .utils import debug_print

class MBComments:
    def __init__(self, client):
        self.client = client

    def get(self, comment_id: Optional[str] = None, response_data: Optional[str] = None, **params):
        """Get model breach comments or details for a specific comment."""
        endpoint = f'/mbcomments{f"/{comment_id}" if comment_id else ""}'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        if response_data:
            params['responsedata'] = response_data
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    def post(self, breach_id: str, comment: str, **params):
        """Add a comment to a model breach."""
        endpoint = '/mbcomments'
        url = f"{self.client.host}{endpoint}"
        headers = self.client.auth.get_headers(endpoint)
        data = {'breachid': breach_id, 'comment': comment}
        data.update(params)
        self.client._debug(f"POST {url} data={data}")
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        return response.json() 