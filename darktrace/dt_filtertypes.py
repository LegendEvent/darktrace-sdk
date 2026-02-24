import requests
from typing import Optional, Union, Tuple
from .dt_utils import debug_print, BaseEndpoint, _UNSET

class FilterTypes(BaseEndpoint):
    """
    Interact with the /filtertypes endpoint of the Darktrace API.
    The /filtertypes endpoint returns all internal Darktrace filters used in the Model Editor, their filter type (e.g., boolean, numeric), and available comparators.

    Args:
        responsedata (str, optional): When given the name of a top-level field or object, restricts the returned JSON to only that field or object.
            Example: responsedata="comparators"
        **params: Additional query parameters (not officially supported, for forward compatibility).

    Returns:
        list: List of filter type objects, each with fields:
            - filtertype (str): The filter name.
            - valuetype (str): The data type expected by the filter.
            - comparators (list): The comparators available for the filter.
            - graphable (bool, optional): True if the filter can be used on a graph.
    """
    def __init__(self, client):
        super().__init__(client)

    def get(self, responsedata: Optional[str] = None, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET, **params):  # type: ignore[assignment]
        """
        Get all filter types or restrict to a specific field/object.

        Args:
            responsedata (str, optional): Restrict the returned JSON to only the specified field/object.
            **params: Additional query parameters (not officially supported).

        Returns:
            list: List of filter type objects from the Darktrace API.
        """
        endpoint = '/filtertypes'
        url = f"{self.client.host}{endpoint}"
        query_params = dict()
        if responsedata:
            query_params['responsedata'] = responsedata
        query_params.update(params)
        headers, sorted_params = self._get_headers(endpoint, query_params)

        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET", url, headers=headers, params=sorted_params,
            verify=self.client.verify_ssl, timeout=resolved_timeout
        )
        response.raise_for_status()
        return response.json()