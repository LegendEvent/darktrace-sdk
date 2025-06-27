import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Status(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self,
            includechildren: Optional[bool] = None,
            fast: Optional[bool] = None,
            responsedata: Optional[str] = None
        ):
        """
        Get detailed system health and status information from Darktrace.

        Args:
            includechildren (bool, optional): Whether to include information about probes (children). True by default.
            fast (bool, optional): When true, returns data faster but may omit subnet connectivity information if not cached.
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field(s) or object(s).

        Returns:
            dict: System health and status information from Darktrace.
        """
        endpoint = '/status'
        url = f"{self.client.host}{endpoint}"

        params = dict()
        if includechildren is not None:
            params['includechildren'] = includechildren
        if fast is not None:
            params['fast'] = fast
        if responsedata is not None:
            params['responsedata'] = responsedata

        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()