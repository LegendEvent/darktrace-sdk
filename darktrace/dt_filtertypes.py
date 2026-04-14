from typing import Any, Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["FilterTypes"]


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

    def get(
        self,
        responsedata: Optional[str] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
        **params,
    ) -> Any:
        """
        Get all filter types or restrict to a specific field/object.

        Args:
            responsedata (str, optional): Restrict the returned JSON to only the specified field/object.
            **params: Additional query parameters (not officially supported).

        Returns:
            list: List of filter type objects from the Darktrace API.
        """
        query_params = {}
        if responsedata:
            query_params["responsedata"] = responsedata
        query_params.update(params)
        return self._get("/filtertypes", params=query_params, timeout=timeout)
