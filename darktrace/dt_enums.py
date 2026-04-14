from typing import Any, Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Enums"]


class Enums(BaseEndpoint):
    """
    Interact with the /enums endpoint of the Darktrace API.
    The /enums endpoint returns string values for numeric codes (enumerated types) used in many API responses.
    The list of enums can be filtered using the responsedata parameter.
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
        Get enum values for all types or restrict to a specific field/object.

        Args:
            responsedata (str, optional): When given the name of a top-level field or object, restricts the returned JSON to only that field or object (e.g., 'countries').
            **params: Additional query parameters (not officially supported, for forward compatibility).

        Returns:
            dict: Enum values from the Darktrace API.
        """
        query_params = {}
        if responsedata:
            query_params["responsedata"] = responsedata
        # Allow for future/unknown params
        query_params.update(params)
        return self._get("/enums", params=query_params, timeout=timeout)
