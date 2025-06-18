import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Components(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, cid: Optional[int] = None, responsedata: Optional[str] = None, **params):
        """
        Get information about model components.

        Parameters:
            cid (int, optional): Component ID to retrieve a specific component. If None, returns all components.
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field or object.
            **params: Additional parameters for future compatibility.

        Returns:
            dict or list: API response containing component(s) data.

        Example:
            get()                # Get all components
            get(cid=1234)        # Get component with ID 1234
            get(responsedata='filters')  # Only return the 'filters' field for all components
        """
        endpoint = f'/components{f"/{cid}" if cid is not None else ""}'
        # Add responsedata to params if provided
        if responsedata is not None:
            params['responsedata'] = responsedata
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()