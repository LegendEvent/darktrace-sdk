import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Enums(BaseEndpoint):
    """
    Interact with the /enums endpoint of the Darktrace API.
    The /enums endpoint returns string values for numeric codes (enumerated types) used in many API responses.
    The list of enums can be filtered using the responsedata parameter.
    """
    def __init__(self, client):
        super().__init__(client)

    def get(self, responsedata: Optional[str] = None, **params):
        """
        Get enum values for all types or restrict to a specific field/object.

        Args:
            responsedata (str, optional): When given the name of a top-level field or object, restricts the returned JSON to only that field or object (e.g., 'countries').
            **params: Additional query parameters (not officially supported, for forward compatibility).

        Returns:
            dict: Enum values from the Darktrace API.
        """
        endpoint = '/enums'
        url = f"{self.client.host}{endpoint}"
        query_params = dict()
        if responsedata:
            query_params['responsedata'] = responsedata
        # Allow for future/unknown params
        query_params.update(params)
        headers, sorted_params = self._get_headers(endpoint, query_params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()